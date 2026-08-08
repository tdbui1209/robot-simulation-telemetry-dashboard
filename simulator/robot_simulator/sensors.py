import math


GRAVITY = 9.80665
CONTACT_FORCE_RATIO = 0.75
SWING_FORCE_RATIO = 0.04
IMU_ACCEL_X_AMPLITUDE = 0.2
IMU_ACCEL_Y_AMPLITUDE = 0.15


def generate_sensors(left_phase, right_phase, mass_kg):
    left_contact = math.sin(left_phase) > 0
    right_contact = math.sin(right_phase) > 0

    weight = mass_kg * GRAVITY
    left_force = weight * (CONTACT_FORCE_RATIO if left_contact else SWING_FORCE_RATIO)
    right_force = weight * (CONTACT_FORCE_RATIO if right_contact else SWING_FORCE_RATIO)

    return {
        "imu": {
            "acceleration": {
                "ax": IMU_ACCEL_X_AMPLITUDE * math.sin(left_phase),
                "ay": IMU_ACCEL_Y_AMPLITUDE * math.sin(left_phase),
                "az": GRAVITY * math.sin(left_phase),
            }
        },
        "foot_contact": {
            "left": left_contact,
            "right": right_contact,
            "left_force": left_force,
            "right_force": right_force,
        }
    }