from abc import ABC, abstractmethod
from typing import Callable
import os

import xarray as xr
import numpy as np
import scipy.io as sio


class FeatureRetreiver:
    def __init__(
            self,
            training_set_dir: str,
            case_dict: dict,
            dz: float = 1
    ) -> None:

        self.alpha = -0.2
        self.grav = 9.81
        self.rho0 = 1027
        self.dz = dz

        self.training_set_dir = training_set_dir
        self.case_dict = case_dict

        first_case = next(iter(case_dict.keys()))
        self.first_case_output = self.get_output(first_case)


    def get_output(
            self,
            case: str
    ) -> xr.Dataset:

        output_file = os.path.join(self.training_set_dir, case, "output.nc")
        return xr.open_dataset(output_file).isel(lat=0, lon=0)
    

    def compute_u_star(
            self,
            case: str
    ) -> float:
        return (self.case_dict[case]['tx'] / self.rho0) ** 0.5
    

    def compute_M(
            self,
            wt: np.ndarray
    ) -> np.ndarray:

        wb = -wt.T * self.alpha * self.grav / self.rho0
        wb[wb < 0] = 0
        return np.sum(wb, axis=1) * self.dz


    def compute_wt(
            self,
            output: xr.Dataset
    ) -> np.ndarray:
        return (output['nuh'].values * output['temp_p'].pad(z=(1), mode="edge").diff(dim='z').values).T / self.dz


    def make_coords_dict(
            self,
            coords: list[str]
    ) -> dict:
        
        coords_dict = {}
        
        for coord in coords:
            if 'z' in coord:
                coords_dict[coord] = self.first_case_output[coord].isel(time=0).values
            else:
                coords_dict[coord] = self.first_case_output[coord].values

        return coords_dict
    

    def make_m_star_dataset(self) -> xr.Dataset:

        coords = {'time': self.first_case_output['time'].values}
        
        data_vars = {}
        for case in self.case_dict.keys():
            var_name = f"m_star_{case}"
            output = self.get_output(case)
            wt = self.compute_wt(output=output)
            M = self.compute_M(wt=wt)
            m_star = M / self.compute_u_star(case=case) ** 3
            data_vars[var_name] = xr.DataArray(
                m_star,
                dims=['time'],
                coords=coords
            )

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )


    def make_dataset_from_processed_data(
            self,
            processing_method: Callable[[xr.Dataset, str], np.ndarray],
            processing_method_name: str,
            variable: str,
            coordinates: list[str]
    ) -> xr.Dataset:
        
        coords = self.make_coords_dict(coords=coordinates)

        data_vars = {}
        for case in self.case_dict.keys():
            var_name = f"{processing_method_name}_{case}"
            output = self.get_output(case)
            array = processing_method(
                output=output, 
                variable=variable
            )
            data_vars[var_name] = xr.DataArray(
                array,
                dims=coordinates,
                coords=coords
            )

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )


    def make_dataset_from_raw_data(
            self,
            variable: str,
            coordinates: list[str]
    ) -> xr.Dataset:
        
        coords = self.make_coords_dict(coords=coordinates)

        data_vars = {}
        for case in self.case_dict.keys():
            var_name = f"{variable}_{case}"
            output = self.get_output(case)
            array = output[variable].values
            data_vars[var_name] = xr.DataArray(
                array,
                dims=coordinates,
                coords=coords
            )

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )
