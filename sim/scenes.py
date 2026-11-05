"""Feasibility: 7 stimuli on FlyWire v783 brain model, left-side only; read out descending/motor neurons."""
import sys, time
sys.path.insert(0, 'Drosophila_brain_model')
import pandas as pd
from model import run_exp, default_params as params
import utils as utl
a = pd.read_csv('data/ann.tsv', sep='\t', low_memory=False)
ct, side = a.cell_type.astype(str), a.side.astype(str)
def orn(*gl, s='left'): return a[ct.isin([f'ORN_{g}' for g in gl]) & (side == s)].root_id.tolist()
SCENES = {
  'sugar':    a[a.cell_sub_class == 'sugar'].root_id.tolist(),            # both sides, taste
  'vinegar':  orn('DM1', 'DM4', 'DP1m'),                                 # acetic acid / ACV (literature, to verify)
  'fruity':   orn('DM2', 'DM3'),                                         # fruity esters (to verify)
  'co2':      orn('V'),                                                  # CO2 (breath)
  'geosmin':  orn('DA2'),                                                # mould, known aversive
  'heat':     a[(ct == 'TRN_VP2') & (side == 'left')].root_id.tolist(),  # hot cells (to verify)
  'looming':  a[(ct == 'LPLC2') & (side == 'left')].root_id.tolist(),    # approaching object (swatter)
}
params['n_run'] = 6
cfg = dict(path_res='./results783', path_comp='Drosophila_brain_model/Completeness_783.csv',
           path_con='Drosophila_brain_model/Connectivity_783.parquet', n_proc=-1)
known = set(pd.read_csv(cfg['path_comp']).iloc[:, 0])
SCENES = {k: [i for i in v if i in known] for k, v in SCENES.items()}
only = sys.argv[1:] or list(SCENES)
for name in only:
    print(name, len(SCENES[name]), 'neurons', flush=True)
    run_exp(exp_name=name, neu_exc=SCENES[name], params=params, **cfg)
