import matplotlib.pyplot as plt
import cmocean
import numpy as np
import matplotlib as mpl

# Plotting functions


class Plotter:
    def __init__(
            self,
            data_list: list[dict],
            color_list: list[str],
            label_list: list[str]):
        
        self.data_list = data_list
        self.color_list = color_list
        self.label_list = label_list


    def plot_stress_xy(
            self,
            ax: mpl.axes.Axes
    ) -> None:

        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['taux'], color=color, label=r"{l} $\tau_x$".format(l=label))
            ax.plot(data['time'], data['tauy'], color=color, label=r"{l} $\tau_y$".format(l=label), linestyle='--')
        ax.axhline(y=0,color='gray')
        ax.set_ylim(-12.,12)
        ax.set_xlim(1,2)
        ax.set_ylabel(r'Surface $\vec{\tau}$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend(ncol=len(self.data_list))


    def plot_stress_mag(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'],np.sqrt(data['taux']**2+data['tauy']**2), color=color, label=label)
        ax.set_ylim(0.,15)
        ax.set_xlim(1,2)
        ax.set_ylabel(r'Surface $|\tau|$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_stress(
            self,
            axes: mpl.axes.Axes,
    ) -> None:
        ax1, ax2 = axes

        self.plot_stress_xy(ax1)
        self.plot_stress_mag(ax2)


    def plot_T_surf(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['sst'], color=color, label=label)
        ax.set_ylim(27,29.3)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $\Theta$ ($^\circ C$)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_T_prof(
            self,
            ax: mpl.axes.Axes
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['temp'][:,0], data['z'], linewidth=2, color=color, linestyle='--')
            ax.plot(data['temp'][:,-1], data['z'], linewidth=2, color=color, linestyle='-', label=label)
        ax.set_ylim(220,0)
        ax.set_xlim(20,29.5)
        ax.set_xlabel(r'$\Theta$ ($^\circ C$)',fontsize=12)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.legend()


    def plot_M(
            self,
            ax: mpl.axes.Axes
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['M'], color=color, label=label)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'<wb>_{dz}',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_u_surf(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['u_surf'], linewidth=2, color=color, linestyle='-', label=r"{l} u".format(l=label))
            ax.plot(data['time'], data['u_s_surf'], linewidth=2, color=color, linestyle='--', label=r"{l} u Stokes".format(l=label))
        ax.set_ylim(-2,2)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $U$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()

    
    def plot_v_surf(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['v_surf'], linewidth=2, color=color, linestyle='-', label=r"{l} v".format(l=label))
            ax.plot(data['time'], data['v_s_surf'], linewidth=2, color=color, linestyle='--', label=r"{l} v Stokes".format(l=label))
        ax.set_ylim(-2,2)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $V$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_surf_vel_mag(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], np.sqrt(data['u_surf']**2+data['v_surf']**2), linewidth=2, color=color, linestyle='-', label=r"{l} |U+V|".format(l=label))
            ax.plot(data['time'], np.sqrt(data['u_s_surf']**2+data['v_s_surf']**2), linewidth=2, color=color, linestyle='--', label=r"{l} |U+V| Stokes".format(l=label))
        ax.set_ylim(0,2)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $|U+V|$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_vel(
            self,
            axes: mpl.axes.Axes,
    ) -> None:
        ax1, ax2, ax3 = axes

        self.plot_u_surf(ax1)
        self.plot_v_surf(ax2)
        self.plot_surf_vel_mag(ax3)


def Comp_wt(LES_wt,LES_z,LES_time,MOM_wt,MOM_z,MOM_time,title=''):
    f,ax=plt.subplots(2,1,figsize=(10,5))
    levels=np.linspace(-0.0045,0.0045,10)
    cmap=cmocean.cm.balance
    cmap.set_bad('gray')
    a=ax.ravel()[0]
    cmap=cmocean.cm.balance
    cmap.set_bad('gray')
    C=a.pcolormesh(LES_time,LES_z,LES_wt,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$<tw>$ resolved (deg C m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    a=ax.ravel()[1]
    C=a.pcolormesh(MOM_time,MOM_z,MOM_wt,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(200,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$\Theta-\Theta_i$ ($^\circ C$)',fontsize=12)
    plt.colorbar(C,ax=a)
    f.suptitle(title)
    f.tight_layout()


def CompT_Hov(LES_temp,LES_z,LES_time,MOM_temp,MOM_z,MOM_time,title=''):
    f,ax=plt.subplots(2,1,figsize=(10,5))
    levels=np.arange(26,29.5,0.25)
    cmap=cmocean.cm.thermal
    cmap.set_bad('gray')
    a=ax.ravel()[0]
    C=a.pcolormesh(LES_time,LES_z,LES_temp,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'LES $\Theta$ ($^\circ C$)',fontsize=12)
    plt.colorbar(C,ax=a)
    a=ax.ravel()[1]
    C=a.pcolormesh(MOM_time,MOM_z,MOM_temp,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(200,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'MOM $\Theta$ ($^\circ C$)',fontsize=12)
    plt.colorbar(C,ax=a)
    f.suptitle(title)
    f.tight_layout()


def CompDeltaT_Hov(LES_temp,LES_z,LES_time,MOM_temp,MOM_z,MOM_time,title=''):
    f,ax=plt.subplots(2,1,figsize=(10,5))
    levels=np.linspace(-1.9,1.9,20)
    cmap=cmocean.cm.balance
    cmap.set_bad('gray')
    a=ax.ravel()[0]
    C=a.pcolormesh(LES_time,LES_z,(LES_temp.T-LES_temp[:,0]).T,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(200,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$\Theta-\Theta_i$ ($^\circ C$)',fontsize=12)
    plt.colorbar(C,ax=a)
    a=ax.ravel()[1]
    C=a.pcolormesh(MOM_time,MOM_z,(MOM_temp.T-MOM_temp[:,0]).T,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(200,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$\Theta-\Theta_i$ ($^\circ C$)',fontsize=12)
    plt.colorbar(C,ax=a)
    f.suptitle(title)
    f.tight_layout()


#Currents


def Comp_U(LES_u,LES_v,LES_u_s,LES_v_s,LES_z,LES_time,MOM_u,MOM_v,MOM_u_s,MOM_v_s,MOM_z,MOM_time,title=''):
    
    
    f,ax=plt.subplots(3,3,figsize=(12,8))
    
    levels=np.linspace(-1.95,1.95,40)
    cmap=cmocean.cm.balance
    cmap.set_bad('gray')
    
    a=ax.ravel()[0]
    C=a.pcolormesh(LES_time,LES_z,LES_u,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$U$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    a=ax.ravel()[1]
    C=a.pcolormesh(MOM_time,MOM_z,MOM_u,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'MOM $U$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    a=ax.ravel()[3]
    C=a.pcolormesh(LES_time,LES_z,LES_v,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$V$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    a=ax.ravel()[4]
    C=a.pcolormesh(MOM_time,MOM_z,MOM_v,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'MOM $V$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    levels=np.linspace(-.45,.45,10)
    cmap=plt.cm.PuOr
    cmap.set_bad('gray')
    
    a=ax.ravel()[2]
    C=a.pcolormesh(LES_time,LES_z,LES_u_s,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$U_S$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    a=ax.ravel()[5]
    C=a.pcolormesh(LES_time,LES_z,LES_v_s,shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$V_S$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    levels=np.arange(0,2,0.05)
    cmap=mpl.cm.Greens
    cmap.set_bad('gray')
    
    a=ax.ravel()[6]
    C=a.pcolormesh(LES_time,LES_z,np.sqrt(LES_u**2+LES_v**2),shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'LES $(U^2+V^2)^{1/2}$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    a=ax.ravel()[7]
    C=a.pcolormesh(MOM_time,MOM_z,np.sqrt(MOM_u**2+MOM_v**2),shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'MOM $(U^2+V^2)^{1/2}$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)
    
    
    levels=np.arange(0,0.5,0.025)
    cmap=mpl.cm.Purples
    cmap.set_bad('gray')
    
    a=ax.ravel()[8]
    C=a.pcolormesh(LES_time,LES_z,np.sqrt(LES_u_s**2+LES_v_s**2),shading='nearest',norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False),cmap=cmap)
    a.set_ylim(220,0)
    a.set_xlim(0,3)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$(U_S^2+V_S^2)^{1/2}$ (m/s)',fontsize=12)
    plt.colorbar(C,ax=a)

    f.suptitle(title)
    f.tight_layout()
    
    pass;