
__all__ = [ 'plot_profiles',
            'add_hist']

# External
from ROOT import TH1F, TH2F, TProfile, TProfile2D, TCanvas
import numpy as np
import array
from ROOT import TCanvas
from root_utils.functions import *
from root_utils.axis import *

import rcphep as rpl



def add_hist(canvas, hist, drawopt='pE1') :
    h = hist.Clone()
    if not "same" in drawopt: drawopt += ' sames'
    rpl.hold(h)
    h.SetName('%s_%s'%(canvas.GetName(),hist.GetName()))
    canvas.cd()
    hist.Draw(drawopt)
    




def plot_profiles( hists, xlabel, these_colors, these_markers,
                   drawopt='pE1', 
                   ratio_label='Trigger/Ref.',
                   ylabel='Trigger Efficiency', 
                   do_ratio=False,
                   y_axes_maximum=1.1, 
                   y_axes_minimum=0.0, 
                   pad_top_y_axes_maximum=1.1, 
                   pad_top_y_axes_minimum=0.0, 
                   pad_bot_y_axes_maximum=1.1,
                   pad_bot_y_axes_minimum=0.9):
    
    
    doRatio = True if (doRatioCanvas and (len(hists)>1)) else False
    collect = []
    canvas = rpl.create_ratio_canvas( 'canvas', "", 700, 500) if do_ratio else rpl.create_canvas( 'canvas', "", 700, 500 )
    if do_ratio:
        pad_top = canvas.GetPrimitive('pad_top')
        pad_bot = canvas.GetPrimitive('pad_bot')
    
    hist_ref = hists[0]
    for idx, hist in enumerate(hists):
        if doRatio:
            if idx < 1:
                hist_ref.SetLineColor(these_colors[idx])
                hist_ref.SetMarkerColor(these_colors[idx])
                hist_ref.SetMarkerStyle(these_markers[idx])
                hist_ref.SetMarkerSize(1)
                hist_ref.SetMaximum(pad_top_y_axes_maximum)
                hist_ref.SetMinimum(pad_top_y_axes_minimum)
                rpl.add_hist(pad_top, hist_ref, drawopt = drawopt)
            else:

                hist.SetLineColor(these_colors[idx])
                hist.SetMarkerColor(these_colors[idx])
                hist.SetMaximum(pad_top_y_axes_maximum)
                hist.SetMarkerStyle(these_markers[idx])
                hist.SetMarkerSize(1)

                hist_ratio=hist.Clone()
                hist_ratio.Divide(hist_ratio,hist_ref,1.,1.,'B')
                hist_ratio.SetMinimum(pad_bot_y_axes_minimum)
                hist_ratio.SetMaximum(pad_bot_y_axes_maximum)
                hist_ratio.SetMarkerStyle(these_markers[idx])
                hist_ratio.SetMarkerSize(1)
    
                rpl.add_hist( pad_top, hist, drawopt)
                rpl.add_hist( pad_bot, hist_ratio, 'P')
        else:
            hist.SetLineColor(these_colors[idx])
            hist.SetMarkerColor(these_colors[idx])
            hist.SetMaximum(y_axes_maximum)
            hist.SetMinimum(y_axes_minimum)
            hist.SetMarkerStyle(these_markers[idx])
            rpl.add_hist(canvas, hist, drawopt = drawopt)
    
    rpl.format_canvas_axes(XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5)
    rpl.set_axis_labels(xlabel,ylabel,rlabel)
    return canvas



