from enum import Enum
from time import time as now

class WaveType(Enum):
    SINE = 1
    SQUARE = 2
    TRIANGLE = 3
    SAWTOOTH = 4


def wave_state(wave_type: WaveType, phase: float) -> float:
    """Given wave type and time location within the current wave cycle, output state."""


def choose_wave(genre: str, bpm: float) -> WaveType:
    """Given genre and BPM, choose a lighting wave type."""


def lighting_step(wave_type: WaveType, bpm: float, wave_start_time: float) -> float:
    """Given wave type, BPM, and wave start time, return the current lighting step (brightness)."""
    time_from_start = now() - wave_start_time
    wave_cycle_time = 60 / bpm
    wave_cycle_progress = time_from_start % wave_cycle_time
    normalized_wave_cycle_progress = max(0, min(1, wave_cycle_progress / wave_cycle_time))
    return wave_state(wave_type=wave_type, phase=normalized_wave_cycle_progress)
