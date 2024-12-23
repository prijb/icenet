# "Analytic" algorithms, observables, metrics etc.
#
# m.mieskolainen@imperial.ac.uk, 2024

import numpy as np
import awkward as ak
import numba
from scipy import special as special


def phi_phasewrap(phi):
    """
    Used for example when phi is deltaphi = phi1 - phi2
    """
    return (phi + np.pi) % (2 * np.pi) - np.pi


def invmass(x, pt1: str, pt2: str, eta1: str, eta2: str, phi1: str, phi2: str, m1_const=0.1396, m2_const=0.1396):
    """
    invariant mass (exact)
    
    With awkward arrays
    """
    px1,py1,pz1 = x[pt1]*np.cos(x[phi1]), x[pt1]*np.sin(x[phi1]), x[pt1]*np.sinh(x[eta1])
    px2,py2,pz2 = x[pt2]*np.cos(x[phi2]), x[pt2]*np.sin(x[phi2]), x[pt2]*np.sinh(x[eta2])
    
    E1 = np.sqrt(m1_const**2 + px1**2 + py1**2 + pz1**2)
    E2 = np.sqrt(m2_const**2 + px2**2 + py2**2 + pz2**2)
    M2 = m1_const**2 + m2_const**2 + 2*(E1*E2 - (px1*px2 + py1*py2 + pz1*pz2))
    
    return np.sqrt(M2)


def invmass_massless(x, pt1: str, pt2: str, eta1: str, eta2: str, phi1: str, phi2: str):
    """
    invariant mass (massless limit)
    
    With awkward arrays
    """
    prodPt   = x[pt1] * x[pt2]
    deltaEta = x[eta1] - x[eta2]
    deltaPhi = phi_phasewrap(x[phi1] - x[phi2])
    
    return np.sqrt(2*prodPt*(np.cosh(deltaEta) - np.cos(deltaPhi)))


def deltaR(x, eta1: str, eta2: str, phi1: str, phi2: str):
    """
    dR distance (invariant [massless limit y --> eta] under longitudinal boosts)
    
    With awkward arrays
    """
    deltaEta = x[eta1] - x[eta2]
    deltaPhi = phi_phasewrap(x[phi1] - x[phi2])
    
    return np.sqrt(deltaEta**2 + deltaPhi**2)

#Versions of pt, invariant mass, dEta and dPhi only for the leading two objects (assume massless)
def diobj_pt(x, pt: str, eta: str, phi: str):
    """
    Di-object pT for only the leading two objects
    """
    px1,py1,pz1 = x[pt][:, 0]*np.cos(x[phi][:, 0]), x[pt][:, 0]*np.sin(x[phi][:, 0]), x[pt][:, 0]*np.sinh(x[eta][:, 0])
    px2,py2,pz2 = x[pt][:, 1]*np.cos(x[phi][:, 1]), x[pt][:, 1]*np.sin(x[phi][:, 1]), x[pt][:, 1]*np.sinh(x[eta][:, 1])

    return np.sqrt((px1 + px2)**2 + (py1 + py2)**2)

def diobj_mass(x, pt: str, eta: str, phi: str):
    """
    Di-object invariant mass for only the leading two objects
    """
    px1,py1,pz1 = x[pt][:, 0]*np.cos(x[phi][:, 0]), x[pt][:, 0]*np.sin(x[phi][:, 0]), x[pt][:, 0]*np.sinh(x[eta][:, 0])
    px2,py2,pz2 = x[pt][:, 1]*np.cos(x[phi][:, 1]), x[pt][:, 1]*np.sin(x[phi][:, 1]), x[pt][:, 1]*np.sinh(x[eta][:, 1])
    
    E1 = np.sqrt(px1**2 + py1**2 + pz1**2)
    E2 = np.sqrt(px2**2 + py2**2 + pz2**2)
    M2 = 2*(E1*E2 - (px1*px2 + py1*py2 + pz1*pz2))

    return np.sqrt(M2)

def diobj_dEta(x, eta: str):
    """
    Di-object delta eta for only the leading two objects
    """
    return np.abs(x[eta][:, 0] - x[eta][:, 1])

def diobj_dPhi(x, phi: str):
    """
    Di-object delta phi for only the leading two objects
    """
    return np.abs(phi_phasewrap(x[phi][:, 0] - x[phi][:, 1]))

#Convert HW to physical values
def get_pt_eta_phi_from_hw(x, pt: str, eta: str, phi: str):
    """
    Convert from hardware to physical values
    """
    x[pt] = x[pt]*0.5
    x[eta] = x[eta]*0.087
    x[phi] = x[phi]*np.pi/36.0
    x[phi] = phi_phasewrap(x[phi])
    return x

def get_sphericity(m):
    """
    Matrix is 3x3

    Returns lambda2 + lambda3
    """
    #Normalise to unit determinant
    #m = m / (np.linalg.det(m)**(1/3))
    vals = np.linalg.eigvals(m)
    vals = np.sort(vals)[::-1]
    return 1.5*(vals[1] + vals[2])


#Event sphericity
def sphericity(x, pt: str, eta: str, phi: str):
    """
    Event sphericity
    """
    #print("\nBefore conversion")
    #print("pT")
    #print(x[pt])
    #print("eta")
    #print(x[eta])
    #print("phi")
    #print(x[phi])

    #Convert from hardware
    #x[pt] = x[pt]*0.5
    #x[eta] = x[eta]*0.0435
    #x[phi] = x[phi]*0.0435
    #Confine to [-pi, pi]
    #x[phi] = phi_phasewrap(x[phi])

    print("\nAfter conversion")
    print("pT")
    print(x[pt])
    print("eta")
    print(x[eta])
    print("phi")
    print(x[phi])

    px = x[pt] * np.cos(x[phi])
    py = x[pt] * np.sin(x[phi])
    pz = x[pt] * np.sinh(x[eta])

    #Sums for sphericity
    Sxx = ak.sum(px*px, axis=-1)
    Syy = ak.sum(py*py, axis=-1)
    Szz = ak.sum(pz*pz, axis=-1)

    Sxy = ak.sum(px*py, axis=-1)
    Sxz = ak.sum(px*pz, axis=-1)
    Syz = ak.sum(py*pz, axis=-1)

    #Normalisation
    Spp = Sxx + Syy + Szz

    print("\nSxx")
    print(Sxx)
    print("Syy")
    print(Syy)
    print("Szz")
    print(Szz)
    print("Spp")
    print(Sxx + Syy + Szz)

    #Non-vectorised loops :( , but that's what I'm doing for now bc of this matrix business
    sphericities = []
    for i in range(len(Spp)):
        if Spp[i] == 0:
            sphericities.append(0)
            continue
        
        S_matrix = np.array([[Sxx[i], Sxy[i], Sxz[i]],
                         [Sxy[i], Syy[i], Syz[i]],
                         [Sxz[i], Syz[i], Szz[i]]]) / Spp[i]
        #S_matrix = np.array([[Sxx[i], Sxy[i], Sxz[i]],
        #                 [Sxy[i], Syy[i], Syz[i]],
        #                 [Sxz[i], Syz[i], Szz[i]]])

        sphericities.append(get_sphericity(S_matrix))

    sphericities = ak.Array(sphericities)

    return sphericities



def fox_wolfram_boost_inv(p, L=10):
    """
    arxiv.org/pdf/1508.03144, (Formula 5.6)

    Args:
        p : list of 4-momentum vectors
        L : maximum angular moment order
    Returns:
        S : list of moments of order 0,1,...,L

    [untested function]
    """
    N  = len(p)
    S  = np.zeros(L+1)
    k  = special.jn_zeros(0, L+1)
    pt = [p[i].pt for i in range(N)]

    dR = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            if i > j:
                dR[i,j] = p[i].deltaR(p[j])
    
    # Compute moments
    for n in range(len(S)):
        for i in range(N):
            for j in range(N):
                if i >= j: # count also the case i==j
                    S[n] += pt[i] * pt[j] * special.j0(k[n]*dR[i,j])

    return S


def gram_matrix(X, type='dot'):
    """
    Gram matrix for 4-vectors.

    Args:
        X    : Array (list of N) of 4-vectors
        type : Type of Lorentz scalars computed ('dot', 's', 't')
    
    Returns:
        G : Gram matrix (NxN)
    """
    
    N = len(X)
    G = np.zeros((N,N))
    for i in range(len(X)):
        for j in range(len(X)):
            if   type == 'dot':
                G[i,j] = X[i].dot(X[j])   ## 4-dot product
            elif type == 's':
                G[i,j] = (X[i] + X[j]).p2 ## s-type
            elif type == 't':
                G[i,j] = (X[i] - X[j]).p2 ## t-type
            else:
                raise Exception('gram_matrix: Unknown type!')
    return G


@numba.njit
def ktmetric(kt2_i, kt2_j, dR2_ij, p = -1, R = 1.0):
    """
    kt-algorithm type distance measure.
    
    Args:
        kt2_i     : Particle 1 pt squared
        kt2_j     : Particle 2 pt squared
        delta2_ij : Angular seperation between particles squared (deta**2 + dphi**2)
        R         : Radius parameter
        
        p =  1    : (p=1) kt-like, (p=0) Cambridge/Aachen, (p=-1) anti-kt like
    
    Returns:
        distance measure
    """
    a = kt2_i**(2*p)
    b = kt2_j**(2*p) 
    c = (dR2_ij/R**2)
    
    return (a * c) if (a < b) else (b * c)

def get_Lorentz_edge_features(p4vec, num_nodes, num_edges, num_edge_features, directed, self_loops, EPS=1E-12):
    
    # Edge features: [num_edges, num_edge_features]
    edge_attr = np.zeros((num_edges, num_edge_features), dtype=float)
    indexlist = np.zeros((num_nodes, num_nodes), dtype=int)
    
    n = 0
    for i in range(num_nodes):
        for j in range(num_nodes):

            if (i == j) and (self_loops == False):
                continue

            if (i < j)  and (directed == True):
                continue

            p4_i   = p4vec[i]
            p4_j   = p4vec[j]

            # kt-metric (anti)
            dR2_ij = p4_i.deltaR(p4_j)**2
            kt2_i  = p4_i.pt2 + EPS 
            kt2_j  = p4_j.pt2 + EPS
            edge_attr[n,0] = ktmetric(kt2_i=kt2_i, kt2_j=kt2_j, dR2_ij=dR2_ij, p=-1, R=1.0)
            
            # Lorentz scalars
            edge_attr[n,1] = (p4_i + p4_j).m2  # Mandelstam s-like
            edge_attr[n,2] = (p4_i - p4_j).m2  # Mandelstam t-like
            edge_attr[n,3] = p4_i.dot4(p4_j)   # 4-dot
            
            indexlist[i,j] = n
            n += 1
    
    ### Copy to the lower triangle for speed (we have symmetric adjacency)
    # (update this to be compatible with self-loops and directed computation)
    """
    n = 0
    for i in range(num_nodes):
        for j in range(num_nodes):
            if (j < i):
                edge_attr[n,:] = edge_attr[indexlist[j,i],:] # note [j,i] !
            n += 1
    """

    # Cast
    edge_attr = edge_attr.astype(float)
    
    return edge_attr


def count_simple_edges(num_nodes, directed, self_loops):
    """
    Count number of edges in a (semi)-fully connected adjacency matrix
    """
    if   directed == False and self_loops == False:
        return num_nodes**2 - num_nodes
    elif directed == False and self_loops == True:
        return num_nodes**2
    elif directed == True  and self_loops == False:
        return (num_nodes**2 - num_nodes) / 2
    elif directed == True  and self_loops == True:
        return (num_nodes**2 - num_nodes) / 2 + num_nodes

@numba.njit
def get_simple_edge_index(num_nodes, num_edges, directed, self_loops):

    # Graph connectivity: (~ sparse adjacency matrix)
    edge_index = np.zeros((2, num_edges))

    n = 0
    for i in range(num_nodes):
        for j in range(num_nodes):

            if (i == j) and (self_loops == False):
                continue

            if (i < j)  and (directed == True):
                continue

            edge_index[0,n] = i
            edge_index[1,n] = j
            n += 1
    
    return edge_index
