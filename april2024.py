import numpy as np
from scipy.integrate import quad, dblquad, tplquad, nquad
from scipy.optimize import fmin, root
from scipy.misc import derivative
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter, ListedColormap
from pprint import pprint

def P_extra(e):
    i1 = (e / 2)**2
    
    f = lambda r: 2 / np.pi * r * np.arccos(np.sqrt(2 * e * r - e**2) / r)
    a = e / 2
    b = 1
    i2 = quad(f, a, b, epsabs=1e-12, epsrel=1e-12)
    return i1 + i2[0], i2

def P(e):
    return P_extra(e)[0]

def P2(e):
    i1 = (e / 2)**2
    
    f = lambda r: 2 / np.pi * r * np.arcsin(np.abs(r - e) / r)
    a = e / 2
    b = 1
    i2 = quad(f, a, b, epsabs=1e-12, epsrel=1e-12)
    return i1 + i2[0]

# this doesn't work
def P3(e):
    i1 = (e / 2)**2
    
    f1 = lambda r: 1 / (3 * np.pi) * (np.sqrt(e) * (r + e) * np.sqrt(2 * r - e) - 3 * r**2 * np.arcsin((r - e) / r)) # valid up to r = e
    f2 = lambda r: -f1(r) # valid past r = e
    
    f3 = lambda r: abs(f1(r))
    
    return i1 + f3(1) - f3(e / 2)
    
def Pgrid(e):
    accuracy = 300
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    R = np.sqrt(XX**2 + YY**2)
    A = np.zeros_like(XX)
    A[R > e / 2] = np.sqrt(2 * e * R[R > e / 2] - e**2)

    ZZ = np.zeros_like(XX)
    #Th = np.arctan2(YY, XX)
    ZZ[R > 1] = -1
    ZZ[ZZ == 0] = (A[ZZ == 0] - XX[ZZ == 0])**2 + YY[ZZ == 0]**2 <= (e - R[ZZ == 0])**2
    
    return np.sum(ZZ > 0) / np.sum(ZZ >= 0)


def PgridRand(e):
    accuracy = 300
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    R = np.sqrt(XX**2 + YY**2)
    A = np.zeros_like(XX)
    A[R > e / 2] = np.sqrt(2 * e * R[R > e / 2] - e**2)
    #Th = np.arctan2(YY, XX)
    Th2 = np.random.rand(XX.shape[0], XX.shape[1]) * 2 * np.pi
    ZZ = np.zeros_like(XX)
    ZZ[R > 1] = -1
    ZZ[ZZ == 0] = (A[ZZ == 0] * np.cos(Th2[ZZ == 0]) - XX[ZZ == 0])**2 + (A[ZZ == 0] * np.sin(Th2[ZZ == 0]) - YY[ZZ == 0])**2 <= (e - R[ZZ == 0])**2
    return np.sum(ZZ > 0) / np.sum(ZZ >= 0)

def boundsGraph(e, fig):
    global accuracy
    global use_theta_0
    ax = fig.add_subplot(111)
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    ZZ = np.zeros_like(XX)
    R = np.sqrt(XX**2 + YY**2)
    A = np.zeros_like(XX)
    A[R > e / 2] = np.sqrt(2 * e * R[R > e / 2] - e**2)
    #Th = np.arctan2(YY, XX)
    ZZ[R > 1] = -1
    if 0: # show where you are guaranteed to win
        ZZ[R < e / 2] = 2
    if use_theta_0:
        ZZ[ZZ == 0] = (A[ZZ == 0] - XX[ZZ == 0])**2 + YY[ZZ == 0]**2 <= (e - R[ZZ == 0])**2
    else:
        Th2 = np.random.rand(ZZ.shape[0], ZZ.shape[1]) * 2 * np.pi
        ZZ[ZZ == 0] = (A[ZZ == 0] * np.cos(Th2[ZZ == 0]) - XX[ZZ == 0])**2 + (A[ZZ == 0] * np.sin(Th2[ZZ == 0]) - YY[ZZ == 0])**2 <= (e - R[ZZ == 0])**2
    
    alp = 1
    cmap = ListedColormap([colorConverter.to_rgba('white', alpha=alp), colorConverter.to_rgba('red', alpha=alp), colorConverter.to_rgba('blue', alpha=alp), colorConverter.to_rgba('blue', alpha=alp-.5)])    
    h = ax.contourf(X, Y, ZZ, [-1.5, -.5, 0.5, 1.5, 2.5], cmap=cmap)
    ax.axis('scaled')
    actual = P(e)
    thetaString = r"$\theta$ = 0" if use_theta_0 else r"$\theta$ = random" 
    fig.suptitle(f"{thetaString}, e = {e:.2f}, estimate = {np.sum(ZZ>0)/np.sum(ZZ>=0):.5f}, actual={actual:.5f}")
    fig.colorbar(h)
    #ax.title(f"d = {d}")
    #ax.colorbar()
    plt.draw()
    
    return XX, YY, ZZ
    
    
def onclick(fig):
    global E
    global idx
    fig.clear()
    idx += 1
    if idx >= E.size:
        idx = 0
    boundsGraph(E[idx], fig)
    plt.draw()

"""
Old functions assumed that Aaron chose (r, 0)
"""
def Pold(e):
    i1 = (e / 3)**2
    
    f = lambda r: 2 / np.pi * r * np.arccos(1/ 2 + e / r - e**2 / (2 * r**2))
    a = e / 3
    b = 1
    i2 = quad(f, a, b, epsabs=1e-12, epsrel=1e-12)
    return i1 + i2[0]

def PgridOld(e):
    accuracy = 300
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    R = np.sqrt(XX**2 + YY**2)
    #Th = np.arctan2(YY, XX)
    ZZ = np.zeros_like(XX)
    ZZ[R > 1] = -1
    ZZ[ZZ == 0] = (R[ZZ == 0] - XX[ZZ == 0])**2 + YY[ZZ == 0]**2 <= (e - R[ZZ == 0])**2
    return np.sum(ZZ > 0) / np.sum(ZZ >= 0)

def PgridRandOld(e):
    accuracy = 300
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    R = np.sqrt(XX**2 + YY**2)
    #Th = np.arctan2(YY, XX)
    Th2 = np.random.rand(XX.shape[0], XX.shape[1]) * 2 * np.pi
    ZZ = np.zeros_like(XX)
    ZZ[R > 1] = -1
    ZZ[ZZ == 0] = (R[ZZ == 0] * np.cos(Th2[ZZ == 0]) - XX[ZZ == 0])**2 + (R[ZZ == 0] * np.sin(Th2[ZZ == 0]) - YY[ZZ == 0])**2 <= (e - R[ZZ == 0])**2
    return np.sum(ZZ > 0) / np.sum(ZZ >= 0)

def PprimeOld(e):
    fe3 = 2 / np.pi * e / 3 * np.pi # f(e / 3)
    i1 = 2 * e / 9 - 1 / 3 * fe3
    a = e / 3
    b = 1
    f2 = lambda r: 2 / np.pi * r * -1 / np.sqrt(1 - (1/2 + e/r - e**2/(2 * r**2))**2) * (1 / r - e / r**2)
    i2 = quad(f2, a, b, epsabs=1e-12, epsrel=1e-12)
    return i1 + i2[0]

# less accurate
def Pprime2Old(e):
    return derivative(P, e, dx=1e-12)

def boundsGraphOld(e, fig):
    global accuracy
    global use_theta_0
    ax = fig.add_subplot(111)
    X = np.linspace(-1, 1, accuracy)
    Y = np.linspace(-1, 1, accuracy)
    XX, YY = np.meshgrid(X, Y)
    ZZ = np.zeros_like(XX)
    R = np.sqrt(XX**2 + YY**2)
    #Th = np.arctan2(YY, XX)
    ZZ[R > 1] = -1
    if 1: # show where you are guaranteed to win
        ZZ[R <= e / 3] = 2
    if use_theta_0:
        ZZ[ZZ == 0] = (R[ZZ == 0] - XX[ZZ == 0])**2 + YY[ZZ == 0]**2 <= (e - R[ZZ == 0])**2
    else:
        Th2 = np.random.rand(ZZ.shape[0], ZZ.shape[1]) * 2 * np.pi
        ZZ[ZZ == 0] = (R[ZZ == 0] * np.cos(Th2[ZZ == 0]) - XX[ZZ == 0])**2 + (R[ZZ == 0] * np.sin(Th2[ZZ == 0]) - YY[ZZ == 0])**2 <= (e - R[ZZ == 0])**2            
    
    alp = 1
    cmap = ListedColormap([colorConverter.to_rgba('white', alpha=alp), colorConverter.to_rgba('red', alpha=alp), colorConverter.to_rgba('blue', alpha=alp), colorConverter.to_rgba('blue', alpha=alp-.5)])    
    h = ax.contourf(X, Y, ZZ, [-1.5, -.5, 0.5, 1.5, 2.5], cmap=cmap)
    ax.axis('scaled')
    actual = Pold(e)
    fig.suptitle(f"e = {e:.2f}, estimate = {np.sum(ZZ>0)/np.sum(ZZ>=0)}, actual={actual}")
    fig.colorbar(h)
    #ax.title(f"d = {d}")
    #ax.colorbar()
    plt.draw()
    
    return XX, YY, ZZ


if __name__ == "__main__":
    if 1:
        idx = 0
        accuracy = 300
        use_theta_0 = True
        E = np.arange(0, 1.1, .1)
        #E = np.array([0.5013069457869279])
        fig = plt.figure()
        XX, YY, ZZ = boundsGraph(E[idx], fig)
        fig.canvas.mpl_connect('button_press_event', lambda event: onclick(fig))
        plt.show()
    
    if 0:
        x = np.linspace(0, 1)
        y = np.array([P(e) for e in x])
        plt.plot(x, y)
        
        #y2 = np.array([P2(e) for e in x])
        #plt.plot(x, y2)
        
        #yg = np.array([Pgrid(e) for e in x])
        #plt.plot(x, yg)
        
        #ygr = np.array([PgridRand(e) for e in x])
        #plt.plot(x, ygr)
        
    
    sol = fmin(P, np.array([.5]), xtol=1e-12, ftol=1e-12, full_output=True)
    pprint(sol)
    print(P_extra(sol[0][0]))
    
    if 0:
        plt.scatter(sol[0][0], sol[1])
    
    if 0:
        s = fmin(Pgrid, np.array([.5]), xtol=1e-12, ftol=1e-12, full_output=True)
        pprint(s)
    
    # find where derivative is 0
    # this is for old functions
    if 0:
        val = 0
        low = 0.5
        high = 0.6
        its = 0
        while True:
            its += 1
            if its >= 100:
                print("TOO MANY ITERATIONS")
                print(mid, p)
                break
            mid = (low + high) / 2
            p = Pprime(mid)
            #done = input((mid, p))
            #if done == "x":
                #break
            if abs(p) <= 1e-11:
                print("DONE")
                print(mid, p)
                break
            if val > p:
                low = mid
            else:
                high = mid
                
    # check between min and 1 for any better soln
    if 0:
        best = 1000
        low = sol[0][0]
        high = 1
        its = 0
        while True:
            its += 1
            if its >= 100:
                print("TOO MANY ITERATIONS")
                print(mid, p)
                break
            mid = (low + high) / 2
            p = P(mid)
            done = input((mid, p))
            if done == "x":
                break
            if abs(p - best) <= 1e-11:
                print("DONE")
                print(mid, p)
                break
            if best < p:
                low = mid
            else:
                high = mid