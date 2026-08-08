import math

import pytest

from simulator.robot_simulator.gait import gait_phase


def test_gait_phase_after_one_full_cycle():
    left_phase, right_phase = gait_phase(sim_time=1.0, gait_frequency_hz=1.0)

    assert left_phase == pytest.approx(2 * math.pi)
    assert right_phase == pytest.approx(3 * math.pi)


def test_gait_phase_increases_when_time_increases():
    first_left_phase, _ = gait_phase(0.1, 1.0)
    second_left_phase, _ = gait_phase(0.2, 1.0)

    assert second_left_phase > first_left_phase
