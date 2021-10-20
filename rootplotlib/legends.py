
__all__ = ['set_text']

from ROOT import TLegend
import rootplotlib as rpl


def set_text(text_list, x1=.2, y1=.84, x2=.5, y2=.9, angle=0, textsize=12, pad=None):
    
    if type(text_list) is str:
        text_list = [ text_list ]

    leg = TLegend(x1,y1,x2,y2)
    leg.SetName('leg')
    leg.SetTextSize(textsize)
    leg.SetTextFont(43)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    for text in text_list :
        leg.AddEntry(0,text,'')
    rpl.add_legend(leg)
    return leg

