
__all__ = [ 
            'add_hist',
            'fill_hist1d', 
            'fill_hist2d',
            ]


import array
import rootplotlib as rpl


def add_hist( hist, drawopt='pE1', pad=None):
    fig = rpl.get_figure()
    fig.add_hist(hist, drawopt, pad)


def fill_hist1d( hist, x_values ):
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN( len(x_values), array.array('d',  x_values),  w)


def fill_hist2d( hist, x_values, y_values ):
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN( len(x_values), array.array('d',  x_values), array.array('d',  y_values),  w)

