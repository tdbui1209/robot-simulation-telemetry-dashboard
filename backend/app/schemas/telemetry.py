from datetime import datetime

from pydantic import BaseModel


class Position(BaseModel):
    x: float
    y: float
    z: float


class Orientation(BaseModel):
    roll: float
    pitch: float
    yaw: float


class LinearVelocity(BaseModel):
    vx: float
    vy: float
    vz: float


class AngularVelocity(BaseModel):
    wx: float
    wy: float
    wz: float


class BasePose(BaseModel):
    position: Position
    orientation: Orientation
    linear_velocity: LinearVelocity
    angular_velocity: AngularVelocity


class Acceleration(BaseModel):
    ax: float
    ay: float
    az: float


class Gyroscope(BaseModel):
    gx: float
    gy: float
    gz: float


class Imu(BaseModel):
    acceleration: Acceleration
    gyroscope: Gyroscope


class FootContact(BaseModel):
    left: float
    right: float
    left_force: float
    right_force: float


class Sensors(BaseModel):
    imu: Imu
    foot_contact: FootContact


class Metrics(BaseModel):
    fps: float
    sim_step_ms: float
    latency_ms: float
    packet_size_bytes: int
    stability_score: float
    tracking_error: float


class Event(BaseModel):
    type: str
    severity: str
    message: str
    value: float | None = None


class TelemetryPacket(BaseModel):
    schema_version: str
    timestamp: datetime

    experiment_id: str
    run_id: str
    robot_id: str

    sequence: int
    sim_time: float

    base_pose: BasePose

    sensors: Sensors
    metrics: Metrics
    events: list[Event]
