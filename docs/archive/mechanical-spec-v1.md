# SaltScale Mechanical Specification v1

## Purpose

Battery powered scale platform for a domestic water softener salt container.

## Salt Container

- Diameter: 290 mm
- Height: 440 mm
- Estimated operating weight: 18-30 kg

## Platform

- Outer diameter: 320 mm
- Circular design
- Total height: max 45 mm
- Designed for installation in a utility closet / meter cupboard

## Printing Constraints

- Compatible with Prusa MK4
- No single printed part larger than 200 x 200 x 200 mm
- PETG recommended
- M3 heat-set inserts where applicable

## Segmentation

- Platform split into 4 identical quarter segments
- Segments assembled with M3 screws

## Load Cell

- Single-point load cell
- Rated capacity: 50 kg
- Centrally mounted
- Replaceable without reprinting the platform

## Electronics

Contained inside platform:

- ESP32-C3
- HX711
- 3x AA battery holder
- Status LED
- Push button

## User Interface

One push button.

Functions:

- Short press: measure now
- Double press: refill event
- Hold 5s: calibration mode
- Hold 10s: WiFi setup
- Hold 20s: factory reset

One status LED.

## Serviceability

Battery replacement must be possible without removing the salt container.

## Protection

Mechanical overload protection required.

Platform shall include overload stops with approximately 1 mm clearance.

## Future Expansion

Reserved space for:

- e-paper display
- buzzer
- temperature sensor

No support required in v1.