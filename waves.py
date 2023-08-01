import numpy as np

from enum import Enum, auto
from time import time as now

from genres import LOW, MEDIUM, NO_ONE_HERE, VOLUME_RANGE_TO_GENRE

BRIGHTNESS_MULTIPLIER = 254


class WaveType(Enum):
    SINE = auto()
    FLASH = auto()
    CONSTANT = auto()


def wave_state(wave_type: WaveType, phase: float) -> float:
    """Given wave type and time location within the current wave cycle, output state."""
    if wave_type == WaveType.SINE:
        normalized_brightness = 0.5 + 0.5 * np.sin(2 * np.pi * phase)
    elif wave_type == WaveType.FLASH:
        normalized_brightness =  1 if phase < 0.5 else 0
    elif wave_type == WaveType.CONSTANT:
        normalized_brightness = 0.5
    else:
        raise ValueError(f"Unknown wave type: {wave_type}")
    return max(0, min(1, normalized_brightness)) * BRIGHTNESS_MULTIPLIER


def choose_wave(genre: str, num_people: int) -> WaveType:
    if num_people <= 5:
        return WaveType.CONSTANT
    """Given genre and BPM, choose a lighting wave type."""
    if genre in VOLUME_RANGE_TO_GENRE[NO_ONE_HERE].union(VOLUME_RANGE_TO_GENRE[LOW]):
        return WaveType.CONSTANT
    if genre in VOLUME_RANGE_TO_GENRE[MEDIUM]:
        return WaveType.SINE
    return WaveType.FLASH


def lighting_step(wave_type: WaveType, bpm: float, wave_start_time: float) -> float:
    """Given wave type, BPM, and wave start time, return the current lighting step (brightness)."""
    time_from_start = now() - wave_start_time
    wave_cycle_time = 60 / bpm
    wave_cycle_progress = time_from_start % wave_cycle_time
    normalized_wave_cycle_progress = max(0, min(1, wave_cycle_progress / wave_cycle_time))
    return wave_state(wave_type=wave_type, phase=normalized_wave_cycle_progress)
