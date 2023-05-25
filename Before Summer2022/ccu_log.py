import fpga_ccu.__main__ as ccu
import sys

options = [
    '-o', 'tmp/ccu-log.csv',
    '-f',
] + sys.argv[1:]

try:
    with ccu.FpgaCcuUtility(options=options) as utility:
        utility.run()
except KeyboardInterrupt:
    print('interrupted; exiting')
