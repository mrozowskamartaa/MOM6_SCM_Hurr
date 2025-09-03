from run_gotm_cases import run_gotm_cases


run_gotm_cases(
    root_dir="/gpfs/f5/gfdl_o/scratch/Marta.Mrozowska/hurricane_LES/MOM6_SCM_Hurr/analysis/compare_with_GOTM",
    source_dir_name="cases",
    forcing_dir_name="forcing",
    case_dict={('05', '46'): "TC021"}
)