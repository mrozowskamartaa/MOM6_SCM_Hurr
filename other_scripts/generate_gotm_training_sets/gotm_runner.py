import os
import shutil
import re
from datetime import datetime, timedelta

import numpy as np


def generate_time_range(start, end, delta):
    current_date = start
    while current_date < end:
        yield current_date
        current_date += timedelta(days=delta)


# IMPORTANT: ASSUMES 1m VERTICAL SPACING
def make_t_profile(
        case_dir: str,
        depth: int,
        mld: int,
        temp_grad: float = 0.04,
        mld_temp: float = 29.25
) -> str:
    
    t_profile = np.empty(depth)
    t_profile[0:mld] = mld_temp
    t_profile[mld:] = mld_temp - temp_grad*np.arange(1,depth-mld+1,1)

    z_start = - depth + 0.5
    z_end = 0.5
    z_levels = np.arange(z_start,z_end,1)[::-1]

    date_start = datetime(2011, 4, 1)
    date_end = datetime(2012, 5, 1)
    delta = 1
    date_list = list(generate_time_range(date_start, date_end, delta))

    filename = os.path.join(case_dir, "t_profile.dat")

    with open(filename, "w", encoding='utf-8') as file:
        for date in date_list:
            data_string_list = [f"{z}\t{t}" for z, t in zip(z_levels,t_profile)]
            data_string = "\n".join(data_string_list)
            file.write(f"{str(date)}\t{depth}\t{2}\n{data_string}\n")

    return filename


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
        training_set_name: str,
        case_dict: dict
    ) -> None:

    source_file = os.path.join(root_dir, source_dir_name, "gotm.yaml")

    for case_ in case_dict.items():

        case_name, case_specs = case_
        case_dir = os.path.join(root_dir, f"{training_set_name}_training_dataset", case_name)
        os.makedirs(case_dir, exist_ok=True)
        shutil.copy(source_file, case_dir)
        case_file = os.path.join(case_dir, "gotm.yaml")

        t_profile_pattern = r'^(?P<indent>\s*)file:\s+t_prof.dat'
        t_profile_file = make_t_profile(
            case_dir=case_dir,
            depth=600,  # depth=300,
            mld=32,
            temp_grad=case_specs["temp_grad"]
        )

        output_pattern = r'^(?P<indent>\s*)output_filename'
        output_file = os.path.join(case_dir, f"output")

        tau_pattern = r'^(?P<indent>\s*)constant_value:\s+tx'
        heat_flux_pattern = r'^(?P<indent>\s*)constant_value:\s+heat_flux'
        latitude_pattern = r'^(?P<indent>\s*)latitude'

        patterns = [t_profile_pattern, output_pattern, tau_pattern, heat_flux_pattern, latitude_pattern]
        new_strings = [f"file: {t_profile_file}", f"{output_file}:", 
                       f"constant_value: {case_specs['tx']}", f"constant_value: {case_specs['heat_flux']}", f"latitude: {case_specs['lat']}"]

        for pattern, string in zip(patterns, new_strings):
            edit_yaml(
                file=case_file,
                pattern=pattern,
                new_string=string
            )
        
        os.chdir(case_dir)  # TODO: more sophisticated handling of failed runs? maybe not necessary 
        os.system('gotm')

