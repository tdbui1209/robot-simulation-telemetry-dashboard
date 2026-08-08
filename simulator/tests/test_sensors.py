import math

import pytest

from simulator.robot_simulator import sensors
from simulator.robot_simulator.sensors import (
    CONTACT_FORCE_RATIO,
    GRAVITY,
    IMU_ACCEL_X_AMPLITUDE,
    IMU_ACCEL_Y_AMPLITUDE,
    SWING_FORCE_RATIO,
    GYRO_X_AMPLITUDE,
    GYRO_Y_AMPLITUDE,
    GYRO_Z_AMPLITUDE,
    generate_sensors,
)


def test_generate_sensors_returns_expected_schema():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60, 1, 2, 3)

    assert "imu" in sensors
    assert "acceleration" in sensors["imu"]
    assert "gyroscope" in sensors["imu"]
    assert "ax" in sensors["imu"]["acceleration"]
    assert "ay" in sensors["imu"]["acceleration"]
    assert "az" in sensors["imu"]["acceleration"]
    assert "gx" in sensors["imu"]["gyroscope"]
    assert "gy" in sensors["imu"]["gyroscope"]
    assert "gz" in sensors["imu"]["gyroscope"]
    assert "foot_contact" in sensors


def test_left_and_right_contact_are_opposite_for_opposite_phases():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60, 1, 2, 3)

    assert sensors["foot_contact"]["left"] is True
    assert sensors["foot_contact"]["right"] is False


def test_contact_force_is_higher_than_swing_force():
    sensors = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60, 1, 2, 3)

    assert sensors["foot_contact"]["left_force"] > sensors["foot_contact"]["right_force"]


def test_contact_and_swing_force_values_are_expected(monkeypatch):
    monkeypatch.setattr(
        sensors.random,
        "gauss",
        lambda *args, **kwargs: 5.0,
    )

    mass_kg = 60
    results = generate_sensors(math.pi / 2, 3 * math.pi / 2, mass_kg, 1, 2, 3)

    assert results["foot_contact"]["left_force"] == pytest.approx(
        mass_kg * GRAVITY * CONTACT_FORCE_RATIO + 5
    )
    assert results["foot_contact"]["right_force"] == pytest.approx(
        mass_kg * GRAVITY * SWING_FORCE_RATIO + 5
    )


def test_imu_acceleration_values_are_expected_at_positive_peak(monkeypatch):
    monkeypatch.setattr(
        sensors.random,
        "gauss",
        lambda *args, **kwargs: 5.0,
    )
    results = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60, 1, 2, 3)

    acceleration = results["imu"]["acceleration"]

    assert acceleration["ax"] == pytest.approx(IMU_ACCEL_X_AMPLITUDE + 5)
    assert acceleration["ay"] == pytest.approx(IMU_ACCEL_Y_AMPLITUDE + 5)
    assert acceleration["az"] == pytest.approx(GRAVITY + 5)


def test_imu_gyroscope_values_are_expected_at_positive_peak(monkeypatch):
    monkeypatch.setattr(
        sensors.random,
        "gauss",
        lambda *args, **kwargs: 5.0,
    )
    results = generate_sensors(math.pi / 2, 3 * math.pi / 2, 60, 1, 2, 3)

    acceleration = results["imu"]["gyroscope"]

    assert acceleration["gx"] == pytest.approx(GYRO_X_AMPLITUDE + 5)
    assert acceleration["gy"] == pytest.approx(GYRO_Y_AMPLITUDE + 5)
    assert acceleration["gz"] == pytest.approx(GYRO_Z_AMPLITUDE + 5)
