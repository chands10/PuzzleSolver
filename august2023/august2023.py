import numpy as np
from scipy.integrate import quad, dblquad, tplquad, nquad
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter, ListedColormap
"""
def bounds1_new(d):
    if d < 2:
        upperX = 1
    else:
        upperX = 1 - d * np.cos(np.arcsin(2 / d))
    X = np.arange(max(0, 1 - d), upperX, .1)
    good = True
    for x in X:
        upper = min(1, 2 - d * np.sin(np.arccos((1 - x) / d)))
        lower = max(0, 1 - d * np.sin(np.arccos((1 - x) / d)))
        diff = upper - lower
        if diff < 0:
            good = False
            break
    if not good:
        print(d, 1 - d * np.cos(np.arcsin(2 / d)))
"""

def bounds1(d):
    X = np.arange(max(0, 1 - d), 1, .1)
    good = True
    for x in X:
        upper = min(1, 2 - d)
        lower = max(0, 1 - d * np.sin(np.arccos((1 - x) / d)))
        diff = upper - lower
        if diff < 0:
            good = False
            break
    if not good:
        print(d)
        
def bounds2(d):
    if d < 1:
        print(d)
        return
    assert(np.sin(np.arccos(1 / d)) >= 0)
    if min(1, 2 - d * np.sin(np.arccos(1 / d))) < max(0, 2 - d):
        print(d)
        return
    print("MADE IT HERE")
    X = np.arange(max(0, 2 - d), min(1, 2 - d * np.sin(np.arccos(1 / d))), .1)
    good = True
    uppers = []
    for x in X:
        upper = 1 - d * np.cos(np.arcsin((2 - x) / d))
        uppers.append(upper)
        lower = 0
        diff = upper - lower
        if diff < 0:
            good = False
            #break
    #E = np.array([.1, .2, .3, .4, .5])
    #E += X[-1]
    #EY = []
    #for x in E:
        #EY.append(1 - d * np.cos(np.arcsin((2 - x) / d)))
        
    if not good:
        print(d)
    #plt.plot(X, uppers)
    #plt.plot(E, EY)
    #plt.plot(X, np.zeros_like(X))

def bounds3(d):
    lowerX = max(0, 1 - d)
    if d < 1:
        upperX = min(1, 2 - d)
    else:
        upperX = min(2 - d, 1 - d * np.sin(np.arccos(1 / d)))
    if lowerX > upperX:
        print(d)
        return
    
    X = np.arange(lowerX, upperX, .1)
    good = True
    for x in X:
        #print(f"x = {x}, d = {d}")
        if d == 0:
            upper = 1
        else:
            upper = 1 - d * np.cos(np.arcsin((1 - x) / d))
        if d > 0:
            assert(1 - x <= d)
        lower = 0
        diff = upper - lower
        if diff < 0:
            good = False
            break
    if not good:
        print(d)

"""
def int1_new(d):
    if not 0 < d < np.sqrt(5):
        return 0, 0
    
    #dy dx
    f = lambda y, x: np.arcsin((1 - x) / d)
    x1 = max(0, 1 - d)
    x2 = 1 if d < 2 else 1 - d * np.cos(np.arcsin(2 / d))
    g = lambda x: max(0, 1 - d * np.sin(np.arccos((1 - x) / d)))
    h = lambda x: max(0, min(1, 2 - d * np.sin(np.arccos((1 - x) / d))))
    i = dblquad(f, x1, x2, g, h)
    print(f"d = {d}, i[0] = {i[0]}")
    assert(i[0] >= 0)
    return 4 / np.pi * i[0], i[1]
"""

def int1(d):
    if not 0 < d < 2:
        return 0, 0
    
    #dy dx
    f = lambda y, x: np.arcsin((1 - x) / d)
    x1, x2 = max(0, 1 - d), 1
    g = lambda x: max(0, 1 - d * np.sin(np.arccos((1 - x) / d)))
    h = lambda x: min(1, 2 - d)
    i = dblquad(f, x1, x2, g, h)
    assert(i[0] >= 0)
    return 4 / np.pi * i[0], i[1]

def int2(d):
    if not 1 < d < np.sqrt(5):
        return 0, 0
    
    #dx dy
    f = lambda x, y: np.arcsin((1 - x) / d) - np.arccos((2 - y) / d)
    y1, y2 = max(0, 2 - d), min(1, 2 - d * np.sin(np.arccos(1 / d)))
    g = lambda y: 0
    h = lambda y: 1 - d * np.cos(np.arcsin((2 - y) / d))
    i = dblquad(f, y1, y2, g, h)
    assert(i[0] >= 0)
    return 4 / np.pi * i[0], i[1]

def int3(d):
    if not 0 < d < np.sqrt(2):
        return 0, 0
    
    #dx dy
    f = lambda x, y: np.arccos((1 - y) / d)
    y1 = max(0, 1 - d)
    if d < 1:
        y2 = 1
    else:
        y2 = 1 - d * np.sin(np.arccos(1 / d))
    g = lambda y: 0
    h = lambda y: 1 - d * np.cos(np.arcsin((1 - y) / d))
    i = dblquad(f, y1, y2, g, h)
    assert(i[0] >= 0)
    return 4 / np.pi * i[0], i[1]

def int_simple(d):
    i1, e1 = int1(d)
    i2, e2 = int2(d)
    i3, e3 = int3(d)
    return i1 + i2 + i3, i1, i2, i3, e1, e2, e3

def b2_3d(d):
    z1 = 1 - d
    z2 = 1
    zs = np.arange(z1, z2, .1)
    for z in zs:
        x1 = 1 - d * np.sin(np.arccos((1 - z) / d))
        x2 = 1
        xs = np.arange(x1, x2, .1)
        for x in xs:
            h1 = 1 - z
            h2 = d * np.cos(np.arcsin((1 - x) / d)) 
            if h1 - h2 > .00001:
                print(f"h1={h1} > h2={h2}, d={d}, z={z}, x={x}")
            hs = np.arange(h1, h2, .1)
            for h in hs:
                num = 1 - x
                den = d * np.sin(np.arccos(h / d))
                if num > den:
                    print(f"h = {h}, x = {x}, z = {z} num = {num}, den={den}, bad={num>den}")

def i1new(d):
    if not 0 < d <= 1:
        return 0, 0
    
    #dx dy dz
    f = lambda x, y, z: np.pi / 2 * d * (z + d - 1)
    x1 = lambda y, z: 0
    x2 = lambda y, z: 1
    y1 = lambda z: 0
    y2 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    z1 = 1 - d
    z2 = 1
    i = tplquad(f, z1, z2, y1, y2, x1, x2)
    assert(i[0] >= 0)
    return 3 * 2 / (np.pi * d**2) * i[0], i[1]

def i1_2new(d):
    if not 0 < d <= 1:
        return 0, 0
    
    #dx dy dz
    f = lambda x, y, z: np.pi / 2 * d * (z + d - 1)
    x1 = lambda y, z: 0
    x2 = lambda y, z: 1 - np.sqrt((d * np.sin(np.arccos((1 - z) / d)))**2 - (y - 1)**2)
    y1 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    y2 = lambda z: 1
    z1 = 1 - d
    z2 = 1
    i = tplquad(f, z1, z2, y1, y2, x1, x2)
    assert(i[0] >= 0)
    return 3 * 2 / (np.pi * d**2) * i[0], i[1]

def i2new(d):
    if not 0 < d <= 1:
        return 0, 0
    
    # dx dy dz
    f = lambda x, y, z: np.pi / 2 * d * (d - d * np.cos(np.arcsin(1 / d * np.sqrt((x - 1)**2 + (y - 1)**2))))
    x1 = lambda y, z: 1 - np.sqrt((d * np.sin(np.arccos((1 - z) / d)))**2 - (y - 1)**2)
    x2 = lambda y, z: 1
    y1 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    y2 = lambda z: 1
    z1 = 1 - d
    z2 = 1
    i = tplquad(f, z1, z2, y1, y2, x1, x2)
    assert(i[0] >= 0)
    return 3 * 2 / (np.pi * d**2) * i[0], i[1]

# subtract this
def i3new(d):
    if not 0 < d <= 1:
        return 0, 0
    
    # dphi dx dz
    f = lambda phi, x, z: d**2 * np.arccos((1 - x) / (d * np.sin(phi))) * np.sin(phi) * d * np.sin(np.arccos((1 - z) / d))
    phi1 = lambda x, z: np.arcsin((1 - x) / d)
    phi2 = lambda x, z: np.arccos((1 - z) / d)
    x1 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    x2 = lambda z: 1
    z1 = 1 - d
    z2 = d
    i = tplquad(f, z1, z2, x1, x2, phi1, phi2)
    assert(i[0] >= 0)
    return 2 * 3 * 2 / np.pi * i[0], i[1]

# subtract this
def i3_2new(d):
    if not 0 < d <= 1:
        return 0, 0
    
    # dphi dx dy dz
    f = lambda phi, x, y, z: d**2 * np.arccos((1 - x) / (d * np.sin(phi))) * np.sin(phi)
    phis = lambda x, y, z: (np.arcsin((1 - x) / d), np.arccos((1 - z) / d))
    xs = lambda y, z: (1 - d * np.sin(np.arccos((1 - z) / d)), 1)
    ys = lambda z: (1 - d * np.sin(np.arccos((1 - z) / d)), 1)
    zs = (1 - d, 1)
    i = nquad(f, [phis, xs, ys, zs])
    assert(i[0] >= 0)
    return 2 * 3 * 2 / np.pi * i[0], i[1]

def sa(x, y, z, d):
    f = lambda phi: np.arccos((1 - x) / d * np.sin(phi)) * np.sin(phi)
    phi1 = np.arcsin((1 - x) / d)
    phi2 = np.arccos((1 - z) / d)
    i = quad(f, phi1, phi2)
    assert(i[0] >= 0)
    return d**2 * i[0], i[1]

def simulation(d, trials):
    adjOne = lambda a, b: 0 <= a <= 1 and (1 <= b <= 2 or -1 <= b <= 0)
    adj = lambda a, b: adjOne(a, b) or adjOne(b, a)
    success = 0
    for i in range(trials):
        x, y, theta = np.random.rand(3)
        theta *= 2 * np.pi
        newX = x + d * np.cos(theta)
        newY = y + d * np.sin(theta)
        success += adj(newX, newY)
        
    return success / trials

def simulation3d(d, trials):
    adjOne = lambda a, b, c: 0 <= a <= 1 and 0 <= b <= 1 and (1 <= c <= 2 or -1 <= c <= 0)
    adj = lambda a, b, c: adjOne(a, b, c) or adjOne(c, a, b) or adjOne(b, c, a)
    success = 0
    for i in range(trials):
        x, y, z, theta, phi = np.random.rand(5)
        theta *= 2 * np.pi
        phi *= np.pi
        newX = x + d * np.sin(phi) * np.cos(theta)
        newY = y + d * np.sin(phi) * np.sin(theta)
        newZ = z + d * np.cos(phi)
        success += adj(newX, newY, newZ)
        
    return success / trials

def simulation3d1_5(d, trials):
    adjOne = lambda a, b, c: 0 <= a <= 1 and 0 <= b <= 1 and (1 <= c <= 2 or -1 <= c <= 0)
    adj = lambda a, b, c: adjOne(a, b, c) or adjOne(c, a, b) or adjOne(b, c, a)
    success = 0
    for i in range(trials):
        x, y, z, theta, = np.random.rand(4)
        theta *= 2 * np.pi
        bVal = 4
        phi = np.random.beta(bVal, bVal)
        phi *= np.pi
        newX = x + d * np.sin(phi) * np.cos(theta)
        newY = y + d * np.sin(phi) * np.sin(theta)
        newZ = z + d * np.cos(phi)
        success += adj(newX, newY, newZ)
        
    return success / trials


def simulation3d2(d, trials):
    adjOne = lambda a, b, c: 0 <= a <= 1 and 0 <= b <= 1 and (1 <= c <= 2 or -1 <= c <= 0)
    adj = lambda a, b, c: adjOne(a, b, c) or adjOne(c, a, b) or adjOne(b, c, a)
    success = 0
    for i in range(trials):
        x, y, z, theta, phi = np.random.rand(5)
        theta *= 2 * np.pi
        phi = np.arccos(2 * phi - 1)
        newX = x + d * np.sin(phi) * np.cos(theta)
        newY = y + d * np.sin(phi) * np.sin(theta)
        newZ = z + d * np.cos(phi)
        success += adj(newX, newY, newZ)
        
    return success / trials

# seems to dip a bit at the end
def simulation3d3(d, trials):
    adjOne = lambda a, b, c: 0 <= a <= 1 and 0 <= b <= 1 and (1 <= c <= 2 or -1 <= c <= 0)
    adj = lambda a, b, c: adjOne(a, b, c) or adjOne(c, a, b) or adjOne(b, c, a)
    success = 0
    for i in range(trials):
        x, y, z = np.random.rand(3)
        z2 = np.random.rand() # between -d and d
        z2 = (z2 - 0.5) * 2 * d
        radius = d * np.sin(np.arccos(abs(z2) / d))
        x2 = np.random.rand()
        x2 = (x2 - 0.5) * 2 * radius # between -radius and radius
        y2 = np.sqrt(radius**2 - x2**2)
        if np.random.rand() < .5:
            y2 *= -1
        newX = x + x2
        newY = y + y2
        newZ = z + z2
        success += adj(newX, newY, newZ)
        
    return success / trials

def b1(d, x, y):
    x1, x2 = max(0, 1 - d), 1
    g = lambda x: max(0, 1 - d * np.sin(np.arccos((1 - x) / d)))
    h = lambda x: min(1, 2 - d)
    if not x1 <= x <= x2:
        return False
    if not g(x) <= y <= h(x):
        return False
    return True

def b2(d, x, y):
    y1, y2 = max(0, 2 - d), min(1, 2 - d * np.sin(np.arccos(1 / d)))
    if not y1 <= y <= y2:
        return False
    g = lambda y: 0
    h = lambda y: 1 - d * np.cos(np.arcsin((2 - y) / d))
    if not g(y) <= x <= h(y):
        return False
    return True

def b3(d, x, y):
    y1 = max(0, 1 - d)
    if d < 1:
        y2 = 1
    else:
        y2 = 1 - d * np.sin(np.arccos(1 / d))
    g = lambda y: 0
    h = lambda y: 1 - d * np.cos(np.arcsin((1 - y) / d))
    if not y1 <= y <= y2:
        return False
    if not g(y) <= x <= h(y):
        return False
    return True

def boundsGraph(d, fig):
    ax = fig.add_subplot(111)
    X = np.linspace(0, 1)
    Y = np.linspace(0, 1)
    XX, YY = np.meshgrid(X, Y)
    ZZ = np.zeros_like(XX)
    for i in range(X.size):
        for j in range(Y.size):
            x = XX[j, i]
            y = YY[j, i]
            box = []
            if b1(d, x, y):
                box.append(1)
            if b2(d, x, y):
                box.append(2)
            if b3(d, x, y):
                box.append(3)
            if len(box) > 0:
                ZZ[j,i] = box[np.random.randint(len(box))]
            else:
                ZZ[j,i] = 0
    
    #ZZ = np.array(ZZ).reshape(XX.shape)
    alp = 1
    cmap = ListedColormap([colorConverter.to_rgba('white', alpha=alp), colorConverter.to_rgba('blue', alpha=alp), colorConverter.to_rgba('orange', alpha=alp), colorConverter.to_rgba('green', alpha=alp)])    
    h = ax.contourf(X, Y, ZZ, [-.5, 0.5, 1.5, 2.5, 3.5], cmap=cmap)
    ax.axis('scaled')
    fig.suptitle(f"d = {d:.1f}")
    fig.colorbar(h)
    #ax.title(f"d = {d}")
    #ax.colorbar()
    plt.draw()

def onclick(fig):
    global D
    global idx
    fig.clear()
    idx += 1
    if idx >= D.size:
        idx = 0
    boundsGraph(D[idx], fig)
    plt.draw()
    
def grapher(funcs, labels, D):
    Is = [[] for i in range(len(funcs))]
    for d in D:
        print(f"d = {d}")
        for i, func in enumerate(funcs):
            inte, e = func(d)
            Is[i].append(inte)
    Is = np.array(Is)
    for i in range(len(Is)):
        plt.plot(D, np.abs(Is[i]), label=labels[i])
    plt.plot(D, Is.sum(0), label="Sum of I")
    plt.legend()
    return Is

def i1new2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    #dz
    f = lambda z: np.pi / 2 * d * (z + d - 1) * (1 - d * np.sin(np.arccos((1 - z) / d)))**2
    z1 = 1 - d
    z2 = 1
    i = quad(f, z1, z2)
    assert(i[0] >= 0)
    return 3 * 2 / (np.pi * d**2) * i[0], i[1]

def i1_2new2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    #dx dz
    f = lambda x, z: np.pi / 2 * d * (d - d * np.cos(np.arcsin((1 - x) / d))) * x
    x1 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    x2 = lambda z: 1
    z1 = 1 - d
    z2 = 1
    i = dblquad(f, z1, z2, x1, x2)
    assert(i[0] >= 0)
    return 2 * 3 * 2 / (np.pi * d**2) * i[0], i[1]

def i2new2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    # dphi dx dz
    f = lambda phi, x, z: d**2 * np.arcsin((1 - x) / (d * np.sin(phi))) * np.sin(phi) * d * np.sin(np.arccos((1 - z) / d))
    phi1 = lambda x, z: np.arcsin((1 - x) / d)
    phi2 = lambda x, z: np.arccos((1 - z) / d)
    x1 = lambda z: 1 - d * np.sin(np.arccos((1 - z) / d))
    x2 = lambda z: 1
    z1 = 1 - d
    z2 = d
    i = tplquad(f, z1, z2, x1, x2, phi1, phi2)
    assert(i[0] >= 0)
    return 2 * 3 * 2 / np.pi * i[0], i[1]

def zInBounds(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: d * np.cos(phi) * (1 - d * np.sin(phi) * np.cos(th)) * (1 - d * np.sin(phi) * np.sin(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 4 / np.pi**2 * i[0], i[1]

def xInBounds(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: d * np.sin(phi) * np.cos(th) * (1 - d * np.cos(phi)) * (1 - d * np.sin(phi) * np.sin(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 4 / np.pi**2 * i[0], i[1]

def yInBounds(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: d * np.sin(phi) * np.sin(th) * (1 - d * np.cos(phi)) * (1 - d * np.sin(phi) * np.cos(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 4 / np.pi**2 * i[0], i[1]

def zInBounds2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: np.sin(phi) * d * np.cos(phi) * (1 - d * np.sin(phi) * np.cos(th)) * (1 - d * np.sin(phi) * np.sin(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 2 / np.pi * i[0], i[1]

def xInBounds2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: np.sin(phi) * d * np.sin(phi) * np.cos(th) * (1 - d * np.cos(phi)) * (1 - d * np.sin(phi) * np.sin(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 2 / np.pi * i[0], i[1]

def yInBounds2(d):
    if not 0 < d <= 1:
        return 0, 0
    
    phi1 = 0
    phi2 = np.pi / 2
    th1 = 0
    th2 = np.pi / 2
    f = lambda phi, th: np.sin(phi) * d * np.sin(phi) * np.sin(th) * (1 - d * np.cos(phi)) * (1 - d * np.sin(phi) * np.cos(th))
    i = dblquad(f, th1, th2, phi1, phi2)
    return 2 / np.pi * i[0], i[1]

def P2(d):
    return 1 / (4 * np.pi) * d * (-16 * d + 3 * d**2 + 6 * np.pi)

def P(d):
    return 4 / np.pi**2 * (1/2 * d**3 - (2 + np.pi / 4) * d**2 + (4 + np.pi) / 2 * d)
    
D = np.linspace(0, np.sqrt(5))
if 0:
    D = np.arange(0, np.sqrt(5), .1)
    for d in D:
        #bounds1_new(d)
        bounds1(d)
        bounds2(d)
        bounds3(d)
        input()

I1 = []
I2 = []
I3 = []
I = []
E1 = []
E2 = []
E3 = []
E = []
if 0:
    for d in D:
        i, i1, i2, i3, e1, e2, e3 = int_simple(d)
        I1.append(i1)
        I2.append(i2)
        I3.append(i3)
        I.append(i)
        
        E1.append(e1)
        E2.append(e2)
        E3.append(e3)
        E.append(e1 + e2 + e3)

    plt.plot(D, I1, label="I1")
    plt.plot(D, I2, label="I2")
    plt.plot(D, I3, label="I3")
    plt.plot(D, I, label="Sum of I")
    plt.legend()
if 0:
    sims = [simulation(d, 10000) for d in D]
    plt.plot(D, sims)

if 0:
    idx = 0
    # D = [1]
    D = np.arange(0, np.sqrt(5), .1)
    fig = plt.figure()
    boundsGraph(D[idx], fig)
    fig.canvas.mpl_connect('button_press_event', lambda event: onclick(fig))
    plt.show()
#for d in D:
    #boundsGraph(d)
    #input()

# ---3D---
#D = np.arange(0, np.sqrt(6), .1)
D = np.linspace(0, 1)
#D = np.linspace(0, np.sqrt(6))
if 1:
    sims = np.array([simulation3d(d, 10000) for d in D])
    plt.plot(D, sims, label="Simulation")
    
    sims2 = np.array([simulation3d2(d, 10000) for d in D])
    plt.plot(D, sims2, label="Simulation 2")    

    sims1_5 = np.array([simulation3d1_5(d, 10000) for d in D])
    plt.plot(D, sims1_5, label="Simulation 1.5")    
    
    for d, sim in zip(D, sims):
        print(d, sim)    

if 0:
    Is = grapher([i1new, i1_2new, i2new], ["I1", "I1_2", "I2"], D)

if 0:
    Is = grapher([i1new2, i1_2new2], ["I1", "I1_2"], D)
    

if 1:
    #Is = grapher([zInBounds, xInBounds, yInBounds], ["z", "x", "y"], D)
    Y = P(D)
    Y[Y<0] = 0
    plt.plot(D, Y, label="Function I found") # didn't account for Jacobian :(
    #Is2 = grapher([zInBounds2, xInBounds2, yInBounds2], ["z2", "x2", "y2"], D)
    Y2 = P2(D)
    Y2[Y2<0] = 0
    plt.plot(D, Y2, label="Jane Street Soln")
    plt.legend()
    plt.show()

    d = 1 / 6 * (8 + np.pi - np.sqrt(np.pi**2 + 4 * np.pi + 16))
    print(f"{d=}, {P(d)=}")
    print(np.sum((Y2-sims2)**2), np.sum((Y2-sims1_5)**2))