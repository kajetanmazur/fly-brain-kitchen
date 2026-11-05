# Fly Brain Kitchen

**Play it:** https://kajetanmazur.github.io/fly-brain-kitchen/

A pixel kitchen with one fruit fly in it. Put down sugar, a drop of bitter coffee, a fan or a swatter and
watch what the fly does. Nobody coded "eat the sugar" or "jump away from the swatter": every decision
comes from a simulation of the real fruit-fly brain.

## How it works

- **The brain** is the whole-brain model from Shiu et al., *A Drosophila computational brain model reveals
  sensorimotor processing*, Nature 2024 ([code](https://github.com/philshiu/Drosophila_brain_model)).
  It is a leaky integrate-and-fire network built from the FlyWire connectome, the wiring diagram of a real
  adult fly brain. We run it on FlyWire v783 (139,255 neurons).
- **Each object switches on a real set of sensory neurons:** sugar = sweet-taste neurons, coffee = bitter-taste
  neurons, fan = antenna (Johnston's organ JO-C/E) neurons, swatter = looming detectors (LPLC2).
- **Each action is read out from real output neurons:** eat = feeding motor neurons (CB0700/CB0701),
  jump = giant fiber (DNp01), clean antennae = grooming descending neurons (DNg62, DNge078),
  steering (DNa01/DNa02) is shown but triggers nothing.
- The model is far too slow to run live in a browser, so each situation was simulated in advance
  (6 trials of 1 s each) and the game replays the recorded activity, slowed down 3 times.
- **Our own game rules (not the brain):** an output neuron above 50 Hz triggers its action (the white line);
  the fly's walking around is random; the "what the fly sees" view is simple geometry.

## What it can't do

**Smells are left out.** In this model, every odour we tried (vinegar, fruity esters, CO2, geosmin), and even heat,
sets off the same runaway storm of about 8,700 neurons, so the fly could not tell them apart. Our trace points
to the excitatory local neurons of the antennal lobe. Our best guess: in real flies they are kept in check by
gap junctions and slow inhibition, which this model (fast chemical synapses only) does not include. Silencing those neurons stops the storm, but that is a lesion,
not the fly's brain, so we did not use it.

## Reproduce the data

`sim/` holds the scripts that produced `data.js`. Clone
[philshiu/Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model) into the repo root (with the
v783 `Completeness_783.csv` and `Connectivity_783.parquet`) and put the FlyWire neuron annotations
(Supplemental file 1 from [flyconnectome/flywire_annotations](https://github.com/flyconnectome/flywire_annotations))
at `data/ann.tsv`. Then:

```bash
python sim/scenes.py sugar looming     # -> results783/
python sim/scenes2.py                  # bitter, antenna, combinations -> results_game/
python sim/export_game.py              # -> data.js
```

## Credits

- Brain model: Shiu et al., Nature 2024, [philshiu/Drosophila_brain_model](https://github.com/philshiu/Drosophila_brain_model) (MIT licence).
- Connectome: the [FlyWire](https://flywire.ai) Consortium, Princeton; v783 data released on Zenodo under CC BY 4.0.
- Neuron annotations and positions: [flyconnectome/flywire_annotations](https://github.com/flyconnectome/flywire_annotations).

Game and scripts: MIT. Built by Kajetan Mazur.
