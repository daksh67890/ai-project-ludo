# AI Ludo - Authentic Edition

A high-performance Python implementation of the classic Ludo board game featuring authentic board artwork matching the plan asset, four core AI agents, and a headless tournament benchmarking suite.

## The Core AI Agents

1. **Expectiminimax (`expectiminimax`)**: Depth-limited game tree search with chance nodes for the dice, Star1 alpha-beta pruning, heuristic move ordering, and a transposition table that stores only exact values. In 3 and 4-player games every opponent is treated as a minimiser (paranoid assumption). Depth 2 costs about 1 to 3 ms per move; depth 3 about 17 to 20 ms.
2. **Greedy (`greedy`)**: Fast 1-ply heuristic evaluation baseline.
3. **Tuned (`tuned`)**: A Greedy agent that loads the weights found by the simulated annealing tuner (`optimization/tuned_weights.json`). In our validation the tuner did not find weights better than the defaults, so this agent plays like Greedy (see `experiments/RESULTS.md`).
4. **Random (`random`)**: Uniform random baseline mover. It accepts a seed, so tournaments are reproducible.

## Authentic Board Artwork & UI Features

- **Authentic Asset Styling**: Faithfully styled after the plan asset:
  - Deep indigo background (`#2c2b67`).
  - Warm rounded peach-caramel wooden outer frame (`#ff9d5b`).
  - Standard quadrants: Top-Left (Red), Top-Right (Green), Bottom-Right (Yellow), Bottom-Left (Blue).
  - 8 Star safe tiles with circular badges.
  - Inward-pointing directional entry arrows (`▶`, `▼`, `◀`, `▲`).
  - Center 3×3 diagonal home triangles.
  - 3D pawns with golden metallic rims and bottom display tray.
- **Player Enhancements**:
  - Numbered token badges (`1`, `2`, `3`, `4`) directly on the board.
  - Tactical landing preview (highlights destination tile with capture crosshairs `⚔️` or finish star `★`).
  - Animated 3D die with pips and rolling effect.
  - Live match event feed logging all rolls, captures, and victories.
  - Watch speed controls (*Slow*, *Normal*, *Fast*, *Turbo*).
  - Move undo support for human play.
  - Procedural sound effects using Python's standard library `winsound` with a mute toggle.
  - Configurable game rules (extra turns, three 6s forfeit, exact finish, blockades).

---

## Quickstart

### Launch the GUI
```powershell
.\.venv\Scripts\python.exe -m gui.app
```

If `.venv` is missing, initialize it once:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Run Unit Tests
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### Run a Headless Benchmark Tournament
```powershell
.\.venv\Scripts\python.exe -m experiments.tournament --agents random greedy expectiminimax tuned --games 1200 --players 2 --depth 2 --seed 2026 --csv experiments/results_2p.csv
.\.venv\Scripts\python.exe -m experiments.tournament --agents random greedy expectiminimax tuned --games 1000 --players 4 --depth 2 --seed 2026 --csv experiments/results_4p.csv
.\.venv\Scripts\python.exe -m experiments.plots experiments/results_2p.csv --output experiments/results_2p.png
```
With 2 players and three or more agents, the runner plays a balanced round robin: every ordered pair of agents plays the same number of games, so each agent meets every other agent equally often and plays both seats equally often.

### Compare Plain Search, Alpha-Beta and Alpha-Beta + Table
```powershell
.\.venv\Scripts\python.exe -m experiments.search_benchmark
```
Writes `experiments/search_benchmark.csv` and `experiments/search_benchmark.png`.

### Tune Weights via Self-Play
```powershell
.\.venv\Scripts\python.exe -m optimization.tuner --iterations 150 --games 100 --final-games 600 --validate 2000 --seed 7
```
The best candidates are replayed on fresh games before the winner is chosen, and the result is checked on 2000 held-out games against the default weights.

---

## Benchmark Summary

Depth-2 search, seed 2026, default rules, all games completed. The margin is the 95% interval.

| Agent | Algorithm | 2-Player Win % (600 games each) | 4-Player Win % (1000 games each) | Avg Move Time (2P / 4P) |
| :--- | :--- | :---: | :---: | :---: |
| **Expectiminimax** | Depth-2 Expectiminimax + Alpha-Beta + Table | **62.3% +/- 3.9** | **33.5% +/- 2.9** | 1.3 ms / 2.5 ms |
| **Tuned** | Greedy with SA-tuned weights (= default weights) | **53.8% +/- 4.0** | **25.9% +/- 2.7** | 0.06 ms / 0.10 ms |
| **Greedy** | 1-Ply Heuristic Baseline | **52.8% +/- 4.0** | **27.7% +/- 2.8** | 0.05 ms / 0.09 ms |
| **Random** | Uniform Random Baseline | **31.0% +/- 3.7** | **12.9% +/- 2.1** | < 0.01 ms |

In a 4-player game an equal share is 25%. In the 2-player round robin each agent plays all three opponents, so Random's 31% is not 50%.

See [experiments/RESULTS.md](experiments/RESULTS.md) for the head-to-head matrix, search cost, tuning results, and methodology.
