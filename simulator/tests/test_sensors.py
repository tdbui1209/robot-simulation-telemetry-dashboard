import math

import pytest

from simulator.robot_simulator.sensors import (
    CONTACT_FORCE_RATIO,
    GRAVITY,
    IMU_ACCEL_X_AMPLITUDE,
    IMU_ACCEL_Y_AMPLITUDE,
    SWING_FORCE_RATIO,
    generate_sensors,
)


def test_generate_sensors_returns_expected_schema():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60)

    assert "imu" in sensors
    assert "acceleration" in sensors["imu"]
    assert "ax" in sensors["imu"]["acceleration"]
    assert "ay" in sensors["imu"]["acceleration"]
    assert "az" in sensors["imu"]["acceleration"]
    assert "foot_contact" in sensors


def test_left_and_right_contact_are_opposite_for_opposite_phases():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60)

    assert sensors["foot_contact"]["left"] is True
    assert sensors["foot_contact"]["right"] is False


def test_contact_force_is_higher_than_swing_force():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60)

    assert sensors["foot_contact"]["left_force"] > sensors["foot_contact"]["right_force"]


def test_contact_and_swing_force_values_are_expected():
    mass_kg = 60
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, mass_kg)

    assert sensors["foot_contact"]["left_force"] == pytest.approx(
        mass_kg * GRAVITY * CONTACT_FORCE_RATIO
    )
    assert sensors["foot_contact"]["right_force"] == pytest.approx(
        mass_kg * GRAVITY * SWING_FORCE_RATIO
    )


def test_imu_acceleration_values_are_expected_at_positive_peak():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60)

    acceleration = sensors["imu"]["acceleration"]

    assert acceleration["ax"] == pytest.approx(IMU_ACCEL_X_AMPLITUDE)
    assert acceleration["ay"] == pytest.approx(IMU_ACCEL_Y_AMPLITUDE)
    assert acceleration["az"] == pytest.approx(GRAVITY)
