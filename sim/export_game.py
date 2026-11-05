"""Export real sim runs -> game/data.js (binned rates of input/output neurons + active-neuron positions)."""
import json, numpy as np, pandas as pd
a = pd.read_csv('data/ann.tsv', sep='\t', low_memory=False)
a = a.dropna(subset=['pos_x']).drop_duplicates('root_id').set_index('root_id')
ct, sub = a.cell_type.astype(str), a.cell_sub_class.astype(str)
G_IN = {  # what the fly senses (real sensory neuron sets)
  'sweet':   a.index[sub == 'sugar'],
  'bitter':  a.index[sub == 'bitter'],
  'antenna': a.index[ct.str.match(r'^JO-(C|E)')],
  'looming': a.index[ct == 'LPLC2'],
}
G_OUT = {  # where the decision is read out (real motor / descending neurons)
  'feed':   ['CB0700', 'CB0701'],          # feeding motor neurons (MN9-like)
  'escape': ['DNp01'],                     # giant fiber -> jump
  'turn':   ['DNa01', 'DNa02'],            # steering
  'groom':  ['DNg62', 'DNge078'],          # aDN1 / DN2 antennal grooming
}
OUT_IDS = {k: a.index[ct.isin(v)] for k, v in G_OUT.items()}
RUNS = {'sugar': 'results783/sugar', 'coffee': 'results_game/bitter', 'sugar+coffee': 'results_game/sugar+bitter',
        'swatter': 'results783/looming', 'sugar+swatter': 'results_game/sugar+looming', 'fan': 'results_game/jo_ce'}
NB, T = 50, 1.0          # 20 ms bins over 1 s
x, y = a.pos_x, a.pos_y
X0, X1, Y0, Y1 = x.quantile(.001), x.quantile(.999), y.quantile(.001), y.quantile(.999)
nx = lambda v: ((v - X0) / (X1 - X0)).clip(0, 1).round(3)
ny = lambda v: ((v - Y0) / (Y1 - Y0)).clip(0, 1).round(3)
rng = np.random.default_rng(0)
bg = rng.choice(a.index, 5000, replace=False)
out = {'bins_ms': 1000 * T / NB, 'background': list(zip(nx(x[bg]).tolist(), ny(y[bg]).tolist())), 'scenes': {},
       'readouts': {k: {str(i): f'{ct[i]} ({a.side[i]})' for i in v} for k, v in OUT_IDS.items()},
       'source': 'Shiu et al. 2024 LIF model (philshiu/Drosophila_brain_model), FlyWire v783 connectome + annotations'}
for name, p in RUNS.items():
    d = pd.read_parquet(p + '.parquet'); ntr = d.trial.nunique()
    d['b'] = (d.t / T * NB).astype(int).clip(0, NB - 1)
    def series(ids):  # mean rate per neuron (Hz) in each bin, averaged over trials
        s = d[d.flywire_id.isin(ids)].groupby('b').size().reindex(range(NB), fill_value=0)
        return (s / ntr / max(len(ids), 1) / (T / NB)).round(1).tolist()
    def series_max(ids):  # strongest single neuron in group (Hz)
        s = d[d.flywire_id.isin(ids)].groupby(['b', 'flywire_id']).size().groupby('b').max().reindex(range(NB), fill_value=0)
        return (s / ntr / (T / NB)).round(1).tolist()
    rate = d.groupby('flywire_id').size() / ntr / T
    first = d.groupby(['trial', 'flywire_id']).t.min().groupby('flywire_id').median()
    act = rate.index.intersection(a.index)
    keep = act if len(act) <= 3000 else rng.choice(act, 3000, replace=False)
    pts = sorted(([float(nx(x[i])), float(ny(y[i])), round(float(first[i]) * 1000), round(float(rate[i]))] for i in keep), key=lambda q: q[2])
    nact = d.groupby('b').flywire_id.nunique().reindex(range(NB), fill_value=0).tolist()
    out['scenes'][name] = {
        'trials': int(ntr), 'active_total': int(len(rate)),
        'in': {k: series(v) for k, v in G_IN.items()},
        'out': {k: series_max(v) for k, v in OUT_IDS.items()},
        'out_mean_hz': {k: round(float(rate.reindex(v).fillna(0).max()), 1) for k, v in OUT_IDS.items()},
        'active_per_bin': nact, 'points': pts}
    print(name, out['scenes'][name]['active_total'], out['scenes'][name]['out_mean_hz'])
open('data.js', 'w').write('const BRAIN = ' + json.dumps(out, separators=(',', ':')) + ';\n')
import os; print('data.js', os.path.getsize('data.js') // 1024, 'KB')
