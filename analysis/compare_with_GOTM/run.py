from gotm_runner import run_gotm_experiments
import json


type_ = "no_langmuir"

with open(f"/gpfs/f5/gfdl_o/scratch/Marta.Mrozowska/hurricane_LES/MOM6_SCM_Hurr/analysis/{type_}_cases.json", "r") as file:
    cases_dict = json.load(file)

gotm_case_dict = {}

for i, case in cases_dict.items():
    wind_mag, loc = case['wind_mag'], str(case['loc'])
    name = f"T{wind_mag}L{loc.zfill(3)}_{type_}"
    gotm_case_dict[(wind_mag, loc)] = name

run_gotm_experiments(
    root_dir="/gpfs/f5/gfdl_o/scratch/Marta.Mrozowska/hurricane_LES/MOM6_SCM_Hurr/analysis/compare_with_GOTM",
    source_dir_name="experiments",
    forcing_dir_name="experiments/forcing",
    case_dict=gotm_case_dict
)