# %% Imports
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Optional, Tuple

'''
Functions implemented within this code can be imported to a new Python file
and run without any further importing. However, if you'd like to run main()
from this .py you'll need to import the MiniPys from:
github.com/emilio-moreno/MiniPys
'''

minipy_formatter_path = r'C:\Users\Laevateinn\Documents\GitHub' \
                         r'\MiniPys\Formatter'


#%% Quiver
ndarray = np.ndarray
F_type = Callable[[ndarray, ndarray], Tuple[ndarray, ndarray, ndarray]]
return_type = Optional[Tuple[plt.figure, plt.axis, plt.axis]]
def Quiver(x: ndarray, y: ndarray, F: F_type,
           cmap : str = 'plasma', fig=None, ax=None) -> return_type:
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
    if not fig:
        fig, ax = plt.subplots(dpi=300)
    
    X, Y = np.meshgrid(x, y)
    U, V, S = F(X, Y)
    
    field = ax.quiver(X, Y, U, V, S, pivot='mid', cmap=cmap)
    cbar = fig.colorbar(field)
    cbar.ax.set_ylabel('Strength')
    
    return fig, ax, cbar.ax


#%% main()
def main():    
    # Dipole moment
    import sys
    import os
    from fields import dipole, constant_field, polarized_sphere
    sys.path.insert(0, minipy_formatter_path)
    import minipy_formatter as MF
    
    
    #CMU = r"C:\Users\Laevateinn\AppData\Local\Microsoft\Windows\Fonts"
    #CMU += "\cmunrm.ttf"
    MF.Format(font_paths=[]).rcUpdate(font_size=12)
    plt.style.use('dark_background')

    fig, ax = plt.subplots(dpi=300)

    # Field parameters
    P = [-1, 1]
    R = 1.5

    # Plots
    z = np.linspace(-R, R, 100)
    x = np.linspace(-3, 3, 30)
    y = np.linspace(-3, 3, 30)
    F = lambda X, Y: polarized_sphere(X, Y, P=P, R=R)
    upper_circle = np.sqrt(R**2 - z**2)

    ax.plot(z, upper_circle, color='white')
    ax.plot(z, -upper_circle, color='white')
    
    fig, ax, cbar_ax = Quiver(x, y, F, fig=fig, ax=ax)
    title = f'Uniformly polarized sphere | $\\mathbf{{P}} = {P}$, $R = {R}$'
    ax.set(title=title, xlabel='x', ylabel='y')
    cbar_ax.set(ylabel='Field strength (E)')
    
    plt.tight_layout()
    figs_dir = './Figures/'
    filename = 'Uniformly polarized sphere.png'
    path = os.path.join(figs_dir, filename)
    
    overwrite = False
    if os.path.isfile(path) and not overwrite:
        raise FileExistsError(f"File {path} already exists!")
    
    plt.savefig(path)

#%% 呪い
if __name__ == '__main__':
    main()
