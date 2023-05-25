import fpga_ccu.__main__ as ccu
from threading import Thread
import sys
import fpga_ccu.renderer as renderer
import matplotlib.pyplot as mpl
import csv
import numpy as np
import time
import datetime as dt
import scipy.stats as stats
import itertools as it
import tkinter as tk
import tkinter.filedialog as fd
import subprocess

from ConfigurationReader import ConfigReader


class CCU:
    def __init__(self, config: ConfigReader):

        self.path = f"temp/ccu/ccu-log.csv"

        self.ccu_log_active = False

    def run_log(self):
        if not self.ccu_log_active:
            subprocess.run(["cmd.exe", "/c", "start", "python", "ccu_log.py"], timeout=3)
            self.ccu_log_active = True
        else:
            pass
        # self._log_thread.start()

    def run_monitor(self):
        if self.ccu_log_active:
            subprocess.run(["cmd.exe", "/c", "start", "python", "ccu_monitor.py"], timeout=3)
        else:
            raise Exception("CCU log is not active.")
        # if self._log_thread.is_alive():
        #     self._monitor_thread.start()
        # else:
        #     raise Exception("Log is not running. Cannot run monitor.")

    def run_record_manual_entry(self):
        if self.ccu_log_active:
            self._record_manual()
        else:
            raise Exception("CCU log is not active.")
        # if self._log_thread.is_alive():
        #     self._record_manual()
        # else:
        #     raise Exception("Log is not running. Cannot run record.")

    def run_record(self, num_samples, file_path):
        self._record_automated(num_samples, file_path)
        # if self._log_thread.is_alive():
        #     self._record_automated(num_samples, file_path)
        # else:
        #     raise Exception("Log is not running. Cannot run monitor.")

    def _record_manual(self):

        root = tk.Tk()
        root.withdraw()

        samples = 0
        while True:
            try:
                print('# of samples (pass 0 to collect indefinitely):')
                entry = input('(default: 0) > ')
                if not entry:
                    samples = 0

                samples = int(entry)

                if samples < 0:
                    print('must be non-negative')
                    continue

                break
            except ValueError:
                print('not a valid integer')

        print()

        print('select output log file:')
        output_path = fd.asksaveasfilename()
        print('> {}'.format(output_path))

        print()

        def file_reader(path):
            with open(path, 'r') as f:
                f.read()
                f.readline()
                while True:
                    line = f.readline().strip()

                    if not line:
                        time.sleep(.1)
                        continue

                    yield line

        def decode(row):
            sample = int(row[0])
            time_ = float(row[1])
            total = np.array(tuple(map(float, row[2::2])))
            uncertainty = np.array(tuple(map(float, row[3::2])))
            return sample, time_, total, uncertainty

        outputter = renderer.Outputter(output_path)
        reader = csv.reader(file_reader(self.path))
        printer = renderer.Printer(output_path)

        outputter.start()

        first_sample = 0
        sample = np.arange(0)
        time_ = np.empty(0)
        total = np.empty((0, 8))
        uncertainty = np.empty((0, 8))

        if samples > 0:
            iterations = range(samples)
        else:
            iterations = it.repeat(0)

        print('listening for data from "{}"'.format(self.path))
        print()

        def end():

            mean = np.mean(total, axis=0)
            uncertainty = stats.sem(total, axis=0)

            outputter.summary(mean, uncertainty)
            printer.summary(mean, uncertainty)

        try:
            for _, (s, ti, to, u) in zip(iterations, map(decode, reader)):
                if sample.size == 0:
                    first_sample = s

                sample = np.append(sample, s)
                time_ = np.append(time_, ti)
                total = np.row_stack((total, to))
                uncertainty = np.row_stack((uncertainty, u))
                printer.render(sample, time_, total, uncertainty)
                outputter.render(sample, time_, total, uncertainty)

            end()
            print('done; press interrupt (ctrl-c) to exit')
            try:
                while True:
                    time.sleep(.1)
            except KeyboardInterrupt:
                print('exiting')

        except KeyboardInterrupt:
            print()
            print('interrupted')
            print()
            end()
            print('press interrupt (ctrl-c) again to exit')

    def _record_automated(self, num_samples: int, file_path):

        root = tk.Tk()
        root.withdraw()

        if num_samples < 0:
            raise Exception('# samples must be non-negative.')

        output_path = file_path

        def file_reader(path):
            with open(path, 'r') as f:
                f.read()
                f.readline()
                while True:
                    line = f.readline().strip()

                    if not line:
                        time.sleep(.1)
                        continue

                    yield line

        def decode(row):
            sample = int(row[0])
            time_ = float(row[1])
            total = np.array(tuple(map(float, row[2::2])))
            uncertainty = np.array(tuple(map(float, row[3::2])))
            return sample, time_, total, uncertainty

        outputter = renderer.Outputter(output_path)
        reader = csv.reader(file_reader(self.path))
        # printer = renderer.Printer(output_path)

        outputter.start()

        first_sample = 0
        sample = np.arange(0)
        time_ = np.empty(0)
        total = np.empty((0, 8))
        uncertainty = np.empty((0, 8))

        if num_samples > 0:
            iterations = range(num_samples)
        else:
            iterations = it.repeat(0)

        def end():

            mean = np.mean(total, axis=0)
            uncertainty = stats.sem(total, axis=0)

            outputter.summary(mean, uncertainty)
            # printer.summary(mean, uncertainty)

        for _, (s, ti, to, u) in zip(iterations, map(decode, reader)):
            if sample.size == 0:
                first_sample = s

            sample = np.append(sample, s)
            time_ = np.append(time_, ti)
            total = np.row_stack((total, to))
            uncertainty = np.row_stack((uncertainty, u))
            # printer.render(sample, time_, total, uncertainty)
            outputter.render(sample, time_, total, uncertainty)

        end()
