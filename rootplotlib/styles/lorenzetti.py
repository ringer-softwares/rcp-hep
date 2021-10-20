

__all__ = [
    'set_lorenzetti_label',
]

import rootplotlib as rpl


def set_lorenzetti_label( x, y, text, pad=None):
    rpl.set_label('Lorenzetti', x, y, text, pad=pad)

