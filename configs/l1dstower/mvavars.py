#L1DS file input (with towers)

# ---------------------------------------------------------
# For plots, diagnostics ...

#KINEMATIC_VARS = [
#    'nL1Jet'
#]

KINEMATIC_VARS = [
    'nL1Jet',
    'nL1EmulCaloTower'
]


KINEMATIC_GEN_VARS = [
  # MC only 
  'GenPart_pt',
  'GenPart_eta',
  'GenPart_phi',
  'GenPart_mass',
  'GenPart_pdgId',
  'GenPart_genPartIdxMother',
  'GenPart_status',
]

# ---------------------------------------------------------
# Pure scalar variables (non-nested)

MVA_SCALAR_VARS = [
    'nL1Jet',
    'nL1EmulCaloTower'
]

MVA_SCALAR_VARS_TOWERS = [
    'nL1EmulCaloTower'
]

MVA_JET_VARS = [
  'L1Jet_pt',
  'L1Jet_eta',
  'L1Jet_phi',
]

MVA_TOWER_VARS = [
  'L1EmulCaloTower_iet',
  'L1EmulCaloTower_ieta',
  'L1EmulCaloTower_iphi',
]

# ---------------------------------------------------------
# Combine logical sets

KINEMATIC_VARS  += KINEMATIC_GEN_VARS
MVA_JAGGED_VARS  = MVA_JET_VARS
MVA_JAGGED_VARS += MVA_TOWER_VARS

# ---------------------------------------------------------
# Variables we read out from the root files

LOAD_VARS = []

LOAD_VARS += KINEMATIC_VARS
LOAD_VARS += MVA_SCALAR_VARS
LOAD_VARS += MVA_JAGGED_VARS

#Mutual information regularization targets
#MI_VARS = [
#    'dijet_deta',
#    'dijet_m'
#]

MI_VARS = [
    'dijet_m'
]