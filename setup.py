import sys
import pkg_resources
from os.path import join, basename
from cx_Freeze import setup, Executable


def collect_dist_info(packages):

    if not isinstance(packages, list):
        packages = [packages]
    dirs = []

    for pkg in packages:
        distrib = pkg_resources.get_distribution(pkg)
        for req in distrib.requires():
            dirs.extend(collect_dist_info(req.key))
        print(distrib.egg_info)
        dirs.append((distrib.egg_info, join('Lib', basename(distrib.egg_info))))

    return dirs
# Dependencies are automatically detected, but it might need fine tuning.

build_exe_options = {
                     "include_msvcr": True,
                     "packages":
                         ["scipy.sparse", "scipy.spatial", "scipy.spatial.ckdtree", "scipy",
                          "multiprocessing.pool"],
                     "excludes": ["scipy.spatial.cKDTree", "multiprocessing.Pool"],
                     "include_files": collect_dist_info(["scipy"])}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "LAMS",
        version = "0.1",
        description = "LAMS",
        options = {"build_exe": build_exe_options},
        executables = [Executable("app.py", base=base)])