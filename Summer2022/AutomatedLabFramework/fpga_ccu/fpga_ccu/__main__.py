import argparse
import os.path as path
import itertools as it
import datetime as dt
from . import manager
from . import renderer
from . import controller
import sys
import errno

from . import config


class FpgaCcuUtility:

    FILL_WIDTH = 70

    def __init__(self, options=None):
        # parse and process command-line options
        self.options = Options(options=options)

        # use dummy controller for debugging if dummy option is selected
        if self.options.dummy:
            self.controller = controller.DummyCcuController()
        else:
            self.controller = controller.FpgaCcuController(self.options.port,
                                                           self.options.baud)

        self.renderers = []

        self.printer = renderer.Printer()
        self.renderers.append(self.printer)

        self.intro()

        # initialize file output handler
        self.outputter = None
        if self.options.output:
            if path.exists(self.options.output_path):
                print('file "' + self.options.output_path + '" already '
                      'exists; ', end='')

                if self.options.overwrite:
                    print('overwriting...')
                else:
                    print('exiting (pass `-f` or `--force` to force '
                          'overwrite)...')
                    sys.exit(errno.EEXIST)

            self.outputter = renderer.Outputter(self.options.output_path)
            self.renderers.append(self.outputter)

        # initialize plotting handler
        self.plotter = None
        if self.options.plot:
            self.plotter = renderer.Plotter(
                self.options.plot_left, self.options.plot_right,
                self.options.bar,
                title=(('CCU measurements:\nCounts per {} sec\n'
                        '{:%Y %B %d (%A), %I:%M %p}')
                       .format(self.options.interval, dt.datetime.now())),
                plot_window=self.options.plot_window,
                refresh_rate=self.controller.UPDATE_PERIOD/10,
            )

            self.renderers.append(self.plotter)

        self.manager = manager.FpgaCcuManager(
            self.controller, self.renderers,
            buffer_samples=self.options.buffer_samples,
        )

    def intro(self):
        # print some intro text
        self.printer.hline('=')
        self.printer.fill_print(config.DESCRIPTION)
        self.printer.hline('=')

        self.printer.fill_print(
            'using serial port "{}"'.format(self.options.port))
        self.printer.fill_print(
            'using serial baud rate {}'.format(self.options.baud))
        self.printer.fill_print('accumulating measurements over {:.1f} sec'
                                .format(self.options.interval))

        if self.options.samples == 0:
            self.printer.fill_print('collecting samples indefinitely')
        else:
            self.printer.fill_print('collecting a total of {} samples'
                                    .format(self.options.samples))

        if self.options.output:
            self.printer.fill_print('writing output to file "{}"'
                                    .format(self.options.output_path))

        print()

    def run(self):
        if self.options.samples > 0:
            iterations = range(self.options.samples)
        else:
            iterations = it.repeat(0)

        self.manager.start()

        for _ in iterations:
            self.manager.next()

    def __enter__(self):
        return self

    def __exit__(self, e_type=None, e_value=None, e_traceback=None):
        self.manager.end()


class Options:
    """
    Parses command-line options and does some basic cleaning and
    pre-processing.
    """

    def __init__(self, options=None):

        args = self.parse(args=options)

        self.port = args.port
        self.baud = args.baud

        self.buffer_samples = max(round(args.interval /
                                        config.DEFAULTS['update_period']), 1)
        self.interval = self.buffer_samples * config.DEFAULTS['update_period']

        self.samples = args.samples

        self.output_path = args.output
        self.output = bool(self.output_path)
        self.overwrite = args.force
        self.summarize = args.summarize

        self.dummy = args.dummy

        self.plot_left = args.plot_left
        self.plot_right = args.plot_right
        self.bar = args.bar
        self.plot = self.plot_left or self.plot_right or self.bar
        self.plot_window = args.window
        self.image = args.image

    def parse(self, args=None):
        """
        Parse and process command-line configuration options.
        """
        # command-line configuration options

        parser = argparse.ArgumentParser(
            description=config.DESCRIPTION,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        connection = parser.add_argument_group(
            'connection',
            'options for connecting to FPGA via serial protocol',
        )

        connection.add_argument(
            '-P', '--port',
            action='store', default=config.DEFAULTS['port'],
            help='serial port on which the FPGA is attached',
        )
        connection.add_argument(
            '-B', '--baud',
            action='store', type=int, default=config.DEFAULTS['baud'],
            help='baud rate for serial communication',
        )

        sampling = parser.add_argument_group(
            'sampling', 'options related to sample timing and counts',
        )

        sampling.add_argument(
            '-t', '--interval',
            metavar='SECONDS', action='store', type=float,
            default=config.DEFAULTS['interval'],
            help='time interval (in seconds) between accumulated '
            'measurements; rounded to the nearest multiple of ' +
            '{:.1f}'.format(config.DEFAULTS['update_period']) + '(seconds)',
        )
        sampling.add_argument(
            '-n', '--samples',
            action='store', type=int, default=config.DEFAULTS['samples'],
            help='number of samples to collect; pass 0 to collect '
            'indefinitely',
        )

        output = parser.add_argument_group(
            'output', 'options related to outputting data to file',
        )

        output.add_argument(
            '-o', '--output',
            metavar='FILE', action='store', default='',
            help='path to output data file (CSV); leave blank for no output',
        )
        output.add_argument(
            '-f', '--force',
            action='store_true',
            help='forcefully overwrite existing data file',
        )
        output.add_argument(
            '-s', '--summarize',
            action='store_true',
            help='add summary statistics (mean & sd) to end of output file',
        )

        plotting = parser.add_argument_group(
            'plotting', 'plotting and visualization options'
        )
        plotting.add_argument(
            '-p', '--plot-left',
            action='append',
            type=int,
            choices=range(8),
            default=[],
            help='plot measurements against time on left column (pass '
            'multiple times to plot multiple channels)',
        )
        plotting.add_argument(
            '-pp', '--plot-right',
            action='append',
            type=int,
            choices=range(8),
            default=[],
            help='plot measurements against time on right column (pass '
            'multiple times to plot multiple channels)',
        )
        plotting.add_argument(
            '-b', '--bar',
            action='store_true',
            help='enable live bar plot of all counters',
        )
        plotting.add_argument(
            '-w', '--window',
            metavar='N', action='store', type=int, default=0,
            help='maximum number of points to plot at a time (pass 0 for '
            'no limit)',
        )
        plotting.add_argument(
            '-i', '--image',
            action='store', default='',
            help='save plot image to file as PDF (leave empty to not save)',
        )

        miscellaneous = parser.add_argument_group(
            'miscellaneous', 'miscellaneous output options',
        )

        miscellaneous.add_argument(
            '-d', '--dummy',
            action='store_true',
            help='use dummy ccu controller (for code debugging/testing only)',
        )

        return parser.parse_args(args)


def main():
    try:
        with FpgaCcuUtility() as utility:
            utility.run()
    except KeyboardInterrupt:
        print('interrupted; exiting')


if __name__ == '__main__':
    main()
