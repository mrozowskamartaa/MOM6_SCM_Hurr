from gotm_runner import run_gotm_experiments
import json
from itertools import product

import numpy as np


training_set_name = "ePBL_paper"
gotm_case_dict = {}
root_dir = "/gpfs/f5/gfdl_o/scratch/Marta.Mrozowska/hurricane_LES/make_smc_training_set"

temperature_gradients = [0.04, 0.02, 0.01, 0.001]
wind_stresses = [0.1, 0.5, 1.0]
latitudes = [10.0, 30.0, 60.0, 90.0]
heat_fluxes = np.arange(-100,125,25).tolist()

for i, combo in enumerate(product(temperature_gradients, wind_stresses, latitudes, heat_fluxes)):
    temp_grad, tx, lat, hf = combo
    case_name = f"case_{i+1}"
    gotm_case_dict[case_name] = {"temp_grad": temp_grad, "tx": tx, "lat": lat, "heat_flux": hf}

with open(f"{root_dir}/{training_set_name}_training_set_cases.json", "w+") as file:
    json.dump(gotm_case_dict, file)

run_gotm_experiments(
    root_dir=root_dir,
    source_dir_name="source_yaml",
    training_set_name=training_set_name,
    case_dict=gotm_case_dict
)