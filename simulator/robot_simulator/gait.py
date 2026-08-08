import math


def gait_phase(sim_time: float, gait_frequency_hz: float) -> tuple[float, float]:
    """
    Calculate the gait phases for a periodic walking cycle. 
    Returns the phases for two legs that are opposite in phase.
    """
    phase = 2 * math.pi * gait_frequency_hz * sim_time
    return phase, phase + math.pi
