from abc import ABC, abstractmethod
from typing import Callable
import os

import xarray as xr
import numpy as np
import scipy.io as sio


def compute_buoyancy_mixing_term(output: xr.Dataset) -> np.ndarray:
    return (output['nuh']*output['NN'].where(output['NN'] > 0)).sum(dim="zi").values


def compute_bl(
        output: xr.Dataset,
        variable: str = "eps"
) -> np.ndarray:
    bl_mask = np.where(output[variable].values > 1e-12, -output['zi'].values, np.nan)
    bl = np.nanmax(bl_mask, axis=1)
    return bl
    

def compute_bl_rh18(
        output: xr.Dataset,
        variable: str = "nuh"
) -> np.ndarray:
    bl_mask = np.where(output[variable].values > 1e-6, -output['zi'].values, np.nan)
    bl = np.nanmax(bl_mask, axis=1)
    bl = np.where(np.isnan(bl), 1.0, bl)
    return bl


class FeatureRetreiver:
    def __init__(
            self,
            training_set_dir: str,
            case_dict: dict,
            dz: int = 1,
            dt: int = 3600
    ) -> None:

        self.alpha = -0.2
        self.grav = 9.81
        self.rho0 = 1027
        self.dz = dz
        self.dt = dt

        self.training_set_dir = training_set_dir
        self.case_dict = case_dict
        self.case_names = [key for key in case_dict.keys()]

        first_case = self.case_names[0]
        self.first_case_output = self.get_output(first_case)

        self.time = self.first_case_output['time'].values


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
    

    def calculate_storage_term(
            self,
            output: xr.Dataset
    ) -> np.ndarray:
        return np.pad((output['tke'].diff(dim="time") / self.dt).sum(dim="zi").values, pad_width=(0,1), mode="edge")


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

        coords_dict['case'] = self.case_names

        return coords_dict
    

    def make_m_star_dataset(self) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }

        # TODO: It would have been better to make case dict have int as keys and then 
        # construct the case names based on those.
        # Consider this edit in future generation of training datasets.
        
        m_star = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            # wt = self.compute_wt(output=output)
            # M = self.compute_M(wt=wt)
            wb = -output.G.values
            wb[wb < 0] = 0
            M = np.sum(wb, axis=1) * self.dz
            m_star[i] = M / self.compute_u_star(case=case) ** 3
        
        data_vars = {"m_star": xr.DataArray(
            m_star,
            dims=['case', 'time'],
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )
    

    def make_M_dataset(self) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }

        M = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            wb = -output.G.values
            wb[wb < 0] = 0
            M[i] = np.sum(wb, axis=1) * self.dz
        
        data_vars = {"M": xr.DataArray(
            M,
            dims=['case', 'time'],
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )
    
    
    def make_var_at_bl_dataset(
        self,
        variable: str,
        index_above_bl: int = 2
    ) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }
        
        array = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            t, z = output[variable].shape
            z_grid = np.arange(z)[::-1]
            if z == 400:
                z_mask = np.where(output['nuh'].values[:,:-1] > 1e-6, z_grid, np.nan)
            elif z == 401:
                z_mask = np.where(output['nuh'].values > 1e-6, z_grid, np.nan)
            z_indices = np.nanmax(z_mask, axis=1)
            z_indices = np.where(np.isnan(z_indices), 1, z_indices).astype(int)
            array[i] = output[variable].values[np.arange(t),-z_indices+index_above_bl]
        
        data_vars = {f"{variable}_bl": xr.DataArray(
            array,
            dims=['case', 'time'],
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )

    
    def make_var_across_bl_dataset(
        self,
        variable: str,
        index_above_bl: int = 2,
        index_below_bl: int = 2
    ) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }
        
        array = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            t, z = output[variable].shape
            z_grid = np.arange(z)[::-1]
            if z == 400:
                z_mask = np.where(output['nuh'].values[:,:-1] > 1e-6, z_grid, np.nan)
            elif z == 401:
                z_mask = np.where(output['nuh'].values > 1e-6, z_grid, np.nan)
            z_indices = np.nanmax(z_mask, axis=1)
            z_indices = np.where(np.isnan(z_indices), 1, z_indices).astype(int)
            val_1 = output[variable].values[np.arange(t),-z_indices+index_above_bl]
            val_2 = output[variable].values[np.arange(t),-z_indices-index_below_bl]
            array[i] = (val_1 + val_2) / (index_above_bl + index_below_bl)
        
        data_vars = {f"{variable}_bl_mean": xr.DataArray(
            array,
            dims=['case', 'time'],
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )
    

    def make_buoyancy_mixing_term_dataset(self) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }
        
        buoyancy_mixing_term = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            buoyancy_mixing_term[i] = compute_buoyancy_mixing_term(output=output)
        
        data_vars = {"buoyancy_mixing_term": xr.DataArray(
            buoyancy_mixing_term,
            dims=['case', 'time'],
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )


    def make_storage_term_dataset(self) -> xr.Dataset:

        coords = {
            'case': self.case_names,
            'time': self.time
        }
        
        storage_term = np.empty((len(self.case_names), len(self.time)))

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            storage_term[i] = self.calculate_storage_term(output=output)
        
        data_vars = {"storage_term": xr.DataArray(
            storage_term,
            dims=['case', 'time'],
            coords=coords
        )}

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
        coordinates = ['case'] + coordinates

        test_array = processing_method(
            output=self.first_case_output,
            variable=variable
        )

        array = np.empty((len(self.case_names),) + test_array.shape)

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            array[i] = processing_method(
                output=output, 
                variable=variable
            )
        
        data_vars = {f"{processing_method_name}" : xr.DataArray(
            array,
            dims=coordinates,
            coords=coords
        )}

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
        coordinates = ['case'] + coordinates

        array = np.empty((len(self.case_names),) + self.first_case_output[variable].shape)

        for i, case in enumerate(self.case_dict.keys()):
            output = self.get_output(case)
            array[i] = output[variable].values
        
        data_vars = {variable : xr.DataArray(
            array,
            dims=coordinates,
            coords=coords
        )}

        return xr.Dataset(
            data_vars=data_vars,
            coords=coords
        )
