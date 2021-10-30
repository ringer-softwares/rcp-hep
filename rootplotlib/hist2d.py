
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

#def new( name, xbins, ybins, title=''):
#    if type(xbins) is list:
#        xbins = array('d', xbins)
#    elif type(xbins) is np.array:
#        xbins = array('d', xbins.tolist())
#    if type(ybins) is list:
#        ybins = array('d', ybins)
#    elif type(xbins) is np.array:
#        ybins = array('d', ybins.tolist())
#    return ROOT.TH2F(name, title, len(xbins), xbins, len(ybins), ybins)



def fill( hist, values ):
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN( len(values), array.array('d',  values),  w)

    
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

