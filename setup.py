from distutils.cmd import Command
from setuptools import setup, find_packages
from setuptools.command import build_py
from wheel.bdist_wheel import bdist_wheel

import git
import os
import pathlib
import subprocess
import sys
import tempfile


here = pathlib.Path(__file__).parent.resolve()


class BdistWheelCommand(bdist_wheel):

    def finalize_options(self):
        super().finalize_options()
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = super().get_tag()
        return python, "none", plat


class BuildPatomicCommand(Command):

    description = "Build patomic shared library"
    user_options = [
        ("git-url=", 'u', "[str] URL to patomic git repo"),
        ("git-tag=", 't', "[str] Tag of commit to use from git repo"),
        ("dst-dir=", 'd', "[str] Directory to place patomic shared library"),
        ("build-type=", 'b', "[str] CMake build type to use when building patomic"),
        ("force-replace=", 'f', "[bool] Whether to replace existing patomic shared library file(s)"),
        ("verbose-cmake=", None, "[bool] Whether to print CMake output to stdout"),
        ("c-compiler=", 'c', "[str] C compiler executable"),
        ("c-standard=", 's', "[int] ISO C Standard to pass to the compiler")
    ]

    def initialize_options(self) -> None:
        self.git_url = "https://github.com/doodspav/patomic"
        self.git_tag = None
        self.dst_dir = here / "src" / "atomics" / "_clib"
        self.build_type = "Release"
        self.force_replace = False
        self.verbose_cmake = False
        self.c_compiler = None
        self.c_standard = 11

    def finalize_options(self) -> None:
        if type(self.dst_dir) is not pathlib.Path:
            self.dst_dir = pathlib.Path(self.dst_dir).resolve()
        if self.c_compiler in [89, 95]:
            self.c_compiler = 90
        if self.git_tag is not None:
            raise RuntimeError(f"Option 'git-tag' (set to: {self.git_tag}) not supported.")

    @staticmethod
    def get_patomic_libs(dir_path: pathlib.Path) -> [pathlib.Path]:
        """Returns a list of patomic shared library files found in dir_path"""
        assert dir_path.is_dir()
        exts = [".dll", ".dylib", ".so"]
        files = [p for p in dir_path.iterdir() if p.is_file()]
        libs = [f for f in files if any(map(str(f).__contains__, exts))]
        patomic_libs = [f for f in libs if "patomic" in str(f)]
        return patomic_libs

    def clone_patomic(self, clone_to: pathlib.Path) -> None:
        """Clones self.git_url into clone_to directory path"""
        assert clone_to.is_dir()
        # clone default branch
        repo = git.Repo.clone_from(url=self.git_url, to_path=str(clone_to))
        # switch to devel branch if main isn't populated
        if not (clone_to / "src").is_dir():
            repo.git.checkout("devel")

    def build_patomic(self, repo_dir: pathlib.Path) -> pathlib.Path:
        """Builds patomic shared library in repo_dir and returns library file path"""
        assert repo_dir.is_dir()
        use_shell = (os.name == "nt")
        fd_out = sys.stdout if self.verbose_cmake else subprocess.DEVNULL
        # configure build directory
        os.mkdir(str(repo_dir / "build"))
        cmd_config = [
            "cmake", "-S", repo_dir, "-B", repo_dir / "build",
            f"-DCMAKE_BUILD_TYPE={self.build_type}",
            f"-DCMAKE_C_STANDARD={self.c_standard}",
            "-DBUILD_SHARED_LIBS=ON"
        ]
        if self.c_compiler:
            cmd_config.append(f"-DCMAKE_C_COMPILER={self.c_compiler}")
        subprocess.check_call(cmd_config, stdout=fd_out, shell=use_shell)
        # build
        out_path = repo_dir / "build"
        cmd_build = ["cmake", "--build", out_path, "--config", self.build_type]
        subprocess.check_call(cmd_build, stdout=fd_out, shell=use_shell)
        # check if using multi-config generator
        if (out_path / self.build_type).is_dir():
            out_path /= self.build_type
        lib_paths = self.get_patomic_libs(out_path)
        lib_paths.sort(reverse=True)
        assert lib_paths, "Should not be empty of CMake succeeds"
        return lib_paths[0]

    def run(self):
        dst_dir = pathlib.Path(self.dst_dir).resolve()
        existing_libs = self.get_patomic_libs(dst_dir)
        # check whether we replace any existing files
        if existing_libs and not self.force_replace:
            print("[build_patomic] skipping; library already built")
            return
        # create shared library and copy over
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = pathlib.Path(temp_dir)
            print("[build_patomic] cloning repo")
            self.clone_patomic(repo_path)
            print("[build_patomic] building shared library")
            lib_path = self.build_patomic(repo_path)
            if self.force_replace and existing_libs:
                print("[build_patomic] removing existing shared library file(s)")
                for el in existing_libs:
                    el.unlink(missing_ok=True)
            print("[build_patomic] copying over shared library")
            os.rename(str(lib_path), str(self.dst_dir / lib_path.name))


class BuildPyCommand(build_py.build_py):

    def run(self):
        self.run_command("build_patomic")
        build_py.build_py.run(self)


setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"atomics": ["_clib/*"]},
    cmdclass={
        "bdist_wheel": BdistWheelCommand,
        "build_patomic": BuildPatomicCommand,
        "build_py": BuildPyCommand,
    }
)
