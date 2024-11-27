import ctypes
import os
import time

class IntervalTimer:
    def __init__(self, priority_class=ctypes.c_int(0x80)):
        self.kernel32 = ctypes.windll.kernel32
        self.current_pid = os.getpid()
        self.current_process = self.open_process()
        self.set_process_priority(priority_class)
        self.frequency = self.get_performance_frequency()
        self.time_period = 1  # 1ms
        self.set_timer_resolution(self.time_period)
        self.iteration = 0

    def open_process(self):
        PROCESS_SET_INFORMATION = 0x0200
        PROCESS_QUERY_INFORMATION = 0x0400
        process_handle = self.kernel32.OpenProcess(PROCESS_SET_INFORMATION | PROCESS_QUERY_INFORMATION, False, self.current_pid)
        if process_handle == 0:
            error_code = self.kernel32.GetLastError()
            raise Exception(f"Failed to get current process handle. Error code: {error_code}")
        return process_handle

    def set_process_priority(self, priority_class):
        result = self.kernel32.SetPriorityClass(self.current_process, priority_class)
        if not result:
            error_code = self.kernel32.GetLastError()
            raise Exception(f"Failed to set process priority. Error code: {error_code}")
        print("Process priority set successfully.")

    def set_timer_resolution(self, time_period):
        self.kernel32.timeBeginPeriod(time_period)

    def get_performance_frequency(self):
        frequency = ctypes.c_uint64()
        self.kernel32.QueryPerformanceFrequency(ctypes.byref(frequency))
        return frequency.value

    def get_high_precision_time(self):
        counter = ctypes.c_uint64()
        self.kernel32.QueryPerformanceCounter(ctypes.byref(counter))
        return counter.value / self.frequency

    def measure_time(self, sleep_duration=0.001):
        """
        Measure the elapsed time for a single execution.

        This function measures the time elapsed from the start to the end of a sleep process, with the unit in milliseconds.
        It is mainly used for performance testing or to measure the execution time of a specific process.

        Parameters:
        sleep_duration (float): The sleep duration in seconds, default is 0.001 seconds.

        Returns:
        list: Returns a list containing the iteration count and the elapsed time for that iteration.
        """
        start_time = time.perf_counter()  # Record the start time of the execution
        time.sleep(sleep_duration)  # Simulate a delay
        end_time = time.perf_counter()  # Record the end time of the execution
        elapsed_time = (end_time - start_time) * 1000  # Calculate the elapsed time (unit: milliseconds)
        self.iteration += 1  # Increment the iteration count
        return [self.iteration, elapsed_time]  # Return the iteration count and the elapsed time for that iteration

    def reset_timer_resolution(self):
        self.kernel32.timeEndPeriod(self.time_period)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset_timer_resolution()
        self.kernel32.CloseHandle(self.current_process)
