import math
import random


GRAVITY = 9.80665
CONTACT_FORCE_RATIO = 0.75
SWING_FORCE_RATIO = 0.04
IMU_ACCEL_X_AMPLITUDE = 0.2
IMU_ACCEL_Y_AMPLITUDE = 0.15
GYRO_X_AMPLITUDE = 0.03
GYRO_Y_AMPLITUDE = 0.03
GYRO_Z_AMPLITUDE = 0.05


def generate_sensors(
    left_phase: float,
    right_phase: float,
    mass_kg: float, 
    imu_accel_std: float,
    gyro_std: float,
    foot_force_std_n: float,
) -> dict:
    left_contact = math.sin(left_phase) > 0
    right_contact = math.sin(right_phase) > 0

    weight = mass_kg * GRAVITY
    left_force = weight * (CONTACT_FORCE_RATIO if left_contact else SWING_FORCE_RATIO)
    right_force = weight * (CONTACT_FORCE_RATIO if right_contact else SWING_FORCE_RATIO)

    return {
        "imu": {
            "acceleration": {
                "ax": IMU_ACCEL_X_AMPLITUDE * math.sin(left_phase) + random.gauss(sigma=imu_accel_std),
                "ay": IMU_ACCEL_Y_AMPLITUDE * math.sin(left_phase) + random.gauss(sigma=imu_accel_std),
                "az": GRAVITY * math.sin(left_phase) + random.gauss(sigma=imu_accel_std),
            },
            "gyroscope": {
                "gx": GYRO_X_AMPLITUDE * math.sin(left_phase) + random.gauss(sigma=gyro_std),
                "gy": GYRO_Y_AMPLITUDE * math.sin(left_phase) + random.gauss(sigma=gyro_std),
                "gz": GYRO_Z_AMPLITUDE * math.sin(left_phase) + random.gauss(sigma=gyro_std),
            }
        },
        "foot_contact": {
            "left": left_contact,
            "right": right_contact,
            "left_force": left_force + random.gauss(sigma=foot_force_std_n),
            "right_force": right_force + random.gauss(sigma=foot_force_std_n)
        }
    }
