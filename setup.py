from setuptools import setup, find_packages, Command, Extension
from setuptools.command import build_py
from wheel.bdist_wheel import bdist_wheel

import configparser
import git
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from typing import List, Optional


here = pathlib.Path(__file__).parent.resolve()


class BdistWheelCommand(bdist_wheel):

    @staticmethod
    def _supported_versions() -> List[str]:
        """Parses setup.cfg to return equiv of ['36', '37', ...]"""
        cfg = configparser.ConfigParser()
        cfg.read("setup.cfg")
        classifiers = cfg["metadata"]["classifiers"].split("\n")
        prefix = "Programming Language :: Python ::"
        versions = []
        for c in classifiers:
            if c.startswith(prefix) and "." in c:
                # prefix X.Y
                v = c.strip(prefix).strip().replace(".", "")
                versions.append(v)
        return versions

    @staticmethod
    def _in_ci() -> bool:
        return bool(os.environ.get("CI"))

    def get_tag(self):
        python, abi, plat = super().get_tag()
        abi = "none"
        if self._in_ci():
            python = "py" + ".py".join(self._supported_versions())
        return python, abi, plat


class BuildPatomicCommand(Command):

    verbose: int  # inherited

    logger: logging.Logger

    git_url: str
    git_tag: Optional[str]
    dest_dir: pathlib.Path
    build_type: str
    force_replace: bool
    cc_path: Optional[pathlib.Path]
    cc_standard: int
    cmake_args: str
    linker_args: Optional[str]

    description = "Clone and build patomic shared library"
    user_options = [
        ("git-url=", 'u', "[str] URL to patomic git repo"),
        ("git-tag=", 't', "[str] Tag of commit to use from git repo"),
        ("dest-dir=", 'd', "[str] Directory to place built patomic shared library"),
        ("build-type=", 'b', "[str] CMake build type"),
        ("force-replace=", 'f', "[bool] Replace existing patomic file(s)"),
        ("cc-path=", 'c', "[str] C compiler path"),
        ("cc-standard=", 's', "[int] ISO C standards version"),
        ("cmake-args=", 'a', "[str] Opaque string appended to cmake config command"),
        ("linker-args=", 'l', "[str] Opaque string passed to shared library linker")
    ]

    def initialize_options(self) -> None:
        self.git_url = "https://github.com/doodspav/patomic"
        # pin to patomic v0.2.2 until we migrate to stable release
        # self.git_tag = None
        self.git_tag = "v0.2.2"
        self.dest_dir = here / "src" / "atomics" / "_clib"
        self.build_type = "RelWithDebInfo"
        self.force_replace = False
        self.cc_path = None
        self.cc_standard = 11
        self.cmake_args = ""
        self.linker_args = None
        # override defaults with env here
        # command line takes precedence over env
        self._obtain_env_options()

    def finalize_options(self) -> None:
        # coerce types
        self.dest_dir = pathlib.Path(self.dest_dir).resolve()
        self.cc_standard = int(self.cc_standard)
        # fix bool
        if isinstance(self.force_replace, str):
            sfr = self.force_replace.lower().strip()
            if sfr.isnumeric():
                self.force_replace = bool(int(self.force_replace))
            else:
                self.force_replace = (sfr == "true")
        # coerce compiler values
        if self.cc_path is not None:
            self.cc_path = pathlib.Path(self.cc_path)
        if self.cc_standard in [89, 95]:
            self.cc_standard = 90
        # setup logger
        self._init_logger()
        self._log_options()

    def _obtain_env_options(self) -> None:
        for name, _, _ in self.user_options:
            attr_name = name.replace("-", "_")[:-1]
            env_name = f"BUILD_PATOMIC_{attr_name.upper()}"
            env = os.environ.get(env_name)
            if env:
                setattr(self, attr_name, env)

    def _init_logger(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._set_verbosity()
        # setup formatting
        sh = logging.StreamHandler()
        template = "[build_patomic] [{levelname}] [{funcName}] {message}"
        fmt = logging.Formatter(template, style="{")
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)

    def _set_verbosity(self) -> None:
        # # get verbosity from env variable
        # env = os.environ.get("BUILD_PATOMIC_VERBOSE")
        # if env:
        #     try:
        #         v = int(env)
        #     except ValueError:
        #         v = 1
        #     self.verbose = max(v, self.verbose)
        # # set log level
        # log_level = 0
        # if self.verbose <= 0:
        #     log_level = logging.WARN
        # elif self.verbose == 1:
        #     log_level = logging.INFO
        # elif self.verbose >= 2:
        #     log_level = logging.DEBUG
        log_level = logging.DEBUG
        self.logger.setLevel(log_level)

    def _log_options(self) -> None:
        opts = {}
        for name, _, _ in self.user_options:
            attr = name.replace("-", "_")[:-1]
            opts[attr] = getattr(self, attr)
        opts["verbose"] = self.verbose
        self.logger.debug(str(opts))

    @staticmethod
    def _cibw_check_win32_x86() -> bool:
        """Checks if CIBW is building for win32-x86"""
        env = os.environ.get("CIBW_MC_NAME")
        return type(env) is str and env.lower() == "win32-x86"

    def get_patomic_libs(self, dir_path: pathlib.Path) -> [pathlib.Path]:
        """Returns a list of patomic shared library files found in dir_path"""
        assert dir_path.is_dir()
        exts = [".dll", ".dylib", ".so"]
        self.logger.debug(f"all paths in {str(dir_path)}: {list(dir_path.iterdir())}")
        files = [p for p in dir_path.iterdir() if p.is_file()]
        self.logger.debug(f"files: {files}")
        libs = [f for f in files if any(map(str(f).__contains__, exts))]
        self.logger.debug(f"libs: {libs}")
        patomic_libs = [f for f in libs if "patomic" in str(f)]
        return patomic_libs

    def clone_patomic(self, clone_into: pathlib.Path) -> None:
        """Clones git_url into clone_to directory"""
        assert clone_into.is_dir()
        # clone default branch
        repo = git.Repo.clone_from(url=self.git_url, to_path=str(clone_into))
        self.logger.debug(f"Cloned patomic repo into: {str(clone_into)}")
        if self.git_tag:
            self.logger.info(f"Checkout out user provided tag: {self.git_tag}")
            repo.git.checkout(self.git_tag)
            if not (clone_into / "src").is_dir():
                self.logger.warning(f"No src directory found in checked out tag: {self.git_tag}")

    def config_patomic(self, repo_dir: pathlib.Path) -> None:
        """Configures CMake for in repo_dir"""
        assert repo_dir.is_dir()
        use_shell = (os.name == "nt")
        fd_out = sys.stdout if self.logger.level == logging.DEBUG else subprocess.DEVNULL
        # setup build dir
        os.mkdir(str(repo_dir / "build"))
        self.logger.debug(f"Created: {str(repo_dir / 'build')}")
        # setup cmd base
        cmd_config = [
            "cmake", "-S", str(repo_dir), "-B", str(repo_dir / "build"),
            f"-DCMAKE_BUILD_TYPE={self.build_type}",
            f"-DCMAKE_C_STANDARD={self.cc_standard}",
            "-DBUILD_SHARED_LIBS=ON",
            "-DBUILD_TESTING=OFF"
        ]
        # build up cmd
        if self.cc_path:
            self.logger.info(f"C compiler set to: {self.cc_path}")
            cmd_config.append(f"-DCMAKE_C_COMPILER={str(self.cc_path)}")
        if self.linker_args:
            self.logger.info(f"Linker args: {self.linker_args}")
            cmd_config.append(f"-DCMAKE_SHARED_LINKER_FLAGS={self.linker_args}")
        if self._cibw_check_win32_x86():
            self.logger.info("Running under win32-x86 on CIBW - using '-A Win32'")
            cmd_config.append("-AWin32")
        if self.cmake_args:
            self.logger.info(f"Appending CMake args: {self.cmake_args}")
            cmd_config.append(self.cmake_args)
        # configure cmake
        self.logger.debug(f"Configuring CMake as: {cmd_config}")
        subprocess.check_call(cmd_config, stdout=fd_out, shell=use_shell)
        self.logger.debug("Configured CMake for patomic")

    def build_patomic(self, repo_dir: pathlib.Path) -> pathlib.Path:
        """Builds patomic in configured repo_dir and returns shared library file path"""
        assert repo_dir.is_dir()
        use_shell = (os.name == "nt")
        fd_out = sys.stdout if self.logger.level == logging.DEBUG else subprocess.DEVNULL
        # build
        build_path = repo_dir / "build"
        cmd_build = ["cmake", "--build", str(build_path), "--config", self.build_type]
        subprocess.check_call(cmd_build, stdout=fd_out, shell=use_shell)
        self.logger.debug(f"Built patomic in: {str(build_path)}")
        # check if using multi-config generator
        if (build_path / self.build_type).is_dir():
            build_path /= self.build_type
        # return most specific lib path (e.g. .so.x.y.z not .so)
        # done by length to support both .so.x.y.z and .x.y.z.dylib
        lib_paths = self.get_patomic_libs(build_path)
        lib_paths.sort(reverse=True, key=lambda p: len(str(p)))
        assert lib_paths, "Should not be empty if CMake succeeds"
        self.logger.debug(f"Chosen patomic lib path: {str(lib_paths[0])}")
        return lib_paths[0]

    def run(self):
        self.logger.debug(f"Contents of dest_dir: {list(self.dest_dir.iterdir())}")
        existing_lib_paths = self.get_patomic_libs(self.dest_dir)
        self.logger.debug(f"Existing lib paths: {existing_lib_paths}")
        # check if we can replace libs
        if existing_lib_paths and not self.force_replace:
            self.logger.info("Skipping; library already build")
            return
        # create shared library and copy over
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # clone repo and build
                repo_path = pathlib.Path(temp_dir)
                self.logger.info("Cloning repo")
                self.clone_patomic(repo_path)
                self.logger.info("Configuring CMake")
                self.config_patomic(repo_path)
                self.logger.info("Building shared library")
                lib_path = self.build_patomic(repo_path)
                self.logger.info("Built shared library successfully")
                # copy stuff over
                if self.force_replace and existing_lib_paths:
                    self.logger.info("Removing existing shared library file(s)")
                    for elp in existing_lib_paths:
                        try:
                            elp.unlink(missing_ok=True)
                        except PermissionError:
                            self.logger.info(f"Could not remove file {str(elp)}")
                self.logger.info(f"Copying over shared library file to: {str(self.dest_dir)}")
                shutil.move(str(lib_path), str(self.dest_dir / lib_path.name))
                # log result
                self.logger.debug(f"Files in {str(self.dest_dir)}: {list(self.dest_dir.iterdir())}")
                self.logger.info("Copied over file successfully")
        except PermissionError:
            self.logger.info(f"Could not close temporary directory")


class BuildPyCommand(build_py.build_py):

    def run(self):
        self.run_command("build_patomic")
        build_py.build_py.run(self)


# setup dummy extension to force non-pure python build
# CIBW won't build pure python projects
with open("dummy.c", "w") as f:
    f.truncate()
    f.write("/* temporary file - safe to delete */\n")
    f.write("extern int PyInit_dummy(void) { return 0; }\n")


try:
    setup(
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        package_data={"atomics": ["_clib/*"]},
        cmdclass={
            "bdist_wheel": BdistWheelCommand,
            "build_patomic": BuildPatomicCommand,
            "build_py": BuildPyCommand
        },
        ext_modules=[Extension(name="dummy", sources=["dummy.c"])]
    )
finally:
    # cleanup extension
    os.remove("dummy.c")
