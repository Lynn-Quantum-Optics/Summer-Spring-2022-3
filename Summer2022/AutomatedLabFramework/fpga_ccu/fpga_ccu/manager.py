import numpy as np
import time
import scipy.stats as stats


class FpgaCcuManager:
    def __init__(self, controller, renderers, buffer_samples):
        self.controller = controller
        self.renderers = renderers
        self.buffer_samples = buffer_samples

        # initialize arrays to hold data
        self.sample = np.arange(0)
        self.time = np.array(())
        self.total = np.empty((0, 8))
        self.uncertainty = np.empty((0, 8))

    def start(self):
        for renderer in self.renderers:
            renderer.start()

    @staticmethod
    def summarize(buffer):
        mean = np.mean(buffer, axis=0)

        if len(buffer) <= 1:
            uncertainty = np.empty(np.shape(mean))
            uncertainty[:] = np.nan
            return mean, uncertainty

        uncertainty = stats.sem(buffer, axis=0)

        return mean, uncertainty

    def next(self):

        buffer = self.controller.read(self.buffer_samples)

        total, uncertainty = self.summarize(buffer)
        total *= self.buffer_samples
        uncertainty *= self.buffer_samples
        sample = len(self.sample) + 1
        t = time.time()

        self.total = np.row_stack((self.total, total))
        self.uncertainty = np.row_stack((self.uncertainty, uncertainty))
        self.sample = np.append(self.sample, sample)
        self.time = np.append(self.time, t)

        for renderer in self.renderers:
            renderer.render(self.sample, self.time,
                            self.total, self.uncertainty)

    def __enter__(self):
        return self

    def __exit__(self, e_type=None, e_value=None, e_traceback=None):
        self.end()

    def end(self):

        mean = np.mean(self.total, axis=0)
        uncertainty = stats.sem(self.total, axis=0)

        for renderer in self.renderers:
            renderer.summary(mean, uncertainty)
            renderer.close()

        self.controller.close()
