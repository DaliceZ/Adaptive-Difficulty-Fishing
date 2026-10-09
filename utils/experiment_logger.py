# utils/experiment_logger.py
import csv
import os
from datetime import datetime

LOG_FILE = "experiment_results.csv"
FIELDNAMES = [
    "Timestamp",
    "Player_ID",
    "Mode_Played",
    "Win_Loss",
    "Catch_Duration_Sec",
    "Match_Accuracy",    # เพิ่มเพื่อดูความแม่นยำจริง
    "Baseline_Skill",    # เพิ่มเพื่อดูว่าผู้เล่นเก่งแค่ไหนก่อนเล่น
    "Difficulty_Score",  # คะแนนความยาก (จากแบบสอบถาม)
    "Fun_Score",         # คะแนนความสนุก (จากแบบสอบถาม)
    "DDA_Similarity",    # เหมือนโหมดไหน (จากแบบสอบถาม)
    "DDA_More_Fun",      # สนุกกว่าไหม (จากแบบสอบถาม)
]


def _migrate_csv_header_if_needed(file_path: str) -> None:
    """Ensure CSV header matches FIELDNAMES.

    If an existing file has a different header, rewrite it with the new header and
    preserve any rows by carrying over same-named columns.
    """
    if not os.path.isfile(file_path):
        return

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            existing_header = next(reader, None)
    except IOError:
        return

    if existing_header == FIELDNAMES:
        return

    tmp_path = f"{file_path}.tmp"
    try:
        with open(file_path, "r", newline="", encoding="utf-8") as src, open(
            tmp_path, "w", newline="", encoding="utf-8"
        ) as dst:
            dict_reader = csv.DictReader(src)
            writer = csv.DictWriter(dst, fieldnames=FIELDNAMES)
            writer.writeheader()
            for row in dict_reader:
                migrated = {key: row.get(key, "") for key in FIELDNAMES}
                writer.writerow(migrated)
        os.replace(tmp_path, file_path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

def log_experiment_data(player_id, mode, win_loss, survey_results, catch_duration=None, match_accuracy=None, baseline_skill=None):
    """
    Appends a new row of experiment data to the CSV file.

    Args:
        player_id (str): A unique identifier for the player session.
        mode (str): The difficulty mode that was just played (e.g., "EASY", "DDA").
        win_loss (str): "WIN" or "LOSS".
        survey_results (dict): A dictionary with keys 'Q1', 'Q2', 'Q3' and integer values.
        catch_duration (float | None): Seconds taken for the fishing encounter.
    """

    # Create file and write header if it doesn't exist (or migrate if schema changed)
    file_exists = os.path.isfile(LOG_FILE)
    if file_exists:
        _migrate_csv_header_if_needed(LOG_FILE)

    row_data = {
        "Timestamp": datetime.now().isoformat(),
        "Player_ID": player_id,
        "Mode_Played": mode,
        "Win_Loss": win_loss,
        "Catch_Duration_Sec": catch_duration,
        "Match_Accuracy": match_accuracy,  # <--- [เพิ่มตรงนี้]
        "Baseline_Skill": baseline_skill,  # <--- [เพิ่มตรงนี้]
        "Difficulty_Score": survey_results.get("Q1", ""),
        "Fun_Score": survey_results.get("Q2", ""),
        "DDA_Similarity": survey_results.get("Q3", ""),
        "DDA_More_Fun": survey_results.get("Q4", ""),
    }

    try:
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_data)
        print(f"[Experiment Logger] Successfully logged data for Player {player_id}, Mode {mode}.")
    except IOError as e:
        print(f"[Experiment Logger] Error writing to file: {e}")

