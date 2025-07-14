import sys, os

def write_MOM_input():
    ##MOM6 parameters                                                                                                                                                          
    with open("MOM_input", "w") as file:
        for inputs in [
                "REENTRANT_Y = True",
                "NIGLOBAL = 2",
                "NJGLOBAL = 2",
                "NIHALO = 2",
                "NJHALO = 2",
                "SPLIT = False",
                "USE_REGRIDDING = True",
                "DT = 1200.0",
                "FRAZIL = True",
                "C_P = 3992.10322329649",
                "SAVE_INITIAL_CONDS = True",
                "GRID_CONFIG = \"cartesian\"",
                "SOUTHLAT = 27.836",
                "LENLAT = 2.0",
                "LENLON = 2.0",
                "TOPO_CONFIG = \"flat\"",
                "ROTATION = \"betaplane\"",
                "F_0 = 6.8103E-05",
                "G_EARTH = 9.81",
                "RHO_0 = 1027.0",
                "MAXIMUM_DEPTH = 300.0",
                "NK = 600",
                "EQN_OF_STATE = \"LINEAR\"",
                "DRHO_DS = 0.0",
                "REGRIDDING_COORDINATE_MODE = \"Z*\"",
                "TS_CONFIG = \"SCM_CVMix_tests\"",
                "SCM_TEMP_MLD = 32.0",
                "SCM_L1_TEMP = 29.25 ",
                "SCM_L2_TEMP = 29.25",
                "SCM_L2_DTDZ = 0.04",
                "HBBL = 10.0",
                "CDRAG = 0.0 ",
                "DRAG_BG_VEL = 0.1",
                "BBL_THICK_MIN = 0.1",
                "KV = 1.0E-04",
                "UPWIND_1ST_CONTINUITY = True",
                "ETA_TOLERANCE = 1.0E-06",
                "CORIOLIS_EN_DIS = True",
                "BOUND_CORIOLIS = True",
                "BIHARMONIC = False",
                "HARMONIC_VISC = True",
                "HMIX_FIXED = 0.01",
                "MAXVEL = 6.0",
                "VEL_UNDERFLOW = 1.0E-30",
                "USE_KPP = True",
                "KPP%",
                "APPLY_NONLOCAL_TRANSPORT = False",
                "INTERP_TYPE = cubic",
                "ANSWER_DATE = 20240101",
                "%KPP",
                "RECLAIM_FRAZIL = False",
                "KHTR = 600.0",
                "MAXTRUNC = 5000",
                "ENERGYSAVEDAYS = 0.25",
                "BUOY_CONFIG = \"const\"",
                "SENSIBLE_HEAT_FLUX = 0.0",
                "WIND_CONFIG = \"ideal_hurr\"",
                "IDL_HURR_X0 = 6.48E+05",
                "IDL_HURR_SCM_BR_BENCH = True",
                "IDL_HURR_SCM = True",
                "IDL_HURR_SCM_EDGE_TAPER_BUG = True",
                "DAYMAX = 3.0",
                "RESTART_CONTROL = 0",
                "RESTINT = 3650.0",
                "U_TRUNC_FILE = \"U_velocity_truncations\"",
                "V_TRUNC_FILE = \"V_velocity_truncations\"",
        ]:
            file.write(inputs+"\n")

def write_input_nml():
    with open("input.nml", "w") as file:
        for inputs in [
                "&MOM_input_nml",
                "output_directory = './',",
                "input_filename = 'n'",
                "restart_input_dir = 'INPUT/',",
                "restart_output_dir = 'RESTART/',",
                "parameter_filename = 'MOM_input','MOM_override'",
                "/",
                "&diag_manager_nml",
                "/",
                "&fms_nml",
                "clock_grain = 'LOOP',",
                "domains_stack_size = 710000,",
                "stack_size = 0",
                "/",
                "&ocean_domains_nml",
                "/",
                "&ice_model_nml",
                "/",
        ]:
            file.write(inputs+"\n")

def write_diag_table():
    mod = "ocean_model"

    with open("diag_table", "w") as file:
        file.write("\"MOM Experiment\"\n"+
                   "1 1 1 0 0 0\n"+
                   "\"ocean\",15,\"minutes\",1,\"days\",\"Time\"\n")
        for var in ["taux","tauy","net_heat_surface","u","v","temp","salt","Tflx_dia_diff","Bflx_dia_diff",
                    ]:
            file.write("\""+mod+"\""+","+
                       "\""+var+"\""+","+"\""+var+"\""+","+
                       "\"ocean\",\"all\",.false.,\"none\",2\n")

def write_MOM_override(INP=["",]):
    ##MOM6 parameters                                                                                                                                                          
    with open("MOM_override", "w") as file:
        file.write("#MOM_override file\n")
        for inputs in INP:
            file.write("#override "+inputs+"\n")
            
def run_model(exe="./MOM6"):
    os.system(exe)

