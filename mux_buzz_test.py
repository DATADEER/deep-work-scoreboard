import argparse
import time

import board
import busio
import adafruit_tca9548a
import adafruit_drv2605

# Two-motor haptic playground via the PCA9546 mux (TCA9548A-compatible lib).
# Driver on mux channel 0 = LEFT, channel 1 = RIGHT.
# Mux answers at 0x70; each driver at 0x5A on its own channel.
#
# The mux only gates I2C, not the motor drive: once a DRV's play() is
# triggered it buzzes on its own, so firing left then right a few ms apart
# reads as simultaneous, and one side can hold a buzz while the other taps
# over it (true async overlap).

def fire(drv, effect):
    # non-blocking: triggers the effect on the chip and returns immediately
    drv.sequence[0] = adafruit_drv2605.Effect(effect)
    drv.play()

def unison(left, right):
    # both sides hit the same strong buzz together, three times
    for _ in range(3):
        fire(left, 14)
        fire(right, 14)
        time.sleep(1.0)

def alternate(left, right):
    # call-and-response: left, right, left, right
    for _ in range(6):
        fire(left, 4)
        time.sleep(0.35)
        fire(right, 4)
        time.sleep(0.35)

def wave(left, right):
    # quick left->right sweep, like motion crossing the device
    for _ in range(5):
        fire(left, 24)
        time.sleep(0.12)
        fire(right, 24)
        time.sleep(0.5)

def pingpong(left, right):
    # bounce side to side, accelerating, then slam together
    sides = [left, right]
    for i, gap in enumerate([0.4, 0.35, 0.3, 0.25, 0.2, 0.16, 0.13, 0.1]):
        fire(sides[i % 2], 4)
        time.sleep(gap)
    fire(left, 14)
    fire(right, 14)
    time.sleep(1.0)

def overlap(left, right):
    # one side holds a sustained hum while the other taps a rhythm over it
    for hum, tap in ((left, right), (right, left)):
        fire(hum, 118)  # long buzz, runs until explicitly stopped
        for _ in range(4):
            fire(tap, 1)
            time.sleep(0.5)
        hum.stop()
        time.sleep(0.4)

def ticktock(left, right, seconds=15):
    # clock: left "tick", right "tock", alternating every half second
    interval = 0.5
    for i in range(int(seconds / interval)):
        fire(left if i % 2 == 0 else right, 24)  # sharp tick
        time.sleep(interval)

PATTERNS = {
    "unison": ("Unison", "both sides buzz together", unison),
    "alternate": ("Alternate", "left/right call-and-response", alternate),
    "wave": ("Wave", "quick left-to-right sweep", wave),
    "pingpong": ("Ping-Pong", "accelerating bounce into a unison slam", pingpong),
    "overlap": ("Overlap", "one side hums while the other taps over it", overlap),
    "ticktock": ("Tick-Tock", "clock: left tick / right tock for N seconds", ticktock),
}

def main():
    parser = argparse.ArgumentParser(description="Two-motor mux haptic patterns")
    parser.add_argument("pattern", nargs="?",
                        help="pattern name (default: tour all; 'list' to list)")
    parser.add_argument("--seconds", type=int, default=15,
                        help="duration for ticktock (default 15)")
    args = parser.parse_args()

    i2c = busio.I2C(board.SCL, board.SDA)
    mux = adafruit_tca9548a.TCA9548A(i2c)  # library also drives the PCA9546
    left = adafruit_drv2605.DRV2605(mux[0])
    right = adafruit_drv2605.DRV2605(mux[1])
    print("two DRV2605 connected (left=ch0, right=ch1)")

    if args.pattern == "list":
        for slug, (title, description, _) in PATTERNS.items():
            print(f"{slug}: {title} — {description}")
        return

    def run(slug):
        title, description, func = PATTERNS[slug]
        print(f"* {title}: {description}")
        if slug == "ticktock":
            func(left, right, args.seconds)
        else:
            func(left, right)

    if args.pattern in PATTERNS:
        run(args.pattern)
    elif args.pattern is None:
        for slug in PATTERNS:
            run(slug)
            time.sleep(1.0)
    else:
        print(f"unknown '{args.pattern}' — try: list")
        return

    print("done")

if __name__ == "__main__":
    main()
