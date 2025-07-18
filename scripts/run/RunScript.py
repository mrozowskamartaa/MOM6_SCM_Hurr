import sys, os
import numpy as np
import shutil
import importlib.util

HeadDir=os.getcwd()
exe=HeadDir+"/build/ncrc6.intel23/ocean_only/REPRO/MOM6"

os.system("mkdir "+HeadDir+"/work")
os.chdir(HeadDir+"/work")

shutil.copyfile(HeadDir+'/scripts/run/SCM_hurr_aux.py','./SCM_hurr_aux.py')

import SCM_hurr_aux as SCM

#This is the input file in the MOM6-examples test case
SCM.write_MOM_input()
SCM.write_input_nml()
SCM.write_diag_table()

#EXP = "JHL"
#overrides = SCM.JHL_overrides

#EXP = "ePBL-OM5"
#overrides = SCM.OM5_overrides

#EXP = "ePBL-OM4"
#overrides = SCM.OM4_overrides

EXP = "ePBL-CM4X"
overrides = SCM.CM4X_overrides

for TS in ["05","10"]:
    for Y0 in ["5.0E+04",
               "3.0E+04",
               "1.0E+04",
               "0.0E+04",
               "-2.0E+04",
               "-4.0E+04",
               "-6.0E+04",
               "-8.0E+04",
               "-10.0E+04",
               "-20.0E+04",
               ]:
        if (TS=="05"):
            X0 = "6.48E+05"
        elif (TS=="10"):
            X0 = "1.295E+06"
        #These are overrides in the MOM_override file specified as a list
        SCM.write_MOM_override([
            "DT=100",
            "USE_KPP = False",
            #"ENERGETICS_SFC_PBL = True",
            "USE_JACKSON_PARAM = True",
            "IDL_HURR_MAX_WIND = 65.0",
            "IDL_HURR_TRAN_SPEED = "+TS,
            "IDL_HURR_X0 = "+X0,
            "SCM_TEMP_MLD = 32.0",
            "IDL_HURR_SCM_LOCY = "+Y0,
        ]+overrides)

        SCM.run_model(exe=exe)

        os.system("mkdir "+HeadDir+"/results_"+EXP)
        os.system("mkdir "+HeadDir+"/results_"+EXP+"/W65R50T"+TS)
        shutil.copyfile("./ocean.nc",HeadDir+"/results_"+EXP+"/W65R50T"+TS+"/ocean.nc."+Y0)
