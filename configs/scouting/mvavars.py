# Looper ROOT file input

# ---------------------------------------------------------
# Conditional (parametric) signal model variables

MODEL_VARS = [
  'MODEL_mpi',
  'MODEL_mA',
  'MODEL_ctau'
]

# ---------------------------------------------------------
# Trigger flag bit variables

TRIGGER_VARS = [
  'L1_DoubleMu_15_7',
  'L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7',
  'L1_DoubleMu4p5_SQ_OS_dR_Max1p2',
  'L1_DoubleMu4_SQ_OS_dR_Max1p2',  
]

# ---------------------------------------------------------
# Pure scalar variables (non-nested)

MVA_SCALAR_VARS = [
]

# ---------------------------------------------------------
# Muons
#
MVA_MUON_VARS = [
  'Muon_pt',
  'Muon_eta',
  'Muon_phi',
  'Muon_phiCorr',
  'Muon_ch',
  'Muon_bestAssocSVIdx',
  'Muon_bestAssocSVOverlapIdx',
  'Muon_isGlobal',
  'Muon_isTracker',
  'Muon_isStandAlone',
  'Muon_chi2Ndof',
  'Muon_dxy',
  'Muon_dxye',
  'Muon_dz',
  'Muon_dze',
  'Muon_dxysig',
  'Muon_dzsig',
  'Muon_ecalIso',
  'Muon_hcalIso',
  'Muon_trackIso',
  'Muon_PFIsoChg0p3',
  'Muon_PFIsoAll0p3',
  'Muon_mindrPF0p3',
  'Muon_nhitsbeforesv',
  'Muon_pixLayers',
  'Muon_trkLayers',
]


# ---------------------------------------------------------
# Secondary vertex

MVA_SV_VARS = [
  'SV_index',   
  'SV_ndof',    
  'SV_x',       
  'SV_y',       
  'SV_z',   
  'SV_xe',       
  'SV_ye',       
  'SV_ze',    
  'SV_chi2',
  'SV_prob',
  'SV_chi2Ndof',
  'SV_lxy',
  'SV_l3d',
  'SV_selected',
  'SV_onModuleWithinUnc',
]

MVA_SVOVERLAP_VARS = [    
  'SV_x',       
  'SV_y',       
  'SV_z',   
  'SV_lxy',
  'SV_l3d',
]

# ---------------------------------------------------------
# Combine logical sets

MVA_SCALAR_VARS += MODEL_VARS         

MVA_JAGGED_VARS  = MVA_MUON_VARS + MVA_SV_VARS + MVA_SVOVERLAP_VARS

# ---------------------------------------------------------
# Variables we read out from the root files

LOAD_VARS = []

LOAD_VARS += TRIGGER_VARS
LOAD_VARS += MVA_SCALAR_VARS
LOAD_VARS += MVA_JAGGED_VARS

# Mutual information regularization targets
MI_VARS = [
  #'SV_mass.*' # All
  'SV_mass_0'  # The leading one
]

#print(LOAD_VARS)

# (regular expressions supported here)
#LOAD_VARS = ['.+hlt.?', '.?gen.?']
#LOAD_VARS = ['.*'] # all