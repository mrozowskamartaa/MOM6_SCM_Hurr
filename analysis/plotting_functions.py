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
        ax.legend(ncol=3)


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
        ax.set_xlim(1,2)
        ax.set_ylabel(r'<wb>_{dz}',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend()


    def plot_u_surf(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['u_surf'], linewidth=2, color=color, linestyle='-', label=r"{l} u".format(l=label))
            ax.plot(data['time'], data['u_s_surf'], linewidth=2, color=color, linestyle='--', label=r"{l} u_s".format(l=label))
        ax.set_ylim(-2.5,2.5)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $U$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend(ncol=3)

    
    def plot_v_surf(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], data['v_surf'], linewidth=2, color=color, linestyle='-', label=r"{l} v".format(l=label))
            ax.plot(data['time'], data['v_s_surf'], linewidth=2, color=color, linestyle='--', label=r"{l} v_s".format(l=label))
        ax.set_ylim(-2.5,2.5)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $V$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend(ncol=3)


    def plot_surf_vel_mag(
            self,
            ax: mpl.axes.Axes,
    ) -> None:
        for data, color, label in zip(self.data_list, self.color_list, self.label_list):
            ax.plot(data['time'], np.sqrt(data['u_surf']**2+data['v_surf']**2), linewidth=2, color=color, linestyle='-', label=r"{l} |U+V|".format(l=label))
            ax.plot(data['time'], np.sqrt(data['u_s_surf']**2+data['v_s_surf']**2), linewidth=2, color=color, linestyle='--', label=r"{l} |U+V|_s".format(l=label))
        ax.set_ylim(0,3)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Surface $|U+V|$ (m/s)',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.legend(ncol=3)


    def plot_vel(
            self,
            axes: mpl.axes.Axes,
    ) -> None:
        ax1, ax2, ax3 = axes

        self.plot_u_surf(ax1)
        self.plot_v_surf(ax2)
        self.plot_surf_vel_mag(ax3)

        ax1.get_legend().remove()
        ax3.get_legend().remove()


    def plot_wt_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-0.0045,0.0045,10)
        cmap = cmocean.cm.balance
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['zi'], self.data_list[i]['wt'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_T_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.arange(26,29.5,0.25)
        cmap = cmocean.cm.thermal
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], self.data_list[i]['temp'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_delta_T_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-1.9,1.9,20)
        cmap = cmocean.cm.balance
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], (self.data_list[i]['temp'].T - self.data_list[i]['temp'][:,0]).T,
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_u_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-1.95,1.95,40)
        cmap = cmocean.cm.balance
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], self.data_list[i]['u'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_v_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-1.95,1.95,40)
        cmap = cmocean.cm.balance
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], self.data_list[i]['v'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        ax.set_title(r'$V$ (m/s)',fontsize=12)
        plt.colorbar(C, ax=ax)

    
    def plot_u_s_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-0.45,0.45,10)
        cmap = plt.cm.PuOr
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], self.data_list[i]['u_s'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_v_s_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.linspace(-0.45,0.45,10)
        cmap = plt.cm.PuOr
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], self.data_list[i]['v_s'],
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)


    def plot_vel_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.arange(0,2,0.05)
        cmap = mpl.cm.Greens
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], np.sqrt(self.data_list[i]['u']**2 + self.data_list[i]['v']**2),
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)

    
    def plot_s_vel_hov(
            self,
            ax: mpl.axes.Axes,
            i: int
    ) -> None:
        levels = np.arange(0,0.5,0.025)
        cmap = mpl.cm.Purples
        cmap.set_bad('gray')
        C = ax.pcolormesh(self.data_list[i]['time'], self.data_list[i]['z'], np.sqrt(self.data_list[i]['u_s']**2 + self.data_list[i]['v_s']**2),
                          shading='nearest', norm = mpl.colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False), cmap=cmap)
        ax.set_ylim(220,0)
        ax.set_xlim(0,3)
        ax.set_ylabel(r'Depth [m]',fontsize=12)
        ax.set_xlabel(r'day',fontsize=12)
        plt.colorbar(C, ax=ax)
