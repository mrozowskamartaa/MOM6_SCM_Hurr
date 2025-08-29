import matplotlib.pyplot as plt
import cmocean
import numpy as np
import matplotlib as mpl

# Plotting functions

# Temp
def plot_stress(LES_time,LES_taux,LES_tauy,MOM_time,MOM_taux,MOM_tauy,title=''):
    f,ax=plt.subplots(1,2,figsize=(10,3))
    a=ax.ravel()[0]
    a.plot(LES_time,LES_taux*1000,'k-',label=r'LES $\tau_x$')
    a.plot(LES_time,LES_tauy*1000,'k--',label=r'LES $\tau_y$')
    a.plot(MOM_time,MOM_taux,'r-',label=r'MOM $\tau_x$')
    a.plot(MOM_time,MOM_tauy,'r--',label=r'MOM $\tau_y$')
    a.axhline(y=0,color='gray')
    a.set_ylim(-10.,10)
    a.set_xlim(1,2)
    a.set_ylabel(r'Surface $\vec{\tau}$ (m/s)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()
    
    a=ax.ravel()[1]
    a.plot(LES_time,np.sqrt((LES_taux*1000)**2+(LES_tauy*1000)**2),'k-',label=r'$\tau$')
    a.plot(MOM_time,np.sqrt(MOM_taux**2+MOM_tauy**2),'k--',label=r'MOM $\tau$')
    a.axhline(y=0,color='gray')
    a.set_ylim(-10.,10)
    a.set_xlim(1,2)
    a.set_ylabel(r'Surface $|\tau|$ (m/s)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()
    f.suptitle(title)
    f.tight_layout()
    
def CompT_surf(LES_temp,LES_time,MOM_temp,MOM_time,title=''):
    
    f,a=plt.subplots(1,1,figsize=(5,3))
    a.plot(LES_time,LES_temp,linewidth=2,color='k',linestyle='-',label='LES')
    a.plot(MOM_time,MOM_temp,'r',label='MOM')
    a.set_ylim(26,29.3)
    a.set_xlim(0,3)
    a.set_ylabel(r'Surface $\Theta$ ($^\circ C$)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()
    f.suptitle(title)
    f.tight_layout()

def CompT_prof(LES_temp,LES_z,MOM_temp,MOM_z,title=''):
    
    f,a=plt.subplots(1,1,figsize=(4,5))
    a.plot(LES_temp[:,0],LES_z,linewidth=2,color='k',linestyle='--')
    a.plot(LES_temp[:,-1],LES_z,linewidth=2,color='k',linestyle='-',label='LES')
    a.plot(MOM_temp[:,0],MOM_z,'r--')
    a.plot(MOM_temp[:,-1],MOM_z,'r',label='MOM')
    a.set_ylim(220,0)
    a.set_xlim(20,29.5)
    a.set_xlabel(r'$\Theta$ ($^\circ C$)',fontsize=12)
    a.set_ylabel(r'Depth [m]',fontsize=12)
    a.legend()
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

def Comp_M(LES_time,LES_M,MOM_time,MOM_M,title=''):
    f,a=plt.subplots(1,1,figsize=(10,3))
    a.plot(LES_time,LES_M,'k-')
    a.plot(MOM_time,MOM_M,'r-')
    a.set_xlim(0,3)
    a.set_ylabel(r'<wb>_{dz}',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.set_title(r'$<bw>_{dz}$ resolved (deg C m/s)',fontsize=12)
    f.suptitle(title)
    f.tight_layout()

def Comp_U_surf(LES_u,LES_v,LES_u_s,LES_v_s,LES_z,LES_time,MOM_u,MOM_v,MOM_u_s,MOM_v_s,MOM_z,MOM_time,title=''):
    f,ax=plt.subplots(1,3,figsize=(12,3))
    a=ax.ravel()[0]
    a.plot(LES_time,LES_u[0,:],linewidth=2,color='k',linestyle='-',label='LES u')
    a.plot(LES_time,LES_u_s[0,:],linewidth=2,color='k',linestyle='--',label='LES u Stokes')
    a.plot(MOM_time,MOM_u[0,:],linewidth=2,color='r',linestyle='-',label='MOM u')
    a.plot(MOM_time,MOM_u_s[0,:],linewidth=2,color='r',linestyle='--',label='MOM u Stokes')
    a.set_ylim(-2,2)
    a.set_xlim(0,3)
    a.set_ylabel(r'Surface $U$ (m/s)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()
    
    a=ax.ravel()[1]
    a.plot(LES_time,LES_v[0,:],linewidth=2,color='k',linestyle='-',label='LES')
    a.plot(LES_time,LES_v_s[0,:],linewidth=2,color='k',linestyle='--',label='LES Stokes')
    a.plot(MOM_time,MOM_v[0,:],linewidth=2,color='r',linestyle='-',label='MOM')
    a.plot(MOM_time,MOM_v_s[0,:],linewidth=2,color='r',linestyle='--',label='MOM Stokes')
    a.set_ylim(-2,2)
    a.set_xlim(0,3)
    a.set_ylabel(r'Surface $V$ (m/s)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()

    a=ax.ravel()[2]
    a.plot(LES_time,np.sqrt(LES_v[0,:]**2+LES_u[0,:]**2),linewidth=2,color='k',linestyle='-',label='LES')
    a.plot(LES_time,np.sqrt(LES_v_s[0,:]**2+LES_u_s[0,:]**2),linewidth=2,color='k',linestyle='--',label='LES stokes')
    a.plot(MOM_time,np.sqrt(MOM_v[0,:]**2+MOM_u[0,:]**2),linewidth=2,color='r',linestyle='-',label='MOM')
    a.plot(MOM_time,np.sqrt(MOM_v_s[0,:]**2+MOM_u_s[0,:]**2),linewidth=2,color='r',linestyle='--',label='MOM stokes')
    a.set_ylim(0,2)
    a.set_xlim(0,3)
    a.set_ylabel(r'Surface $|U+V|$ (m/s)',fontsize=12)
    a.set_xlabel(r'day',fontsize=12)
    a.legend()

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