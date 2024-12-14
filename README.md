(for better visibility of the readme, you may view this on github: https://github.com/RT4404/U21-Project)

# Steps to run the project

## Vortex Setup
Before starting, install the Vortex platform following the quick-start steps from the original repo's README.md: https://github.com/vortexgpgpu/vortex/tree/master

For comprehensiveness and clarity, the necessary steps will also be displayed here (these steps are directly from their repo):

### Platform
* Ubuntu 20.04 (VirtualBox also okay)
### Installing Vortex
```sh
git clone --depth=1 --recursive https://github.com/vortexgpgpu/vortex.git
cd vortex
```
### Installing dependencies
```sh
sudo ./ci/install_dependencies.sh
```
### Configure your build folder
```sh
mkdir build
cd build
# for 32bit
../configure --xlen=32 --tooldir=$HOME/tools
# for 64bit
../configure --xlen=64 --tooldir=$HOME/tools
```
### Install prebuilt toolchain
```sh
./ci/toolchain_install.sh --all
```
### set environment variables
```sh
# should always run before using the toolchain!
source ./ci/toolchain_env.sh
```
### Building Vortex
```sh
make -s
```
### Test if Vortex works with a quick demo
```sh
./ci/blackbox.sh --cores=2 --app=vecadd
```
## U21 Scripts Overview
The three scripts that are part of the U21 Project are:
* blackboxthree.sh: a version of Vortex's blackbox.sh script that includes configuration options from Vortex's VX_config.vh file.
* run_tests.sh: a script based on Vortex's regression.sh.in script that collects data into log files and places them into organized directories.
* format_stats.py: a Python script that formats selected log files into CSV files with a chosen metric (e.g. IPC, cache hit rate, memory latency, etc.) for readability and data visualization.

## U21 Scripts Setup
The three scripts are located in "\XXX\U21-Project-main\U21-Project-main\ci" directory of this installation (XXX is where the project is downloaded to. The complete path might be Home\Downloads\U21-Project-main\U21-Project-main\ci for example). 

The steps to setup the scripts with Vortex are as follows:
* Place the ci folder from this project into the ci folder (vortex/ci) of your Vortex installation.
* Run the following commands from a fresh terminal:
```sh
cd vortex/ci
# Give read, write, and execute permissions to the scripts
chmod a+rwx blackboxthree.sh run_tests.sh format_stats.py
cd ~
cd vortex/build
../configure
source ./ci/toolchain_env.sh
make -s
```

## Running the U21 Scripts
For every new session, ensure that the following commands are run for Vortex to run properly:
```sh
cd vortex/build
../configure
source ./ci/toolchain_env.sh
make -s
```
Also ensure that you are in the vortex/build directory when running the scripts.
### blackboxthree.sh
```sh
# Example test
./ci/blackboxthree.sh --app=sgemm --driver=rtlsim --l1cache_disable

# run --help to see available options and how to use them
./ci/blackboxthree.sh --help
```

### run_tests.sh
Results from this script are stored in vortex/build/RESULTS
```sh
# run --help to know how to use the script
./run_tests.sh --help

# Command to run all tests sequentially
./run_tests.sh --all

# Command to run just baseline tests
./run_tests.sh --baseline

# Command to run baseline and cache tests
./run_tests.sh --baseline --cache
```

### format_stats.py
Results from this script are stored in vortex/build/CSV_results
Before running, ensure that the log files exist (run_tests.sh should be run first to generate the necessary log files).
```sh
# Example command to retrieve IPC metrics from all log files for baseline sgemmx tests
./format_stats.py ./RESULTS/Baseline/sgemmx IPC

# Example command to retrieve IPC metrics from all log files for baseline sgemmx tests and tests that disable L1 cache
./format_stats.py ./RESULTS/Baseline/sgemmx ./RESULTS/Cache_configurations/disable_L1_cache

# Example command to retrieve memory latency metric from all log files for baseline sgemmx tests
./format_stats.py ./RESULTS/Baseline/sgemmx "memory latency"
```
