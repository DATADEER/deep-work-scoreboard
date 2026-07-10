import argparse
import time

import board
import busio
import adafruit_drv2605

# Standalone haptic test for the DRV2605L on the QW/ST I2C bus.
# Kept separate from main.py so it never touches the scoreboard.
# The DRV answers at 0x5A — confirm with `i2cdetect -y 1` first.

# The full DRV2605 ROM waveform library (effect id -> name).
EFFECTS = {
    1: "Strong Click 100%",
    2: "Strong Click 60%",
    3: "Strong Click 30%",
    4: "Sharp Click 100%",
    5: "Sharp Click 60%",
    6: "Sharp Click 30%",
    7: "Soft Bump 100%",
    8: "Soft Bump 60%",
    9: "Soft Bump 30%",
    10: "Double Click 100%",
    11: "Double Click 60%",
    12: "Triple Click 100%",
    13: "Soft Fuzz 60%",
    14: "Strong Buzz 100%",
    15: "750 ms Alert 100%",
    16: "1000 ms Alert 100%",
    17: "Strong Click 1 100%",
    18: "Strong Click 2 80%",
    19: "Strong Click 3 60%",
    20: "Strong Click 4 30%",
    21: "Medium Click 1 100%",
    22: "Medium Click 2 80%",
    23: "Medium Click 3 60%",
    24: "Sharp Tick 1 100%",
    25: "Sharp Tick 2 80%",
    26: "Sharp Tick 3 60%",
    27: "Short Double Click Strong 1 100%",
    28: "Short Double Click Strong 2 80%",
    29: "Short Double Click Strong 3 60%",
    30: "Short Double Click Strong 4 30%",
    31: "Short Double Click Medium 1 100%",
    32: "Short Double Click Medium 2 80%",
    33: "Short Double Click Medium 3 60%",
    34: "Short Double Sharp Tick 1 100%",
    35: "Short Double Sharp Tick 2 80%",
    36: "Short Double Sharp Tick 3 60%",
    37: "Long Double Sharp Click Strong 1 100%",
    38: "Long Double Sharp Click Strong 2 80%",
    39: "Long Double Sharp Click Strong 3 60%",
    40: "Long Double Sharp Click Strong 4 30%",
    41: "Long Double Sharp Click Medium 1 100%",
    42: "Long Double Sharp Click Medium 2 80%",
    43: "Long Double Sharp Click Medium 3 60%",
    44: "Long Double Sharp Tick 1 100%",
    45: "Long Double Sharp Tick 2 80%",
    46: "Long Double Sharp Tick 3 60%",
    47: "Buzz 1 100%",
    48: "Buzz 2 80%",
    49: "Buzz 3 60%",
    50: "Buzz 4 40%",
    51: "Buzz 5 20%",
    52: "Pulsing Strong 1 100%",
    53: "Pulsing Strong 2 60%",
    54: "Pulsing Medium 1 100%",
    55: "Pulsing Medium 2 60%",
    56: "Pulsing Sharp 1 100%",
    57: "Pulsing Sharp 2 60%",
    58: "Transition Click 1 100%",
    59: "Transition Click 2 80%",
    60: "Transition Click 3 60%",
    61: "Transition Click 4 40%",
    62: "Transition Click 5 20%",
    63: "Transition Click 6 10%",
    64: "Transition Hum 1 100%",
    65: "Transition Hum 2 80%",
    66: "Transition Hum 3 60%",
    67: "Transition Hum 4 40%",
    68: "Transition Hum 5 20%",
    69: "Transition Hum 6 10%",
    70: "Transition Ramp Down Long Smooth 1",
    71: "Transition Ramp Down Long Smooth 2",
    72: "Transition Ramp Down Medium Smooth 1",
    73: "Transition Ramp Down Medium Smooth 2",
    74: "Transition Ramp Down Short Smooth 1",
    75: "Transition Ramp Down Short Smooth 2",
    76: "Transition Ramp Down Long Sharp 1",
    77: "Transition Ramp Down Long Sharp 2",
    78: "Transition Ramp Down Medium Sharp 1",
    79: "Transition Ramp Down Medium Sharp 2",
    80: "Transition Ramp Down Short Sharp 1",
    81: "Transition Ramp Down Short Sharp 2",
    82: "Transition Ramp Up Long Smooth 1",
    83: "Transition Ramp Up Long Smooth 2",
    84: "Transition Ramp Up Medium Smooth 1",
    85: "Transition Ramp Up Medium Smooth 2",
    86: "Transition Ramp Up Short Smooth 1",
    87: "Transition Ramp Up Short Smooth 2",
    88: "Transition Ramp Up Long Sharp 1",
    89: "Transition Ramp Up Long Sharp 2",
    90: "Transition Ramp Up Medium Sharp 1",
    91: "Transition Ramp Up Medium Sharp 2",
    92: "Transition Ramp Up Short Sharp 1",
    93: "Transition Ramp Up Short Sharp 2",
    94: "Transition Ramp Down Long Smooth 1 (50%)",
    95: "Transition Ramp Down Long Smooth 2 (50%)",
    96: "Transition Ramp Down Medium Smooth 1 (50%)",
    97: "Transition Ramp Down Medium Smooth 2 (50%)",
    98: "Transition Ramp Down Short Smooth 1 (50%)",
    99: "Transition Ramp Down Short Smooth 2 (50%)",
    100: "Transition Ramp Down Long Sharp 1 (50%)",
    101: "Transition Ramp Down Long Sharp 2 (50%)",
    102: "Transition Ramp Down Medium Sharp 1 (50%)",
    103: "Transition Ramp Down Medium Sharp 2 (50%)",
    104: "Transition Ramp Down Short Sharp 1 (50%)",
    105: "Transition Ramp Down Short Sharp 2 (50%)",
    106: "Transition Ramp Up Long Smooth 1 (50%)",
    107: "Transition Ramp Up Long Smooth 2 (50%)",
    108: "Transition Ramp Up Medium Smooth 1 (50%)",
    109: "Transition Ramp Up Medium Smooth 2 (50%)",
    110: "Transition Ramp Up Short Smooth 1 (50%)",
    111: "Transition Ramp Up Short Smooth 2 (50%)",
    112: "Transition Ramp Up Long Sharp 1 (50%)",
    113: "Transition Ramp Up Long Sharp 2 (50%)",
    114: "Transition Ramp Up Medium Sharp 1 (50%)",
    115: "Transition Ramp Up Medium Sharp 2 (50%)",
    116: "Transition Ramp Up Short Sharp 1 (50%)",
    117: "Transition Ramp Up Short Sharp 2 (50%)",
    118: "Long Buzz for Programmatic Stopping 100%",
    119: "Smooth Hum 1 (No kick/brake) 50%",
    120: "Smooth Hum 2 (No kick/brake) 40%",
    121: "Smooth Hum 3 (No kick/brake) 30%",
    122: "Smooth Hum 4 (No kick/brake) 20%",
    123: "Smooth Hum 5 (No kick/brake) 10%",
}

# A short, distinct subset for the default demo.
DEMO_EFFECTS = [1, 10, 12, 14, 47, 52, 58, 70, 118]

# Celebration chains for completing a focus session. Each is a short phrase
# played back-to-back on the DRV's 8-slot sequencer (max 8 steps), so every
# waveform finishes before the next starts — it feels like one gesture.
# Steps: ("e", effect_id) fires a waveform, ("p", seconds) inserts a pause.
CELEBRATIONS = [
    ("Level Up", "rising clicks into a strong buzz", [
        ("e", 3), ("e", 2), ("e", 1), ("p", 0.1), ("e", 14),
    ]),
    ("Fanfare", "click, double-click, then a triumphant buzz", [
        ("e", 1), ("p", 0.15), ("e", 10), ("p", 0.15), ("e", 14),
    ]),
    ("Heartbeat", "two strong pulses landing on a buzz", [
        ("e", 52), ("e", 52), ("p", 0.1), ("e", 14),
    ]),
    ("Whoosh Pop", "a rising ramp that pops at the top", [
        ("e", 84), ("e", 4), ("p", 0.1), ("e", 10),
    ]),
    ("Victory Roll", "ticks accelerating into a buzz and a final hit", [
        ("e", 24), ("e", 25), ("e", 26), ("e", 47), ("e", 1),
    ]),
]

def play(drv, effect):
    print(f"{effect:>3}: {EFFECTS.get(effect, '?')}")
    drv.sequence[0] = adafruit_drv2605.Effect(effect)
    drv.play()
    time.sleep(1)  # let the effect finish before the next one
    drv.stop()

def play_chain(drv, steps):
    for i, (kind, value) in enumerate(steps):
        drv.sequence[i] = (adafruit_drv2605.Effect(value) if kind == "e"
                           else adafruit_drv2605.Pause(value))
    if len(steps) < 8:  # terminate so stale slots from a prior chain don't play
        drv.sequence[len(steps)] = adafruit_drv2605.Effect(0)
    drv.play()
    time.sleep(2)  # play() is non-blocking; wait out the phrase

def main():
    parser = argparse.ArgumentParser(description="Buzz the DRV2605L motor")
    parser.add_argument("effect", nargs="?", type=int,
                        help="single effect number 1-123 (default: short demo)")
    parser.add_argument("--all", action="store_true",
                        help="play every effect 1-123 in order")
    parser.add_argument("--celebrate", action="store_true",
                        help="play the five focus-session celebration chains")
    args = parser.parse_args()

    i2c = busio.I2C(board.SCL, board.SDA)
    drv = adafruit_drv2605.DRV2605(i2c)
    print("DRV2605 connected")

    if args.celebrate:
        for name, description, steps in CELEBRATIONS:
            print(f"* {name}: {description}")
            play_chain(drv, steps)
            time.sleep(0.8)
        print("done")
        return

    if args.all:
        effects = list(EFFECTS)
    elif args.effect is not None:
        effects = [args.effect]
    else:
        effects = DEMO_EFFECTS

    for effect in effects:
        play(drv, effect)
        time.sleep(2.0)

    print("done")

if __name__ == "__main__":
    main()
