# Adaptive Difficulty Fishing (DDA Experiment)

A Pygame fishing mini-game built to compare **static difficulty** (EASY/MEDIUM/HARD) against **Dynamic Difficulty Adjustment (DDA)** in a controlled, repeatable **Experiment Mode**. The project includes an in-game survey system and a data analysis script that exports ready-to-use charts and summary statistics.

## Features

- **Dynamic Difficulty Adjustment (DDA):** A DDA manager adjusts encounter parameters during gameplay.
- **Static Difficulty Modes:** EASY, MEDIUM, HARD for baseline comparisons.
- **Dedicated Experiment Mode:** Runs the modes in a fixed order (EASY → MEDIUM → HARD → DDA) and logs every round to a single CSV.
- **Survey System:** Post-round questions captured immediately after each encounter.
- **Data Analysis Exports:** A standalone script generates 6 charts + a summary table from the CSV dataset.

## Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### Install

1. Clone the repository:
     ```bash
     git clone https://github.com/TWFILM/Adaptive-Difficulty-Fishing.git
     cd Adaptive-Difficulty-Fishing
     ```

2. Create and activate a virtual environment (recommended):
     ```bash
     python -m venv venv
     source venv/bin/activate  # Windows: venv\Scripts\activate
     ```

3. Install dependencies:

     - To **run the game only**:
         ```bash
         pip install pygame
         ```

     - To **run data analysis / plotting** (recommended):
         ```bash
         pip install pandas numpy matplotlib seaborn
         ```

## How to Run

Launch the game from the project root:

```bash
python main.py
```

From the lobby you can start a normal game session, or select **Start Experiment** to run the research loop.

## Experiment & Data Collection

Experiment Mode is designed to minimize confounds and keep conditions comparable across participants.

### What gets locked

- **Equipment is locked:** the rod is forced to **Novice Rod** for every experiment round.
- **Fish encounter is controlled:** the fish is locked to **Uncommon**.
- **Fish stats are fixed for comparison:** during experiments the encounter uses:
    - `fish_resilience = 0.75`
    - `fish_progress = 0`
- **Timing is measured:** the time to finish each encounter is recorded as `Catch_Duration_Sec`.

### Survey system

After each round, the participant answers a short survey using keyboard number keys.

- Base questions (all modes):
    - **Q1 Difficulty:** “How HARD was this mode?” (0–9)
    - **Q2 Fun:** “How FUN was this mode?” (0–9)

- Extra questions (DDA only):
    - **Q3 DDA Similarity:** “Which mode did this feel like?” (1=Easy, 2=Medium, 3=Hard)
    - **Q4 DDA More Fun:** “Was this mode MORE FUN?” (0–9)

### Logging & CSV safety

Each experiment round appends one row to `experiment_results.csv`.

The logger includes **header migration**: if the file already exists with an older header, it rewrites the CSV with the new schema while preserving any columns that still match by name.

## Data Output (experiment_results.csv)

Current schema:

| Column | Description |
|---|---|
| Timestamp | ISO timestamp for the row |
| Player_ID | UUID for the participant/session |
| Mode_Played | `EASY`, `MEDIUM`, `HARD`, `DDA` |
| Win_Loss | `WIN` or `LOSS` |
| Catch_Duration_Sec | Seconds spent in the encounter |
| Difficulty_Score | Survey Q1 (0–9) |
| Fun_Score | Survey Q2 (0–9) |
| DDA_Similarity | Survey Q3 (DDA only; 1/2/3) |
| DDA_More_Fun | Survey Q4 (DDA only; 0–9) |

## Data Analysis

The analysis pipeline is implemented in `plot_graph.py`.

### Requirements

```bash
pip install pandas numpy matplotlib seaborn
```

### Generate charts and summary table

Run:

```bash
python plot_graph.py
```

This creates a `Graph/` directory and exports:

- `Graph/1_catch_duration.png` — catch duration by mode (boxplot)
- `Graph/2_difficulty_vs_fun.png` — grouped bars of average difficulty vs fun
- `Graph/3_dda_similarity.png` — DDA similarity perception (pie chart)
- `Graph/4_win_rate.png` — win rate by mode
- `Graph/5_dda_more_fun.png` — distribution of DDA “More Fun” scores
- `Graph/6_flow_state_scatter.png` — difficulty vs fun scatter (colored by mode, with jitter)
- `Graph/summary_stats.csv` — per-mode aggregated statistics (count, win rate %, avg duration, avg difficulty, avg fun)

### Troubleshooting

- If you see errors like `Missing dependency 'matplotlib'`, install the missing package(s) listed in the message.
