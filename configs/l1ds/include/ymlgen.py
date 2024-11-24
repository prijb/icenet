# Automated YAML-file generation
# Modified for L1DS
#
# prijith.babu-pradeep18@imperial.ac.uk, 2024

import argparse
import os

#Writes a new line to the output file
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

  for mZ in rp['mZ']:

    #MC signal
    if isMC == 'true' and mZ != 'null':
      process_name = f'{process}_{mZ}'
      folder_name  = f'{process_name}'

    #MC background
    elif isMC == 'true' and mZ == 'null':
      process_name = f'{process}'
      folder_name  = f'{process_name}'
    
    #Data
    else:
      process_name = f'{process}'
      folder_name  = f'{end_name}'

    #Print
    dprint(outputfile, f'# [{i}]')
    dprint(outputfile, f'{process_name}: &{process_name}')
    dprint(outputfile, f"  path:  \'{folder_name}\'")
    dprint(outputfile, f"  files: \'{filename}\'")
    dprint(outputfile, f'  xs:   {xs}')
    dprint(outputfile, f'  model_param:')
    dprint(outputfile, f'    mZ: {str2float(mZ)}')
    dprint(outputfile, f'  force_xs: {force_xs}')
    dprint(outputfile, f'  isMC:     {isMC}')
    dprint(outputfile, f'  maxevents_scale: {maxevents_scale}')
    dprint(outputfile, f'')

    i += 1

#Process definition
def zprime(outputfile, filerange='*'):

  #The process name steers the pathname
  process = 'ztoqq_mlm'

  # ------------------------------------------
  # Basic
  filename        = f'output_{filerange}.root'
  path            = ''
  end_name        = ''
  xs              = '1.0 # [pb]'
  force_xs        = 'true'
  isMC            = 'true'
  maxevents_scale = '1.0'
  # ------------------------------------------

  rp = {}
  rp['mZ'] = ['250', '350']

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


def QCD(outputfile, filerange='*'):

  processes = [ \
    #{'path':     '',
    #  'process':  'QCD_15to30',
    #  'end_name': '',
    #  'xs': 1.306e+09
    #},
    {'path':     '',
      'process':  'QCD_30to50',
      'end_name': '',
      'xs': 1.126e+08
    },
    {'path':     '',
      'process':  'QCD_50to80',
      'end_name': '',
      'xs': 1.669e+07
    },
    {'path':     '',
      'process':  'QCD_80to120',
      'end_name': '',
      'xs': 2.506e+06
    }
  ]
  
  rp = {}

  rp['mZ'] = ['null']
  pfunc = printer

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
      pfunc(**param)
    else:
      pfunc(**param, flush_index=i)

     


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

  if args.process == 'zprime':
    zprime(outputfile=outputfile, filerange=args.filerange)
  
  elif args.process == 'QCD':
    QCD(outputfile=outputfile, filerange=args.filerange)

  else:
    print('Error: unknown --process chosen (run --help)')

  print(f'Saved to file "{outputfile}"')
