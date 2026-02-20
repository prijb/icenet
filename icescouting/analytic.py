# "Analytic" algorithms, observables, metrics etc. specific to Scouting use case

import numpy as np
import awkward as ak
import numba
from scipy import special as special

from icenet.tools.icevec import vec4

## Add SV mass to events
def get_sv_mass(muons, svs):
    muon_pairs = ak.combinations(muons, 2, fields=["muon_i", "muon_j"])

    os_mask = muon_pairs.muon_i.ch != muon_pairs.muon_j.ch 
    same_vtx_mask = (muon_pairs.muon_i.bestAssocSVIdx == muon_pairs.muon_j.bestAssocSVIdx)
    valid_vtx_mask = muon_pairs.muon_i.bestAssocSVIdx > -1
    mask = np.logical_and(os_mask, same_vtx_mask)
    mask = np.logical_and(mask, valid_vtx_mask)

    muon_pairs = muon_pairs[mask]

    svs_mass = ak.ArrayBuilder()

    for i_event in range(len(muons)):
        muon_pairs_i = muon_pairs[i_event]
        svs_i = svs[i_event]
        svs_mass_i = np.full(len(svs_i), -1.0)

        if len(muon_pairs_i) > 0:
            for muon_pair in muon_pairs_i:
                muon_i = muon_pair.muon_i
                muon_j = muon_pair.muon_j

                muon_i_vec = vec4()
                muon_i_vec.setPtEtaPhiM(muon_i.pt, muon_i.eta, muon_i.phiCorr, 0.10566)
                muon_j_vec = vec4()
                muon_j_vec.setPtEtaPhiM(muon_j.pt, muon_j.eta, muon_j.phiCorr, 0.10566)
                dimuon = muon_i_vec + muon_j_vec
                
                sv_idx = muon_i.bestAssocSVIdx

                for i_sv in range(len(svs_i)):
                    if (svs_i.index[i_sv] == sv_idx):
                        svs_mass_i[i_sv] = dimuon.m
                        break

        svs_mass.append(svs_mass_i)

    return svs_mass
