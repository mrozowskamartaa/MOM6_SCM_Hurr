# MOM6_SCM_Hurr

Step 1:  Checkout this repository  
git clone https://github.com/breichl/MOM6_SCM_Hurr.git  

Step 2:  Update submodules  
cd MOM6_SCM_Hurr  
git submodule update --init --recursive  
cd src/MOM6  
git submodule update --init --recursive  
cd ../..  

Step 3:  Compile
./scripts/compile/OceanComp.csh

Step 4:  Run
See the sample run script in scripts/run  
It is presently set up to run with overrides for experiments in the file "SCM_hurr_aux.py"
You can comment/uncomment to run with various scenarios

Step 5: Analysis
A sample analysis notebook is in the analysis folder  


_INCLUDING GOTM CASES_

Step 1: Install GOTM (conda/mamba env to build)

a. Install miniconda: https://docs.rdhpcs.noaa.gov/software/python/miniforge.html

b. Make directory for GOTM:  
mkdir GOTM  
cd GOTM  
git clone https://github.com/gotm-model/code gotm-code  
(optional)  
cd ..  
git clone https://github.com/gotm-model/cases gotm-cases  

c. Make conda environment for GOTM:  
conda create -n gotm-env -c conda-forge fortran-compiler netcdf-fortran cmake  
conda activate gotm-env  

d. Build GOTM:  
(In GOTM directory)  
mkdir gotm-install  
mkdir build  
cd build  
cmake ../gotm-code -DGOTM_USE_FABM=off -DCMAKE_INSTALL_PREFIX=/absolute/path/to/GOTM/gotm-install  
make -j$(nproc)  
make install  

e. Activate GOTM:  
export PATH="/absolute/path/to/GOTM/gotm-install/bin:$PATH"  

f. Verify installation (and optionally, run a test case):  
gotm --version  
cd ../gotm-cases/ows_papa/  
gotm  
