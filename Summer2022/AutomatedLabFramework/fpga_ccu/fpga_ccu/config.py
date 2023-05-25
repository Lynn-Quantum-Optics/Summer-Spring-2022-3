DEFAULTS = {
    'port': 'COM4',
    'baud': 19200,
    'interval': 1.0,
    'termination': 0xff,
    'update_period': .1,
    'samples': 0,
}

CHANNEL_KEYS = ('C0 (A)', 'C1 (B)', "C2 (A')",
                "C3 (B')", 'C4', 'C5', 'C6', 'C7')
MAX_CHANNEL_KEY_LEN = max(map(len, CHANNEL_KEYS))

DESCRIPTION = (
    'Altera DE2 FPGA CCU interface; see '
    'http://people.whitman.edu/~beckmk/QM/circuit/circuit.html')
