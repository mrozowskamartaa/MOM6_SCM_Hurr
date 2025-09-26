from abc import ABC, abstractmethod
from typing import Any
import os

import xarray as xr
import numpy as np
import scipy.io as sio


def compute_M(
        wt: np.ndarray, 
        dz: float
) -> np.ndarray:
    alpha = -0.2
    grav = 9.81
    rho0 = 1027

    wb = -wt.T * alpha * grav / rho0
    wb[wb < 0] = 0
    return wb, np.sum(wb, axis=1) * dz


class DataRetriever(ABC):
    def __init__(self) -> None:
        self.data_namelist = [
            'time', 'z', 'zi', 'dz',
            'taux', 'tauy', 'temp', 'sst',
            'wt', 'wb', 'M', 
            'u_surf', 'v_surf',
            'u_s_surf', 'v_s_surf',
            'u', 'v',
            'u_s', 'v_s'
        ] 

    @abstractmethod
    def retreive_data(
            self,
            case_name: str,
            exp_name: str,
            case_dir: str
    ) -> dict[str, Any]:
        return ...
    

class LESDataRetriever(DataRetriever):
    def retreive_data(
            self,
            case_name: str,
            exp_name: str,
            case_dir: str
    ) -> dict[str, Any]:
        
        data_path = os.path.join(case_dir, f"{case_name}_PROF.mat")
        output = sio.loadmat(data_path)

        time = output['t'][:].squeeze() / 86400
        z = output['z'].T[:].squeeze()
        zi = output['z'].T[:].squeeze()
        dz = zi[2] - zi[1]

        taux = output['tau13l'][:][:,0] * 1000
        tauy = output['tau23l'][:][:,0] * 1000
        temp = (output['T'] - 273.15).T
        sst = temp[0]
        wt = (output['tw'][:]).T

        wb, M = compute_M(wt, dz)
        u, v = output['U'][:].T, output['V'][:].T
        u_surf, v_surf = u[0], v[0]
        u_s, v_s = output['Us'][:].T, output['Vs'][:].T
        u_s_surf, v_s_surf = u_s[0], v_s[0]

        data = [
            time, z, zi, dz, 
            taux, tauy, temp, sst, 
            wt, wb, M, 
            u_surf, v_surf,
            u_s_surf, v_s_surf,
            u, v, u_s, v_s]

        return {name: value for name, value in zip(self.data_namelist, data)}
    

class MOMDataRetriever(DataRetriever):
    def retreive_data(
            self,
            case_name: str,
            exp_name: str,
            case_dir: str
    ) -> dict[str, Any]:
        
        data_path = os.path.join(case_dir, exp_name, case_name)
        output = xr.open_dataset(data_path).isel(xh=0, yh=0, xq=0, yq=0)

        # The time axis can be cumbersome to work with, this is easier but relies on the MOM output being 15 minutes
        out_time = 900  # in seconds
        time = out_time / 86400 * (np.arange(output.Time.size) + 0.5)
        z = output.zl.values
        zi = output.zi.values
        dz = zi[2] - zi[1]

        taux = output.taux.values
        tauy = output.tauy.values
        temp = output.temp.values.T
        sst = temp[0]
        wt = output.Tflx_dia_diff.values.T

        wb, M = compute_M(wt, dz)
        u, v = output.u.values.T, output.v.values.T
        u_surf, v_surf = u[0], v[0]
        u_s, v_s = output.u.values.T*0, output.v.values.T*0  # No Stokes drift in these runs!
        u_s_surf, v_s_surf = u_s[0], v_s[0]

        data = [
            time, z, zi, dz, 
            taux, tauy, temp, sst, 
            wt, wb, M, 
            u_surf, v_surf,
            u_s_surf, v_s_surf,
            u, v, u_s, v_s]

        return {name: value for name, value in zip(self.data_namelist, data)}
    

class GOTMDataRetriever(DataRetriever):
    def retreive_data(
            self,
            case_name: str,
            exp_name: str,
            case_dir: str
    ) -> dict[str, Any]:
        
        data_path = os.path.join(case_dir, exp_name, f"{case_name}/output.nc")
        output = xr.open_dataset(data_path).isel(lat=0, lon=0)

        time = (output.time.values - output.time[0].values).astype(float) / 1e9 / 86400
        z = -output.z.isel(time=0).values
        zi = -output.zi.isel(time=0).values
        dz = zi[1] - zi[2]  # zi is negative

        taux = output.tx.values * 1000
        tauy = output.ty.values * 1000
        temp = output.temp_p.values.T
        sst = temp[-1]
        wt = (output.nuh.values[:,1:-1]*output.temp_p.diff(dim='z').values).T

        wb, M = compute_M(wt, dz)
        u, v = output.u.values.T, output.v.values.T
        u_surf, v_surf = output.u[:,-1].values, output.v[:,-1].values
        u_s, v_s = output.us.values.T, output.vs.values.T
        u_s_surf, v_s_surf = output.us[:,-1].values, output.vs[:,-1].values

        data = [
            time, z, zi, dz, 
            taux, tauy, temp, sst, 
            wt, wb, M, 
            u_surf, v_surf,
            u_s_surf, v_s_surf,
            u, v, u_s, v_s]

        return {name: value for name, value in zip(self.data_namelist, data)}
    

    
