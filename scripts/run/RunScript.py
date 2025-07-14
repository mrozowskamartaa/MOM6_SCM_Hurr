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


#These are overrides in the MOM_override file specified as a list
SCM.write_MOM_override([
    "DT=100",
    "USE_KPP = False",
    "ENERGETICS_SFC_PBL = True",
    "USE_JACKSON_PARAM = True",
    "IDL_HURR_MAX_WIND = 65.0",
    "IDL_HURR_TRAN_SPEED = 5.0",
    "SCM_TEMP_MLD = 32.0",
    "IDL_HURR_SCM_LOCY = 5.0E+04",
])

SCM.run_model(exe=exe)
