
__all__ = [ 
            'add_hist',
            'hist1d',
            'fill1d',
            'density',
            'divide',
            'shift',
            ]


import array
import rootplotlib as rpl
import ROOT


#
# Add TH1 or TH2 object into the figure
#
def add_hist( hist, drawopt='pE1', pad=None):
    fig = rpl.get_figure()
    fig.add_hist(hist, drawopt, pad)


#
# Create TH1F histogram
#
def hist1d( name, bins, xmin=None, xmax=None, title=''):

    if type(bins) is int and (xmin and xmax):
        return ROOT.TH1F(name, title, bins, xmin, xmax)
    else:
        if type(bins) is list:
            bins = array('d', bins)
        elif type(bins) is np.array:
            bins = array('d', bins.tolist())
        return ROOT.TH1F(name, title, len(bins), bins)


def fill1d( hist, x_values ):
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN( len(x_values), array.array('d',  x_values),  w)

    
def density( hist ):
    norm = 1./sum(hist)
    h = hist.Clone()
    h.Reset('M')
    h.SetName( hist.GetName() + '_dens')
    for b in range(0,h.GetNbinsX()+1):
      content = hist.GetBinContent(b)
      value = content*norm
      h.SetBinContent(b , value )
    return h


def divide( hist_num, hist_den ):
    h = hist_num.Clone()
    h.SetName(hist_num.GetName()+'_ratio')
    h.Divide( hist_den )
    return h


def shift( hist, shift_units ):
    h = hist.Clone()
    h.SetName( hist.GetName() + '_shift')
    h.Reset('M')
    for b in range(1, hist.GetNbinsX()):
        content = hist.GetBinContent(b)
        h.SetBinContent(b+shift_units, content)
    return h

