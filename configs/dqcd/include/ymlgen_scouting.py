# Automated YAML-file generation
#
# m.mieskolainen@imperial.ac.uk, 2022

import argparse
import os

def dprint(outputfile, string, mode='a'):
  print(string)
  with open(outputfile, mode) as f:
    f.write(f'{string} \n')

def str2float(x):
  """
  Conversion from '10p1' type str representation to float
  """
  if x == 'null':
    return x
  
  if type(x) is str:
    return float(x.replace('p','.'))
  elif type(x) is float:
    return x
  else:
    raise Exception(f'str2float: Input {x} should be either str or float')


def printer(outputfile, process, path, end_name, filename, xs, force_xs, isMC, maxevents_scale, rp, flush_index=0):
  
  if flush_index == 0:
    dprint(outputfile, '', 'w') # Empty it

  i = flush_index
  for m in rp['m']:
    for ctau in rp['ctau']:
      for xi_pair in rp['xi_pair']:

        # MC signal
        if isMC == 'true' and m != 'null':
          param_name   = f'm_{m}_ctau_{ctau}_xiO_{xi_pair[0]}_xiL_{xi_pair[1]}'
          process_name = f'{process}_{param_name}'  
          folder_name  = f'{process_name}_{end_name}'

        # MC background
        elif isMC == 'true' and m == 'null':
          process_name = f'{process}'  
          folder_name  = f'{process_name}'
          #Commented this because the yaml generation adds an extra underscore
          #folder_name  = f'{process_name}_{end_name}
        
        # Data
        else:
          process_name = f'{process}'
          folder_name  = f'{end_name}'

        # Print
        dprint(outputfile, f'# [{i}]')
        dprint(outputfile, f'{path}--{process_name}: &{path}--{process_name}')
        dprint(outputfile, f"  path:  \'{path}/{folder_name}\'")
        dprint(outputfile, f"  files: \'{filename}\'")
        dprint(outputfile, f'  xs:   {xs}')
        dprint(outputfile, f'  model_param:')
        dprint(outputfile, f'    m:    {str2float(m)}')
        dprint(outputfile, f'    ctau: {str2float(ctau)}')
        dprint(outputfile, f'    xiO:  {str2float(xi_pair[0])}')
        dprint(outputfile, f'    xiL:  {str2float(xi_pair[1])}')
        dprint(outputfile, f'  force_xs: {force_xs}')
        dprint(outputfile, f'  isMC:     {isMC}')
        dprint(outputfile, f'  maxevents_scale: {maxevents_scale}')
        dprint(outputfile, f'')

        i += 1


def printer_newmodels(outputfile, process, path, end_name, filename, xs, force_xs, isMC, maxevents_scale, rp, flush_index=0):
  
  if flush_index == 0:
    dprint(outputfile, '', 'w') # Empty it

  i = flush_index
  for mpi_mA_pair in rp['mpi_mA_pair']:
      for ctau in rp['ctau']:

        # MC signal
        if isMC == 'true' and mpi_mA_pair[0] != 'null':
          param_name   = f'mpi_{mpi_mA_pair[0]}_mA_{mpi_mA_pair[1]}_ctau_{ctau}'
          process_name = f'{process}_{param_name}'  
          folder_name  = f'{process_name}'

        # MC background
        elif isMC == 'true' and mpi_mA_pair[0] == 'null':
          process_name = f'{process}'  
          folder_name  = f'{process_name}'
          #Commented this because the yaml generation adds an extra underscore
          #folder_name  = f'{process_name}_{end_name}'
        
        # Data
        else:
          process_name = f'{process}'
          folder_name  = f'{end_name}'

        # Print
        dprint(outputfile, f'# [{i}]')
        dprint(outputfile, f'{path}--{process_name}: &{path}--{process_name}')
        dprint(outputfile, f"  path:  \'{path}/{folder_name}\'")
        dprint(outputfile, f"  files: \'{filename}\'")
        dprint(outputfile, f'  xs:   {xs}')
        dprint(outputfile, f'  model_param:')
        dprint(outputfile, f'    mpi:    {str2float(mpi_mA_pair[0])}')
        dprint(outputfile, f'    mA:     {str2float(mpi_mA_pair[1])}')
        dprint(outputfile, f'    ctau:   {str2float(ctau)}')
        dprint(outputfile, f'  force_xs: {force_xs}')
        dprint(outputfile, f'  isMC:     {isMC}')
        dprint(outputfile, f'  maxevents_scale: {maxevents_scale}')
        dprint(outputfile, f'')

        i += 1


def darkphoton(outputfile, filerange='*'):
  
  process         = 'HiddenValley_darkphoton'

  # ------------------------------------------
  # Basic
  filename        = f'output_{filerange}.root'
  path            = 'bparkProductionV3'
  end_name        = 'privateMC_11X_NANOAODSIM_v3_generationForBParking'
  xs              = '1.0 # [pb]'
  force_xs        = 'true'
  isMC            = 'true'
  maxevents_scale = '1.0'
  # ------------------------------------------

  rp = {}
  rp['m']         = ['2', '5', '10', '15']
  rp['ctau']      = ['10', '50', '100', '500'] 
  rp['xi_pair']   = [['1', '1'], ['2p5', '1'], ['2p5', '2p5']]

  param = {
    'outputfile':      outputfile,
    'rp':              rp,
    'process':         process,
    'path':            path,
    'end_name':        end_name,
    'filename':        filename,
    'xs':              xs,
    'force_xs':        force_xs,
    'isMC':            isMC,
    'maxevents_scale': maxevents_scale
  }
  printer(**param)


def vector(outputfile, filerange='*'):

  process         = 'HiddenValley_vector'

  # ------------------------------------------
  # Basic
  filename        = f'output_{filerange}.root'
  path            = 'bparkProductionAll_V1p0'
  end_name        = 'privateMC_11X_NANOAODSIM_v1p0_generationSync'
  xs              = '1.0 # [pb]'
  force_xs        = 'true'
  isMC            = 'true'
  maxevents_scale = '1.0'
  # ------------------------------------------
  
  rp = {}
  rp['m']         = ['2', '5', '10', '15', '20']
  rp['ctau']      = ['1', '10', '50', '100', '500'] 
  rp['xi_pair']   = [['1', '1']]
  
  param = {
    'outputfile':      outputfile,
    'rp':              rp,
    'process':         process,
    'path':            path,
    'end_name':        end_name,
    'filename':        filename,
    'xs':              xs,
    'force_xs':        force_xs,
    'isMC':            isMC,
    'maxevents_scale': maxevents_scale
  }
  printer(**param)


def higgs(outputfile, filerange='*'):

  process         = 'HiddenValley_higgs'

  # ------------------------------------------
  # Basic
  filename        = f'output_{filerange}.root'
  path            = 'bparkProductionV2'
  end_name        = 'privateMC_11X_NANOAODSIM_v2_generationForBParking'
  xs              = '1.0 # [pb]'
  force_xs        = 'true'
  isMC            = 'true'
  maxevents_scale = '1.0'
  # ------------------------------------------
  
  rp = {}
  rp['m']         = ['10', '15', '20']
  rp['ctau']      = ['10', '50', '100', '500'] 
  rp['xi_pair']   = [['1', '1'], ['2p5', '1'], ['2p5', '2p5']]
  
  param = {
    'outputfile':      outputfile,
    'rp':              rp,
    'process':         process,
    'path':            path,
    'end_name':        end_name,
    'filename':        filename,
    'xs':              xs,
    'force_xs':        force_xs,
    'isMC':            isMC,
    'maxevents_scale': maxevents_scale
  }
  printer(**param)

def scenarioA(outputfile, filerange='*'):

  process         = 'scenarioA'

  # ------------------------------------------
  # Basic
  filename        = f'output_{filerange}.root'
  path            = 'StoreNTuple/DQCD_v2/Run3/Scouting'
  end_name        = ''
  xs              = '1.0 # [pb]'
  force_xs        = 'true'
  isMC            = 'true'
  maxevents_scale = '1.0'
  # ------------------------------------------
  
  rp = {}
  rp['mpi_mA_pair']  = [['4','1p33']]
  rp['ctau']         = ['10']
  
  param = {
    'outputfile':      outputfile,
    'rp':              rp,
    'process':         process,
    'path':            path,
    'end_name':        end_name,
    'filename':        filename,
    'xs':              xs,
    'force_xs':        force_xs,
    'isMC':            isMC,
    'maxevents_scale': maxevents_scale
  }
  printer_newmodels(**param)


def QCD(outputfile, filerange='*'):
  #Need to complete xs estimation
  processes = [ \
  {'path':     'qcd_scouting_new/qcd_15to20',
   'process':  '',
   'end_name': '',
   'xs': 2982000.0} # pb
  ,
  
  {'path':     'qcd_scouting_new/qcd_20to30',
   'process':  '',
   'end_name': '',
   'xs': 2679000.0 }
  ,

  {'path':     'qcd_scouting_new/qcd_30to50',
   'process':  '',
   'end_name': '',
   'xs': 1497000.0}
  ,

  {'path':     'qcd_scouting_new/qcd_50to80',
   'process':  '',
   'end_name': '',
   'xs': 402900.0}
  ,

  {'path':     'qcd_scouting_new/qcd_80to120',
   'process':  '',
   'end_name': '',
   'xs': 96200.0} 
  ,

  {'path':     'qcd_scouting_new/qcd_120to170',
   'process':  '',
   'end_name': '',
   'xs': 22980.0}  
  ,

  {'path':     'qcd_scouting_new/qcd_170to300',
   'process':  '',
   'end_name': '',
   'xs': 7055.0}
  ,
  
  {'path':     'qcd_scouting_new/qcd_300to470',
   'process':  '',
   'end_name': '',
   'xs': 699.1} 
  ,

  {'path':     'qcd_scouting_new/qcd_470to600',
   'process':  '',
   'end_name': '',
   'xs': 59.24}
  ,

  {'path':     'qcd_scouting_new/qcd_600to800',
   'process':  '',
   'end_name': '',
   'xs': 21.37}
  ,

  {'path':     'qcd_scouting_new/qcd_800to1000',
   'process':  '',
   'end_name': '',
   'xs': 3.913}
  ,

  {'path':     'qcd_scouting_new/qcd_1000toInf',
   'process':  '',
   'end_name': '',
   'xs': 1.078} ]
  
  rp = {}

  #old models
  '''
  rp['m']       = ['null']
  rp['ctau']    = ['null'] 
  rp['xi_pair'] = [['null', 'null']]
  '''
  
  #new models
  rp['mpi_mA_pair'] = [['null', 'null']]
  rp['ctau']        = ['null']

  for i in range(len(processes)):

    # ------------------------------------------
    # Basic
    filename        = f'output_{filerange}.root'
    force_xs        = 'false'
    isMC            = 'true'
    maxevents_scale = '1.0'
    # ------------------------------------------

    param = {
      'outputfile':      outputfile,
      'rp':              rp,
      'process':         processes[i]['process'],
      'path':            processes[i]['path'],
      'end_name':        processes[i]['end_name'],
      'filename':        filename,
      'xs':              processes[i]['xs'],
      'force_xs':        force_xs,
      'isMC':            isMC,
      'maxevents_scale': maxevents_scale
    }

    if i == 0:
      printer_newmodels(**param)
    else:
      printer_newmodels(**param, flush_index=i)



def data(outputfile, filerange='*'):

  processes = None
    
  processes = [
  {'path':     'StoreNTuple/Scouting22F/Nanotronv2',
    'process':  '',
    'end_name': ''
  }
  ]

  rp              = {}
  rp['m']         = ['null']
  rp['ctau']      = ['null'] 
  rp['xi_pair']   = [['null', 'null']]
  rp['xi2str']    = ['null']
  
  for i in range(len(processes)):

    # ------------------------------------------
    # Basic
    filename        = f'output_{filerange}.root'
    force_xs        = 'false'
    isMC            = 'false'
    xs              = '2799000.0'
    maxevents_scale = '1.0'
    # ------------------------------------------

    param = {
      'outputfile':      outputfile,
      'rp':              rp,
      'process':         processes[i]['process'],
      'path':            processes[i]['path'],
      'end_name':        processes[i]['end_name'],
      'filename':        filename,
      'xs':              xs,
      'force_xs':        force_xs,
      'isMC':            isMC,
      'maxevents_scale': maxevents_scale
    }

    if i == 0:
      printer(**param)
    else:
      printer(**param, flush_index=i)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generate some YAML-files.')
  parser.add_argument('--process',    type=str, default='vector')
  parser.add_argument('--filerange',  type=str, default='*')
  parser.add_argument('--outputfile', type=str, default=None)
  args = parser.parse_args()
  
  if args.outputfile is None:
    # By default, we write to the path of this python script
    path = os.path.abspath(os.path.dirname(__file__))
    outputfile = f'{path}/{args.process}.yml'
  else:
    outputfile = args.outputfile

  if   args.process == 'vector':
    vector(outputfile=outputfile, filerange=args.filerange)

  elif args.process == 'higgs':
    higgs(outputfile=outputfile, filerange=args.filerange)

  elif args.process == 'darkphoton':
    darkphoton(outputfile=outputfile, filerange=args.filerange)
  
  elif args.process == 'scenarioA':
    scenarioA(outputfile=outputfile, filerange=args.filerange)

  elif args.process == 'QCD':
    QCD(outputfile=outputfile, filerange=args.filerange)
  
  elif args.process == 'data':
    data_scouting(outputfile=outputfile, filerange=args.filerange)
  
  else:
    print('Error: unknown --process chosen (run --help)')

  print(f'Saved to file "{outputfile}"')
