#%% Imports
import numpy as np
from scipy.constants import epsilon_0
from typing import List
#from pprint import pprint

# %% Fields
def constant_field(X, Y, E0: List[float] = [0, 1], normal: bool = False):
    mag_E0 = np.sqrt(E0[0]**2 + E0[1]**2)
    if normal: mag_E0 = 1
    return E0[0] * np.ones(X.shape), E0[1] * np.ones(Y.shape), mag_E0
    

def dipole(X: np.ndarray, Y: np.ndarray,
           p: List[float] = [0, 1], normal: bool = True):
    '''Returns an (optionally) unscaled dipole field.'''
    A = 1 / (4 * np.pi * epsilon_0)
    r_dot_p = p[0] * X + p[1] * Y
    r = np.sqrt(X**2 + Y**2)
    
    Ex = (A / r**3) * ((3 * r_dot_p * X) - p[0])
    Ey = (A / r**3) * ((3 * r_dot_p * Y) - p[1])
    
    if normal:
        E = np.sqrt(Ex**2 + Ey**2)
        Ex = Ex / E
        Ey = Ey / E
    
    return Ex, Ey, E


def polarized_sphere(X: np.ndarray, Y: np.ndarray,
                     R: float = 1, P: List[float] = [0, 1],
                     normal: bool = True):
    '''Uniformly polarized sphere.'''
    p = (4 * np.pi / 3) * R**3 * np.array(P)
    Inside = lambda X, Y: np.sqrt(X**2 + Y**2) < R
    Inside = Inside(X, Y)
    Outside = (~Inside).astype(float)
    Inside = Inside.astype(float)
    
    E0 = constant_field(X, Y, E0=(-P[0], -P[1]), normal=normal)
    dip = dipole(X, Y, p, normal=normal)
    EInside = Inside * E0[0], Inside * E0[1], Inside * E0[2] 
    EOutside = Outside * dip[0], Outside * dip[1], Outside * dip[2] 
    Ex, Ey = EInside[0] + EOutside[0], EInside[1] + EOutside[1]
    S = EInside[2] + EOutside[2]
    
    return Ex, Ey, S


#%% main
def main():
    x = np.linspace(-3, 3, 20)
    y = np.linspace(-3, 3, 20)
    X, Y = np.meshgrid(x, y)

    polarized_sphere(X, Y)


#%% 呪い

if __name__ == '__main__':
    main()