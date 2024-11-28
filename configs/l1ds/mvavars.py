#L1DS file input

# ---------------------------------------------------------
# For plots, diagnostics ...

KINEMATIC_VARS = [
    'nJet'
]


KINEMATIC_GEN_VARS = [
  # MC only 
  'GenJet_pt',
  'GenJet_eta',
  'GenJet_phi',
  'GenJet_mass'
]

# ---------------------------------------------------------
# Pure scalar variables (non-nested)


MVA_SCALAR_VARS = [
    'nJet'
]

MVA_JET_VARS = [
  'Jet_pt',
  'Jet_eta',
  'Jet_phi',
]

# ---------------------------------------------------------
# Combine logical sets

KINEMATIC_VARS  += KINEMATIC_GEN_VARS
MVA_JAGGED_VARS  = MVA_JET_VARS

# ---------------------------------------------------------
# Variables we read out from the root files

LOAD_VARS = []

LOAD_VARS += KINEMATIC_VARS
LOAD_VARS += MVA_SCALAR_VARS
LOAD_VARS += MVA_JAGGED_VARS

#Mutual information regularization targets
#MI_VARS = [
#    'dijet_m'
#]

#MI_VARS = [
#    'dijet_deta'
#]

MI_VARS = [
    'dijet_deta',
    'dijet_m'
]