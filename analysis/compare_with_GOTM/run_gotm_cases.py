import os
import shutil
import re


def edit_yaml(
        file: str,
        pattern: str,
        new_string: str
) -> None:
    
    with open(file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    compiled_pattern = re.compile(pattern)

    for line in lines:
        match = compiled_pattern.match(line)

        if match:
            indent = match.group('indent')
            new_line = (f"{indent}{new_string}\n")
            new_lines.append(new_line)
            continue
    
        new_lines.append(line)

    with open(file, 'w') as f:
        f.writelines(new_lines)


def run_gotm_cases(
        root_dir: str, 
        source_dir_name: str,
        forcing_dir_name: str, 
        case_dict: dict
    ) -> None:

    source_file = os.path.join(root_dir, source_dir_name, "gotm.yaml")
    forcing_dir = os.path.join(root_dir, forcing_dir_name)

    for case_no, case_name in case_dict.items():
        case_dir = os.path.join(root_dir, "cases", case_name)
        case_file = os.path.join(root_dir, case_dir, "gotm.yaml")
        wind_mag, loc = case_no  # this could probably be better, like if we streamlined how the cases are named and categorized across the 3 models??? yfm
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


        
