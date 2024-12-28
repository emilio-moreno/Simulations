# %% Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as C
from typing import Callable, Optional, Tuple


# %% Fields
def dipole(X: np.ndarray, Y: np.ndarray, p= (0, 1), normal: bool = True):
    '''Returns an (optionally) unscaled dipole field.'''
    A = 1 / (4 * np.pi * C.epsilon_0)
    r_dot_p = p[0] * X + p[1] * Y
    r = np.sqrt(X**2 + Y**2)
    
    Ex = A * (3 * r_dot_p * X) - p[0] / r**3
    Ey = A * (3 * r_dot_p * Y) - p[1] / r**3
    
    if normal:
        E = np.sqrt(Ex**2 + Ey**2)
        Ex = Ex / E
        Ey = Ey / E
        
    
    return Ex, Ey, 1 / r


#%% Quiver
ndarray = np.ndarray
def Quiver(x: ndarray, y: ndarray,
           F: Callable[[ndarray, ndarray], Tuple[ndarray, ndarray, ndarray]],
           cmap : str = 'gist_earth') -> Optional[Tuple[plt.figure, plt.axis, plt.axis]]:
    '''
    Plots a normalized, colormapped quiver.
        
    Parameters
    ----------
    x: ndarray
        1D array for x positions.
    y: ndarray
        1D array for y positions.
    F: Callable
        A callable that takes meshgrids X, Y (from x, y) and returns the U, V
        of the vector field and a scaling meshgrid S.
    cmap: str
        Color bar format.
    
    
    Returns
    -------
    fig: plt.figure
        Figure object.
    ax: plt.axis
        Quiver axis.
        
    cbar_ax: plt.axis
        Colorbar axis.
    '''
    fig, ax = plt.subplots(dpi=300)
    
    X, Y = np.meshgrid(x, y)
    U, V, S = F(X, Y)
    
    field = ax.quiver(X, Y, U, V, S, pivot='mid', cmap=cmap)
    cbar = fig.colorbar(field)
    cbar.ax.set_ylabel('Strength')
    
    return fig, ax, cbar.ax



#%% Calls
# Dipole moment
p = (1, 1)
x = np.linspace(-3, 3, 20)
y = np.linspace(-3, 3, 20)
F = lambda X, Y: dipole(X, Y, p)

fig, ax, cbar = Quiver(x, y, F)
plt.show()


#%% Streamplot
x = np.array([0, 1, 2, 3])
y = np.array([0, 1, 2, 3])
u = np.array(x)
v = np.array(y)

im = ax.streamplot(X, Y, Ex, Ey)
plt.show()