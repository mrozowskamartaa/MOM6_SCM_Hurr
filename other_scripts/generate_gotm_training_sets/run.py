from gotm_runner import run_gotm_experiments
# from gotm_runner_f_u_star_grid import run_gotm_experiments
import json
from itertools import product

import numpy as np


training_set_name = "ePBL_paper_2283_corrected_dz0.1"
gotm_case_dict = {}
root_dir = "/gpfs/f5/gfdl_o/scratch/Marta.Mrozowska/hurricane_LES/make_smc_training_set"

temperature_gradients = [0.001, 0.01, 0.02, 0.04]  # ePBL paper, ePBL paper expanded
# temperature_gradients = [0.001, 0.04]  # ePBL paper reduced
# temperature_gradients = [0.005, 0.015, 0.03]  # ePBL paper validation, ePBL validation dz=0.1
# temperature_gradients = [0.5, 1.]  # non-rotating
# wind_stresses = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]  # ePBL paper expanded with smaller tx values
wind_stresses = [0.01, 0.05, 0.1, 0.5, 1.0]  # ePBL paper expanded with smaller tx values (0.001 and 0.005 were too small)
# wind_stresses = np.arange(0.1, 1.1, 0.1).tolist()  # ePBL paper expanded
# wind_stresses = [0.25, 0.75, 0.95]  # ePBL paper validation
# wind_stresses = [0.025, 0.25, 0.75]  # ePBL validation dz=0.1
# wind_stresses = [0.1, 0.5, 1.0]  # ePBL paper
# wind_stresses = [0.1, 1.0]  # non-rotating
latitudes = np.arange(10., 100., 10.).tolist()  # ePBL paper expanded
# latitudes = [15., 25., 55., 85.]  # ePBL paper validation, ePBL validation dz=0.1
# latitudes = [10., 30., 60., 90.]  # ePBL paper
# latitudes = [10., 90.]  # ePBL paper reduced
# latitudes = [0.0, 1., 5., 60.]  # non-rotating
# heat_fluxes = [0.0]
heat_fluxes = np.arange(-100,125,25).tolist()  # ePBL paper expanded, ePBL paper
# heat_fluxes = [-90, -40, -10, 10, 40, 90]  # ePBL paper validation
# heat_fluxes = [0.0, 100.0]  # non-rotating

for i, combo in enumerate(product(temperature_gradients, wind_stresses, latitudes, heat_fluxes)):
    temp_grad, tx, lat, hf = combo
    case_name = f"case_{i+1}"
    gotm_case_dict[case_name] = {"temp_grad": temp_grad, "tx": tx, "lat": lat, "heat_flux": hf}

with open(f"{root_dir}/{training_set_name}_training_set_cases.json", "w+") as file:
    json.dump(gotm_case_dict, file)

# with open(f"{root_dir}/{training_set_name}_training_set_cases.json", "r") as file:
#     gotm_case_dict = json.load(file)

# for i in range(1,35):
#     gotm_case_dict.pop(f"case_{i}")

run_gotm_experiments(
    root_dir=root_dir,
    source_dir_name="source_yaml",
    training_set_name=training_set_name,
    case_dict=gotm_case_dict
)