
__all__ = [ 
            #'new',
            #'fill',
            #'density',
            #'divide',
            #'shift',
            ]


import array
import rootplotlib as rpl
import ROOT
import numpy as np



#
# Create TH1F histogram
#
def new( name, xbins, xmin, xmax, ybins, ymin, ymax, title=''):
    return ROOT.TH2F(name, title, xbins, xmin, xmax, ybins, ymin, ymax)


def new2( name, xbins, ybins, title=''):
    if type(xbins) is list:
        xbins = array.array('d', xbins)
    elif type(xbins) is np.array:
        xbins = array.array('d', xbins.tolist())
    if type(ybins) is list:
        ybins = array.array('d', ybins)
    elif type(xbins) is np.array:
        ybins = array.array('d', ybins.tolist())
    print(xbins)
    print(ybins)
    return ROOT.TH2F(name, title, len(xbins)-1, xbins, len(ybins)-1, ybins)



def fill( hist, xvalues, yvalues ):

    w = array.array( 'd', np.ones_like( xvalues ) )

    # treat x values
    if type(xvalues) is list:
        xvalues = array('d', xvalues)
    elif type(xvalues) is np.array:
        xvalues = array('d', xvalues.tolist())

    # treat y values
    if type(yvalues) is list:
        yvalues = array('d', yvalues)
    elif type(xvalues) is np.array:
        yvalues = array('d', yvalues.tolist())

    if len(xvalues) != len(yvalues):
        print('It is not possible to fill the histogram. x/y values must be the same size')
    else:
        hist.FillN( len(xvalues), xvalues, yvalues,  w)

    
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

