import os
import sys
import glob

from . import tsutils
from binaries.conda.build_packages import conda_build

REPO_ROOT = os.getcwd()


def build():
    print("## Started torchserve and modelarchiver build")
    create_wheel_cmd = "python setup.py bdist_wheel --release --universal"

    # Build torchserve wheel
    print(f"## In directory: {os.getcwd()} | Executing command: {create_wheel_cmd}")
    ts_build_exit_code = os.system(create_wheel_cmd)

    # Build model archiver wheel
    os.chdir("model-archiver")
    print(f"## In directory: {os.getcwd()} | Executing command: {create_wheel_cmd}")
    ma_build_exit_code = os.system(create_wheel_cmd)

    os.chdir(REPO_ROOT)

    ts_wheel_path = glob.glob(os.path.join(REPO_ROOT, "dist", "*.whl"))[0]
    ma_wheel_path = glob.glob(os.path.join(REPO_ROOT, "model-archiver", "dist", "*.whl"))[0]
    print(f"## TorchServe wheel location: {ts_wheel_path}")
    print(f"## Model archiver wheel location: {ma_wheel_path}")

    # Build TS & MA on Conda if available
    conda_build_exit_code = 0
    if tsutils.is_conda_env():
        conda_build_exit_code = conda_build(ts_wheel_path, ma_wheel_path)

    # If any one of the steps fail, exit with error
    if ts_build_exit_code != 0:
        sys.exit("## Torchserve Build Failed !")
    if ma_build_exit_code != 0:
        sys.exit("## Model archiver Build Failed !")
    if conda_build_exit_code != 0:
        sys.exit("## Conda Build Failed !")


if __name__ == "__main__":
    build()
