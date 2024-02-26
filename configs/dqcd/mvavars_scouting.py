# DQCD root file input

# ---------------------------------------------------------
# Conditional (parametric) signal model variables

MODEL_VARS = [
  'MODEL_mpi',
  'MODEL_mA',
  'MODEL_ctau',
]

# ---------------------------------------------------------
# Generator level variables

KINEMATIC_GEN_VARS = [
  'GenJet_pt',
  'GenJet_eta',
  'GenJet_phi',
  'GenJet_mass'
]

# ---------------------------------------------------------
# Trigger flag bit variables

TRIGGER_VARS = [
  'L1_DoubleMu_15_7',
  'L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7',
  'L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18',
  'L1_DoubleMu4_SQ_OS_dR_Max1p2',
  'L1_DoubleMu4p5_SQ_OS_dR_Max1p2'

]

# ---------------------------------------------------------
# For plots etc.

KINEMATIC_VARS = [
  'nJet',
  'nMuon',
  'nSV',
  'nmuonSV',
]

# ---------------------------------------------------------
# Pure scalar variables (non-nested)

MVA_SCALAR_VARS = [
  'nJet',
  'nMuon',
  'nSV',
  'nmuonSV',
]

# ---------------------------------------------------------
# Charged particle flow
#
# 'cpf_' is the custom (nanotron) jet-matched collection
#


#MVA_CPF_VARS = ['cpf_.*']

MVA_CPF_VARS = []

# ---------------------------------------------------------
# Neutral particle flow
#
# 'npf_' is the custom (nanotron) jet-matched collection
#


MVA_NPF_VARS = []



# ---------------------------------------------------------
# Jets
#  'Jet_' is the standard nanoAOD collection
#
MVA_JET_VARS = [
  'Jet_pt',
  'Jet_eta',
  'Jet_phi',
  'Jet_mass',
]

#MVA_JET_VARS = ['Jet_.*']

# ---------------------------------------------------------
# Muons
#  'Muon_' is the standard nanoAOD collection
#  'muon_' is the jet matched custom-collection 
#
MVA_MUON_VARS = [
  'Muon_eta',
  'Muon_phi',
  'Muon_pt',
  'Muon_normalizedChi2',
  'Muon_ecalIso',
  'Muon_hcalIso',
  'Muon_trackIso',

  'Muon_dxy',         # impact parameter: dxy (with sign) wrt PV (cm)
  'Muon_dxyErr',
  
  'Muon_dz',          # impact parameter: dz  (with sign) wrt PV (cm)
  'Muon_dzErr',
  
  'Muon_charge',
  
  'Muon_isTracker',
  'Muon_isGlobal',
  'Muon_isPFmatched',
  'Muon_isStandalone',

  #Add scouting variables for hits
  'Muon_nStations',
  'Muon_nValidPixelHits',
  'Muon_nValidStripHits',
  'Muon_nTrackerLayersWithMeasurement',
  'Muon_nPixelLayersWithMeasurement'
]

#MVA_MUON_VARS = ['Muon_.*']

# ---------------------------------------------------------
# Secondary vertex
#  'SV_'        is the standard nanoAOD collection
#  'MuonSV_'    is the custom muon SV collection


MVA_MUONSV_VARS = [
  'muonSV_chi2',     # Reduced chi2, i.e. chi2 / ndof
  'muonSV_pAngle',   # Pointing angle: acos(p_SV * (SV - PV))

  'muonSV_dlen',     # 3D decay length (cm)
  'muonSV_dlenSig',  # 3D decay length significance
  'muonSV_dxy',      # 2D transverse decay length (cm)
  'muonSV_dxySig',   # 2D transverse decay length significance

  'muonSV_mu1pt',    # Muon (1) kinematics
  'muonSV_mu1eta',
  'muonSV_mu1phi',
  'muonSV_mu2pt',    # Muon (2) kinematics
  'muonSV_mu2eta',
  'muonSV_mu2phi',
  
  'muonSV_x',        # Sec. vertex position
  'muonSV_y',        # Sec. vertex position
  'muonSV_z'         # Sec. vertex position
]


MVA_SV_VARS = [
  'SV_mass',    # Mass

  'SV_x',       # Sec. vertex position
  'SV_y',       # Sec. vertex position
  'SV_z',       # Sec. vertex position

  'SV_dxy',     # 2D transverse decay length (cm)
  'SV_dxySig',  # 2D transverse decay length significance
  'SV_dlen',    # 3D decay length (cm)
  'SV_dlenSig', # 3D decay length significance
  'SV_pAngle',  # Pointing angle: acos(p_SV * (SV - PV))

  'SV_chi2',    # Reduced chi2, i.e. chi2 / ndof
  'SV_ndof',     # Number of degrees of freedom
  'SV_ntracks'
]


# ---------------------------------------------------------
# Combine logical sets

MVA_SCALAR_VARS += MODEL_VARS # Treated on the same basis as scalar vars

MVA_PF_VARS     = MVA_CPF_VARS + MVA_NPF_VARS
MVA_JAGGED_VARS = MVA_JET_VARS + MVA_MUON_VARS + MVA_MUONSV_VARS + MVA_SV_VARS #+ MVA_PF_VARS


# ---------------------------------------------------------
# Variables we read out from the root files

LOAD_VARS = []

LOAD_VARS += TRIGGER_VARS
LOAD_VARS += KINEMATIC_VARS
LOAD_VARS += KINEMATIC_GEN_VARS

LOAD_VARS += MVA_SCALAR_VARS
LOAD_VARS += MVA_JAGGED_VARS

# Mutual information regularization targets
MI_VARS = [
  #'muonSV_mass.*' # All
  'muonSV_mass_0'  # The leading one
]

#Adding muonSV charge (filtered)
LOAD_VARS += ['muonSV_charge']

print(LOAD_VARS)

# (regular expressions supported here)
#LOAD_VARS = ['.+hlt.?', '.?gen.?']
#LOAD_VARS = ['.*'] # all

