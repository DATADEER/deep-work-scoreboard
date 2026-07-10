import argparse
import time

import board
import busio
import adafruit_drv2605

# Standalone haptic test for the DRV2605L on the QW/ST I2C bus.
# Kept separate from main.py so it never touches the scoreboard.
# The DRV answers at 0x5A — confirm with `i2cdetect -y 1` first.

# A few of the 123 built-in effects, picked to feel distinct.
DEMO_EFFECTS = [
    (1, "strong click"),
    (10, "double click"),
    (47, "buzz"),
    (16, "soft bump"),
]

def play(drv, effect):
    print(f"playing effect {effect}")
    drv.sequence[0] = adafruit_drv2605.Effect(effect)
    drv.play()
    time.sleep(1)  # let the effect finish before the next one
    drv.stop()

def main():
    parser = argparse.ArgumentParser(description="Buzz the DRV2605L motor")
    parser.add_argument("effect", nargs="?", type=int,
                        help="single effect number 1-123 (default: run the demo)")
    args = parser.parse_args()

    i2c = busio.I2C(board.SCL, board.SDA)
    drv = adafruit_drv2605.DRV2605(i2c)
    print("DRV2605 connected")

    if args.effect is not None:
        play(drv, args.effect)
    else:
        for effect, name in DEMO_EFFECTS:
            print(f"-> {name}")
            play(drv, effect)
            time.sleep(0.5)

    print("done")

if __name__ == "__main__":
    main()
