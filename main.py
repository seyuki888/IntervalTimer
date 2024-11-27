import ctypes
from IntervalTimer import IntervalTimer
NORMAL_PRIORITY_CLASS = 0x20
IDLE_PRIORITY_CLASS = 0x40
HIGH_PRIORITY_CLASS = 0x80
REALTIME_PRIORITY_CLASS = 0x100
ABOVE_NORMAL_PRIORITY_CLASS = 0x8000
BELOW_NORMAL_PRIORITY_CLASS = 0x4000
PROCESS_MODE_BACKGROUND_BEGIN = 0x10000000
PROCESS_MODE_BACKGROUND_END = 0x20000000
if __name__ == "__main__":
    priority_class = ctypes.c_int(REALTIME_PRIORITY_CLASS)  # REALTIME_PRIORITY_CLASS
    with IntervalTimer(priority_class) as timer:
        try:
            while True:
                iteration, elapsed_time = timer.measure_time(0.001) # unit: second
                if elapsed_time > 3:
                    print(f"Time elapsed for the {iteration} time: {elapsed_time:.2f} ms")
        except KeyboardInterrupt:
            print("Measurement stopped by user.")
