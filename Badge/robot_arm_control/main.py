### Author: Dave Kimber <https://github.com/Kimbsy>
### Description: Control the MeArm robotic arm using the servo outputs on the badge.
### License: MIT
### Appname: MeArm Control

# pin 1 = bottom servo, rotation, left/right on joystick
# pin 2 = left servo, distance, up/down on joystick
# pin 3 = right servo, height, A/B buttons
# pin 4 = claw, toggle with center joystick

import pyb
import buttons
import ugfx

servos = [
    pyb.Servo(1),
    pyb.Servo(2),
    pyb.Servo(3),
    pyb.Servo(4),
]

boundaries = [
    [-90, 90], # (right, left)
    [0, 65],   # (close, far)
    [-65, 20], # (up,    down)
    [-80, 20], # (open,  closed)
]

positions = [
    0,
    boundaries[1][0],
    boundaries[2][0],
    boundaries[3][0],
]

active = True

# Claw works on a toggle as the badge doesn't have enough inputs.
claw_closed = False

ugfx.init()
buttons.init()

# Set up display.
ugfx.area(0, 0, ugfx.width(), ugfx.height(), 0)
ugfx.text(30, 30, "Base: %d" % (positions[0]), 0xFFFF)
ugfx.text(30, 60, "Distance: %d" % (positions[1]), 0xFFFF)
ugfx.text(30, 90, "Height: %d" % (positions[2]), 0xFFFF)
ugfx.text(30, 120, "Claw: %d" % (positions[3]), 0xFFFF)

def got_input(index, inc):
    """Having received an input, update the positions of the servos keeping them within the boundaries.

    @param  index  The index of the servo to move.
    @param  inc    How much to adjust the position by.
    """
    positions[index] = positions[index] + inc
    if positions[index] < boundaries[index][0]:
        positions[index] = boundaries[index][0]
    if positions[index] > boundaries[index][1]:
        positions[index] = boundaries[index][1]

def check_inputs():
    """Determine if the user has pressed any buttons and update the target positions of the servos accordingly.

    @return  Whether the user has pressed any buttons.
    """
    changed = False;
    # Base.
    if buttons.is_pressed("JOY_LEFT"):
        got_input(0, 5)
        changed      = True
    if buttons.is_pressed("JOY_RIGHT"):
        got_input(0, -5)
        changed      = True
    # Distance.
    if buttons.is_pressed("JOY_UP"):
        got_input(1, -5)
        changed      = True
    if buttons.is_pressed("JOY_DOWN"):
        got_input(1, 5)
        changed      = True
    # Height.
    if buttons.is_pressed("BTN_A"):
        got_input(2, 5)
        changed      = True
    if buttons.is_pressed("BTN_B"):
        got_input(2, -5)
        changed      = True
    # Claw.
    if buttons.is_pressed("JOY_CENTER"):
        global claw_closed
        claw_closed  = not claw_closed
        positions[3] = boundaries[3][1] if claw_closed else boundaries[3][0]
        changed      = True
    return changed

# Run until menu button exits the app.
while active:
    # Check for inputs.
    changed = check_inputs()

    # Update display.
    if changed:
        ugfx.area(0, 0, ugfx.width(), ugfx.height(), 0)
        ugfx.text(30, 30, "Base: %d" % (positions[0]), 0xFFFF)
        ugfx.text(30, 60, "Distance: %d" % (positions[1]), 0xFFFF)
        ugfx.text(30, 90, "Height: %d" % (positions[2]), 0xFFFF)
        ugfx.text(30, 120, "Claw: %d" % (positions[3]), 0xFFFF)

    # Update servo positions.
    for i, servo in enumerate(servos):
        servo.angle(positions[i])
        pyb.delay(10)
