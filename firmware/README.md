# SaltScale Firmware

Firmware is intentionally not implemented yet.

The first firmware task is a bench-only hardware bring-up sketch for:

- Seeed Studio XIAO ESP32C3.
- SparkFun HX711.
- SparkFun Load Sensor Combinator.
- Four 50 kg load sensors.

Initial firmware goal:

- Read raw HX711 values.
- Print raw values over USB serial.
- Avoid Wi-Fi.
- Avoid deep sleep.
- Avoid battery handling.
- Avoid calibration logic.
- Avoid MQTT or product behavior.

See:

- `docs/hardware-bringup-v0.md`

Do not start battery optimization, enclosure electronics, or final calibration until the raw four-sensor bridge is proven on the bench.
