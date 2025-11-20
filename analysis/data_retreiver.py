from abc import ABC, abstractmethod
from typing import Any
import os

import xarray as xr
import numpy as np
import scipy.io as sio


def compute_NRMSE(
        sample: np.ndarray,
        target: np.ndarray
) -> np.ndarray:
    return np.sqrt(np.nanmean((sample - target) ** 2)) / (np.nanmax(target) - np.nanmin(target))


def compute_NMAE(
        sample: np.ndarray,
        target: np.ndarray
) -> np.ndarray:
    return np.nanmean(np.abs(sample - target)) / (np.nanmax(target) - np.nanmin(target))


def compute_RMSE(
        sample: np.ndarray,
        target: np.ndarray
) -> np.ndarray:
    return np.sqrt(np.nanmean((sample - target)**2))


def interpolate_and_quantify_timeseries_difference(
        sample_data_dict: dict,
        target_data_dict: dict,
        variable: str,
        method: str = "NRMSE",
        mask: bool = False,
        threshold: float = 0.00001
) -> float:
    sample_time, sample_data = sample_data_dict['time'], sample_data_dict[variable]
    target_time, target_data = target_data_dict['time'], target_data_dict[variable]
    new_time = np.linspace(target_time[0], target_time[-1], 1000)
    sample_data_interp = np.interp(new_time, sample_time, sample_data)
    target_data_interp = np.interp(new_time, target_time, target_data)

    if mask:
        criterion = np.logical_or(target_data_interp > threshold, sample_data_interp > threshold)
        data_mask = np.where(criterion)
        sample, target = sample_data_interp[data_mask], target_data_interp[data_mask]
    else:
        sample, target = sample_data_interp, target_data_interp

    if method == "NRMSE":
        diff = compute_NRMSE(
            sample=sample,
            target=target
        )
    elif method == "NMAE":
        diff = compute_NMAE(
            sample=sample,
            target=target
        )
    elif method == "RMSE":
        diff = compute_RMSE(
            sample=sample,
            target=target
        )
    else:
        raise ValueError("method should be 'NRMSE', 'NMAE' or 'RMSE'.")

    return diff


# TODO: Allow for dz: Union[float, np.ndarray]
"""
def compute_M(
        wt: np.ndarray, 
        dz: float
) -> tuple[np.ndarray, np.ndarray]:
    alpha = -0.2
    grav = 9.81
    rho0 = 1027

    wb = -wt.T * alpha * grav / rho0
    wb[wb < 0] = 0
    return wb, np.sum(wb, axis=1) * dz
"""


def compute_M(
        wt: np.ndarray, 
        dz: float
) -> tuple[np.ndarray, np.ndarray]:
    alpha = -2.e-4
    grav = 9.81
    rho0 = 1027

    wb = -wt.T * alpha * grav
    wb[wb < 0] = 0
    return wb, np.sum(wb, axis=1) * dz


def find_nearest(
        z: np.ndarray,
        depth: float
) -> int:
    z_above = np.where(z <= depth, z, np.nan)
    z_nearest = np.nanmax(z_above)
    return np.where(z == z_nearest)[0][0]


def compute_mld(
        temp: np.ndarray,
        z: np.ndarray,
        depth: float = 10.,
        threshold: float = 0.2
) -> np.ndarray:
    z_index = find_nearest(
        z=z,
        depth=depth
    )
    temp_10_m = temp[z_index]
    temp_mld = temp_10_m - threshold
    z_2D = z[:,np.newaxis]

    z_above = np.nanmax(np.where(temp > temp_mld[np.newaxis,:], z_2D, np.nan), axis=0)
    z_below = np.nanmin(np.where(temp < temp_mld[np.newaxis,:], z_2D, np.nan), axis=0)

    temp_above = temp[z_2D==z_above[np.newaxis,:]]
    temp_below = temp[z_2D==z_below[np.newaxis,:]]

    return z_above + (temp_below - temp_above) * (temp_mld - temp_above) / (z_below - z_above)


class DataRetriever(ABC):
    def __init__(
            self,
            case_name: str,
            exp_name: str,
            case_dir: str
    ) -> None:

        self.data_namelist = [
            'time', 'z', 'zi', 'dz',
            'taux', 'tauy', 'temp', 'sst', 'mld',
            'wt', 'wb', 'M', 
            'u_surf', 'v_surf',
            'u_s_surf', 'v_s_surf',
            'u', 'v',
            'u_s', 'v_s'
        ]

        self.case_name = case_name
        self.exp_name = exp_name
        self.case_dir = case_dir

        self._output = self.get_output()

    @property
    @abstractmethod
    def data_path(self) -> str:
        return ...

    @abstractmethod
    def get_output(self) -> Any:
        return ...

    @property
    def output(self) -> Any:
        return self._output

    @property
    @abstractmethod
    def surface_index(self) -> int:
        return ...
    
    @property
    @abstractmethod
    def reference_depth_for_mld_calculation() -> float:
        return ...
    
    @abstractmethod
    def get_dims(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        return ...

    @abstractmethod
    def get_wind_stress(self) -> tuple[np.ndarray, np.ndarray]:
        return ...

    @abstractmethod
    def get_tracers(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        return ...
    
    @abstractmethod
    def get_M(
        self,
        wt: np.ndarray,
        dz: float
    ) -> tuple[np.ndarray, np.ndarray]:
        return ...

    @abstractmethod
    def get_currents(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        return ...

    def retreive_data(self) -> dict[str, Any]:
        time, z, zi, dz = self.get_dims()

        taux, tauy = self.get_wind_stress()
        temp, wt = self.get_tracers()
        sst = temp[self.surface_index]
        mld = compute_mld(
            temp=temp,
            z=z,
            depth=self.reference_depth_for_mld_calculation
        )

        wb, M = self.get_M(wt=wt, dz=dz)

        u, v, u_s, v_s = self.get_currents()
        u_surf, v_surf = u[self.surface_index], v[self.surface_index]
        u_s_surf, v_s_surf = u_s[self.surface_index], v_s[self.surface_index]

        data = [
            time, z, zi, dz, 
            taux, tauy, temp, sst, mld,
            wt, wb, M, 
            u_surf, v_surf,
            u_s_surf, v_s_surf,
            u, v, u_s, v_s]

        return {name: value for name, value in zip(self.data_namelist, data)}
    

class LESDataRetriever(DataRetriever):
    @property
    def data_path(self) -> str:
        return os.path.join(self.case_dir, f"{self.case_name}_PROF.mat")

    def get_output(self) -> Any:
        return sio.loadmat(self.data_path)

    @property
    def surface_index(self) -> int:
        return 0
    
    @property
    def reference_depth_for_mld_calculation(self) -> float:
        return 10.

    def get_dims(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        time = self.output['t'][:].squeeze() / 86400
        z = self.output['z'].T[:].squeeze()
        zi = self.output['z'].T[:].squeeze()
        dz = zi[2] - zi[1]
        return time, z, zi, dz

    def get_wind_stress(self) -> tuple[np.ndarray, np.ndarray]:
        taux = self.output['tau13l'][:][:,0] * 1000
        tauy = self.output['tau23l'][:][:,0] * 1000
        return taux, tauy

    def get_tracers(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        temp = (self.output['T'] - 273.15).T
        wt = (self.output['tw'][:]).T
        return temp, wt
    
    def get_M(
            self,
            wt: np.ndarray,
            dz: float
    ) -> tuple[np.ndarray, np.ndarray]:
        return compute_M(wt=wt, dz=dz)

    def get_currents(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        u, v = self.output['U'][:].T, self.output['V'][:].T
        u_s, v_s = self.output['Us'][:].T, self.output['Vs'][:].T
        return u, v, u_s, v_s
    

class MOMDataRetriever(DataRetriever):
    @property
    def data_path(self) -> str:
        return os.path.join(self.case_dir, self.exp_name, self.case_name)

    def get_output(self) -> Any:
        return xr.open_dataset(self.data_path).isel(xh=0, yh=0, xq=0, yq=0)

    @property
    def surface_index(self) -> int:
        return 0
    
    @property
    def reference_depth_for_mld_calculation(self) -> int:
        return 9.75

    def get_dims(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        out_time = 900  # in seconds
        time = out_time / 86400 * (np.arange(self.output.Time.size) + 0.5)
        z = self.output.zl.values
        zi = self.output.zi.values
        dz = zi[2] - zi[1]
        return time, z, zi, dz

    def get_wind_stress(self) -> tuple[np.ndarray, np.ndarray]:
        taux = self.output.taux.values
        tauy = self.output.tauy.values
        return taux, tauy

    def get_tracers(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        temp = self.output.temp.values.T
        wt = self.output.Tflx_dia_diff.values.T
        return temp, wt

    def get_M(
            self,
            wt: np.ndarray,
            dz: float
    ) -> tuple[np.ndarray, np.ndarray]:
        return compute_M(wt=wt, dz=dz)

    def get_currents(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        u, v = self.output.u.values.T, self.output.v.values.T
        u_s, v_s = self.output.u.values.T*0, self.output.v.values.T*0  # No Stokes drift in these runs!
        return u, v, u_s, v_s
    

class GOTMDataRetriever(DataRetriever):
    @property
    def data_path(self) -> str:
        return os.path.join(self.case_dir, self.exp_name, f"{self.case_name}/output.nc")

    def get_output(self) -> Any:
        return xr.open_dataset(self.data_path).isel(lat=0, lon=0)

    @property
    def surface_index(self) -> int:
        return -1
    
    @property
    def reference_depth_for_mld_calculation(self) -> float:
        return 9.5

    def get_dims(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        time = (self.output.time.values - self.output.time[0].values).astype(float) / 1e9 / 86400
        z = -self.output.z.isel(time=0).values
        zi = -self.output.zi.isel(time=0).values
        dz = zi[1] - zi[2]  # z-axis increases from -z_bot to -z_surf in GOTM
        return time, z, zi, dz

    def get_wind_stress(self) -> tuple[np.ndarray, np.ndarray]:
        taux = self.output.tx.values * 1000
        tauy = self.output.ty.values * 1000
        return taux, tauy
    
    # def get_M(
    #         self,
    #         wt: np.ndarray,
    #         dz: float
    # ) -> tuple[np.ndarray, np.ndarray]:
    #     return compute_M(wt=wt, dz=dz)
    
    def get_M(
            self,
            wt: np.ndarray,
            dz: float
    ) -> tuple[np.ndarray, np.ndarray]:
        wb = -self.output.G.values
        wb[wb < 0] = 0
        M = np.sum(wb, axis=1) * dz
        return wb, M

    # TODO: more robust wt computation which does not assume dz=1!
    def get_tracers(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        temp = self.output.temp_p.values.T
        wt = (self.output.nuh.values*self.output.temp_p.pad(z=(1), mode="edge").diff(dim='z').values).T
        return temp, wt

    def get_currents(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        u, v = self.output.u.values.T, self.output.v.values.T
        u_s, v_s = self.output.us.values.T, self.output.vs.values.T
        return u, v, u_s, v_s
