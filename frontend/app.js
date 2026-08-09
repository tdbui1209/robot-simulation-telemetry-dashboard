const statusElement = document.getElementById("connection-status");
const emptyState = document.getElementById("empty-state");
const dashboard = document.getElementById("dashboard");

const setText = (id, value) => {
  document.getElementById(id).textContent = value;
};

const fixed = (value, digits = 2) =>
  typeof value === "number" ? value.toFixed(digits) : "—";

function setStatus(state) {
  statusElement.textContent = state;
  statusElement.className = `status status--${state}`;
}

function render(packet) {
  emptyState.hidden = true;
  dashboard.hidden = false;

  setText("experiment-id", packet.experiment_id);
  setText("run-id", packet.run_id);
  setText("robot-id", packet.robot_id);
  setText("sequence", packet.sequence);
  setText("sim-time", `${fixed(packet.sim_time, 3)} s`);
  setText("fps", fixed(packet.metrics?.fps, 1));
  setText("latency", `${fixed(packet.metrics?.latency_ms, 2)} ms`);
  setText("stability", fixed(packet.metrics?.stability_score, 3));
  setText("velocity-x", `${fixed(packet.base_pose?.linear_velocity?.vx, 3)} m/s`);
  setText("tracking-error", fixed(packet.metrics?.tracking_error, 4));

  setText("position-x", fixed(packet.base_pose?.position?.x, 3));
  setText("position-y", fixed(packet.base_pose?.position?.y, 3));
  setText("position-z", fixed(packet.base_pose?.position?.z, 3));
  setText("roll", fixed(packet.base_pose?.orientation?.roll, 3));
  setText("pitch", fixed(packet.base_pose?.orientation?.pitch, 3));
  setText("yaw", fixed(packet.base_pose?.orientation?.yaw, 3));

  setText("accel-z", fixed(packet.sensors?.imu?.acceleration?.az, 3));
  setText("gyro-z", fixed(packet.sensors?.imu?.gyroscope?.gz, 3));
  setText("left-force", `${fixed(packet.sensors?.foot_contact?.left_force, 1)} N`);
  setText("right-force", `${fixed(packet.sensors?.foot_contact?.right_force, 1)} N`);
  setText("step-time", `${fixed(packet.metrics?.sim_step_ms, 2)} ms`);
  setText("packet-size", `${packet.metrics?.packet_size_bytes ?? "—"} B`);
  setText("schema-version", `schema ${packet.schema_version}`);
  setText("packet-time", new Date(packet.timestamp).toLocaleTimeString());
  setText("raw-json", JSON.stringify(packet, null, 2));
}

let socket;
let reconnectTimer;

function connect() {
  clearTimeout(reconnectTimer);
  setStatus("connecting");

  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const url = `${protocol}://${window.location.host}/ws/dashboard`;
  socket = new WebSocket(url);

  socket.addEventListener("open", () => setStatus("connected"));

  socket.addEventListener("message", (event) => {
    try {
      const message = JSON.parse(event.data);
      if (message.type === "telemetry") {
        render(message.data);
      }
    } catch (error) {
      console.error("Invalid WebSocket message", error);
    }
  });

  socket.addEventListener("error", () => setStatus("error"));

  socket.addEventListener("close", () => {
    setStatus("disconnected");
    reconnectTimer = setTimeout(connect, 1500);
  });
}

window.addEventListener("beforeunload", () => {
  clearTimeout(reconnectTimer);
  socket?.close();
});

connect();
