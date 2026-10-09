from collections import deque
import numpy as np
import random

# These values can be tuned
PERFORMANCE_HISTORY_LENGTH = 120 # track last 2 seconds (at 60fps)
PERFORMANCE_THRESHOLD_LOW = 0.4  # Below this, player is struggling
PERFORMANCE_THRESHOLD_HIGH = 0.75 # Above this, player is doing well

# Min/max values for interpolation to clamp the DDA effects
MIN_CHAOS_CHANCE = 0.01 # Base chance for jukes/stops
MAX_CHAOS_CHANCE = 0.04 # Max chance when player is expert

MIN_RESILIENCE_MOD = -0.5 # Seconds to SUBTRACT from resilience (easier)
MAX_RESILIENCE_MOD = 0.8  # Seconds to ADD to resilience (harder)

MIN_PROGRESS_MOD = 0.2    # Bonus to catch speed (easier)
MAX_PROGRESS_MOD = -0.3   # Malus to catch speed (harder)

MIN_SPEED_ADJ = -0.01   # Speed adjustment when struggling
MAX_SPEED_ADJ = 0.008   # Speed adjustment when doing well

class DDAManager:
    """
    Manages dynamic difficulty by tracking player performance and adjusting
    multiple gameplay parameters in real-time to maintain a 'flow state'.
    """
    def __init__(self, fish_resilience, fish_progress, baseline_skill=0.5): # เพิ่ม baseline_skill
        self.catching_history = deque(maxlen=PERFORMANCE_HISTORY_LENGTH)

        # ใส่ประวัติจำลองตอนเริ่มเกมตามฝีมือที่ประเมินได้
        for _ in range(PERFORMANCE_HISTORY_LENGTH):
            self.catching_history.append(1 if random.random() < baseline_skill else 0)

        self.performance_metric = baseline_skill  # เริ่มต้นตามฝีมือจริง

        # Store base values of the current fish to modify
        self.base_resilience = fish_resilience
        self.base_progress = fish_progress

    def update(self, is_catching):
        """Call this every frame to update the performance tracker."""
        self.catching_history.append(is_catching)

        # Only update the metric once the history is full to avoid wild swings at the start
        if len(self.catching_history) == self.catching_history.maxlen:
            # Calculate performance as the ratio of time spent catching
            current_performance = sum(self.catching_history) / len(self.catching_history)
            # Smooth the performance metric using an exponential moving average to avoid drastic changes
            self.performance_metric = (self.performance_metric * 0.98) + (current_performance * 0.02)
            self.performance_metric = np.clip(self.performance_metric, 0, 1)

    def adjust_fish_speed(self, current_speed, is_catching):
        """Adjusts fish speed based on both immediate state and overall performance."""
        # Immediate adjustment
        if not is_catching:
            current_speed -= 0.005 # Player is not on the fish, slow it down a bit

        # Performance-based adjustment
        if self.performance_metric > PERFORMANCE_THRESHOLD_HIGH:
            # Player is doing well, make it harder over time
            adjustment = np.interp(self.performance_metric, [PERFORMANCE_THRESHOLD_HIGH, 1], [0, MAX_SPEED_ADJ])
            return min(4.0, current_speed + adjustment)
        elif self.performance_metric < PERFORMANCE_THRESHOLD_LOW:
            # Player is struggling, make it easier over time
            adjustment = np.interp(self.performance_metric, [0, PERFORMANCE_THRESHOLD_LOW], [MIN_SPEED_ADJ, 0])
            return max(0.5, current_speed + adjustment)

        # Ensure speed is always within a valid range
        return np.clip(current_speed, 0.5, 4.0)

    def get_chaos_chance(self):
        """
        Gets the dynamic probability of the fish performing an unpredictable
        'chaos' move (juke or sudden stop).
        """
        # Scale chaos chance based on performance
        return np.interp(self.performance_metric, [0, 1], [MIN_CHAOS_CHANCE, MAX_CHAOS_CHANCE])

    def get_modified_resilience(self):
        """
        Calculates the fish's waiting time between movements. Higher performance
        leads to higher resilience, meaning shorter pauses for the player.
        """
        modifier = np.interp(self.performance_metric, [0, 1], [MIN_RESILIENCE_MOD, MAX_RESILIENCE_MOD])
        return max(0.1, self.base_resilience + modifier) # Ensure resilience is never zero or negative

    def get_modified_progress(self):
        """
        Calculates the catch progress speed. Higher performance leads to a
        progress penalty, requiring the player to be more precise for longer.
        """
        modifier = np.interp(self.performance_metric, [0, 1], [MIN_PROGRESS_MOD, MAX_PROGRESS_MOD])
        return self.base_progress + modifier

def update_fish_speed(is_catching, fish_speed):
    """Legacy function, kept for non-DDA modes if needed."""
    if is_catching:
        return min(3.0, fish_speed + 0.001)
    else:
        return max(0.5, fish_speed - 0.005)
