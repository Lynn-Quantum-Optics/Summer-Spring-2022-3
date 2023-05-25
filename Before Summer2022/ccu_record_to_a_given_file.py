import fpga_ccu.renderer as renderer
import numpy as np
import scipy.stats as stats
import time
import csv
import tkinter as tk
import tkinter.filedialog as fd


from os.path import join
LOG_PATH = 'C:\\Users\\lynnlab\\Desktop\\summer2018\\scripts\\'
relativeLog = 'tmp\\ccu-log.csv'
LOG_PATH = join(LOG_PATH, relativeLog)

first_sample = 0
sample = np.arange(0)
time_ = np.empty(0)
total = np.empty((0, 8))
uncertainty = np.empty((0, 8))

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

 

def measure(samples, output_path):
    root = tk.Tk()
    root.withdraw() 
    
    outputter = renderer.Outputter(output_path)
    reader = csv.reader(file_reader(LOG_PATH))
    print(reader)
    printer = renderer.Printer(output_path)

    outputter.start()
    
    first_sample = 0
    sample = np.arange(0)
    time_ = np.empty(0)
    total = np.empty((0, 8))
    uncertainty = np.empty((0, 8)) 
        
    if samples > 0:
        iterations = range(samples)

    print('listening for data from "{}"'.format(LOG_PATH))
    print()
    
    def end():
        mean = np.mean(total, axis=0)
        uncertainty = stats.sem(total, axis=0)

        outputter.summary(mean, uncertainty)
        printer.summary(mean, uncertainty)
        return [mean, uncertainty]
    
    for _, (s, ti, to, u) in zip(iterations, map(decode, reader)):
        if sample.size == 0:
            first_sample = s

        sample = np.append(sample, s)
        time_ = np.append(time_, ti)
        total = np.row_stack((total, to))
        uncertainty = np.row_stack((uncertainty, u))
        printer.render(sample, time_, total, uncertainty)
        outputter.render(sample, time_, total, uncertainty)

    datasummary = end()
    print('The data is recorded at "{}"'.format(output_path))

    #added July 25, 2019:  not sure what we are doing, but this seems necessary.
    outputter.close()
    return datasummary

