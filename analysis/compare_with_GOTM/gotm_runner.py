import os
import shutil
import re
import yaml


def get_title(
        file: str
) -> str:
    
    with open(file, "r") as f:
        data = yaml.safe_load(f)

    return data["title"]


def edit_yaml(
        file: str,
        pattern: str,
        new_string: str
) -> None:
    
    with open(file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    line_to_edit = re.compile(pattern)

    for line in lines:
        match = line_to_edit.match(line)

        if match:
            indent = match.group('indent')
            new_line = (f"{indent}{new_string}\n")
            new_lines.append(new_line)
            continue
    
        new_lines.append(line)

    with open(file, 'w') as f:
        f.writelines(new_lines)


def run_gotm_experiments(
        root_dir: str, 
        source_dir_name: str,
        forcing_dir_name: str, 
        case_dict: dict
    ) -> None:

    source_file = os.path.join(root_dir, source_dir_name, "gotm.yaml")
    forcing_dir = os.path.join(root_dir, forcing_dir_name)
    
    experiment_name = get_title(source_file)
    experiment_dir = os.path.join(root_dir, "experiments", experiment_name)
    os.makedirs(experiment_dir, exist_ok=True)
    shutil.copy(source_file, experiment_dir)  # TODO: Also copy initial t_profile! Make each stand-alone experiment reproducible by running gotm_runner with specific run files from the exp directory

    for case_specs, case_name in case_dict.items():
        case_dir = os.path.join(experiment_dir, f"{case_name}")
        case_file = os.path.join(root_dir, case_dir, "gotm.yaml")
        wind_mag, loc = case_specs
        forcing_file = os.path.join(forcing_dir, wind_mag, f"momentumflux{loc.zfill(3)}.dat")

        os.makedirs(case_dir, exist_ok=True)
        shutil.copy(source_file, case_dir)

        tau_pattern = r'^(?P<indent>\s*)file:\s+tau_file.dat'
        output_pattern = r'^(?P<indent>\s*)output_filename'
        output_file = os.path.join(case_dir, f"output")

        edit_yaml(
            file=case_file,
            pattern=tau_pattern,
            new_string=f"file: {forcing_file}"
        )

        edit_yaml(
            file=case_file,
            pattern=output_pattern,
            new_string=f"{output_file}:"
        )
        
        os.chdir(case_dir)
        os.system('gotm')
