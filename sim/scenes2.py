"""Game stimuli validated in Shiu et al. (bitter, water, JO touch) + combos, on FlyWire v783. 6 trials, 150 Hz."""
import sys
from brian2 import Hz
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes.py')).read().split("only = sys.argv")[0]; ns = {}; exec(src, ns)
S, cfg, params, run_exp, a, known = ns['SCENES'], ns['cfg'], ns['params'], ns['run_exp'], ns['a'], ns['known']
ct = a.cell_type.astype(str)
k = lambda ids: [i for i in ids if i in known]
S['bitter'] = k(a[a.cell_sub_class == 'bitter'].root_id)
S['water'] = k(a[a.cell_sub_class == 'water'].root_id)
S['jo_ce'] = k(a[ct.str.match(r'^JO-(C|E)')].root_id)   # antenna displacement (air puff / touch)
S['jo_f'] = k(a[ct.str.match(r'^JO-F')].root_id)        # antenna grooming-trigger JONs
COMBOS = {'sugar+bitter': ('sugar', 'bitter'), 'sugar+water': ('sugar', 'water'), 'sugar+looming': ('sugar', 'looming')}
cfg['path_res'] = './results_game'
params['r_poi2'] = 150 * Hz
todo = sys.argv[1:] or ['bitter', 'water', 'jo_ce', 'jo_f', *COMBOS]
for name in todo:
    if name in COMBOS:
        x, y = COMBOS[name]; print(name, flush=True)
        run_exp(exp_name=name, neu_exc=S[x], neu_exc2=S[y], params=params, **cfg)
    else:
        print(name, len(S[name]), flush=True)
        run_exp(exp_name=name, neu_exc=S[name], params=params, **cfg)
