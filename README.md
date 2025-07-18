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


