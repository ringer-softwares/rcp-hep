
__all__ = ['set_axis_labels',
           'fix_x_axis_ranges',
           'fix_x_axis_ranges',
           ]

import numpy as np
from ROOT import TGraph,TH1,TH2,THStack, TMath, TGraphErrors
from operator import itemgetter
import itertools
import sys

#
# Main functions
#

def set_axis_labels(xlabel, ylabel,yratiolabel='ratio'):

    canvas = rpl.get_canvas()
    if canvas:
        # case of ratio_canvas
        if 'pad_top' in (primitive.GetName() for primitive in canvas.GetListOfPrimitives()) :
            SetAxisLabels(canvas.GetPrimitive('pad_bot'), xlabel, yratiolabel)
            SetAxisLabels(canvas.GetPrimitive('pad_top'), '', ylabel)
        else:
            for primitive in canvas.GetListOfPrimitives() :
                if hasattr(primitive,'GetXaxis') :
                    primitive.GetXaxis().SetTitle(xlabel)
                    primitive.GetYaxis().SetTitle(ylabel)
                    break
        canvas.Modified()
        canvas.Update()


def fix_x_axis_ranges(xminf=1., xminc=0., xmaxf=1., xmaxc=0., only_filled=False):
    canvas = rpl.get_canvas()
    if canvas:
        xmin, xmax = get_x_axis_ranges(canvas,check_all=True, only_filled=only_filled)
        set_x_axis_ranges(canvas, xmin*xminf+xminc, xmax*xmaxf+xmaxc, for_all=True)

def fix_y_axis_ranges(yminf=1., yminc=0., ymaxf=1., ymaxc=0., ignore_zeros=True, ignore_errors=False):
    canvas = rpl.get_canvas()
    if canvas:
        xmin, xmax = get_y_axis_ranges(canvas, check_all=True, ignore_zeros=ignore_zeros, ignore_errors=ignore_errors)
        set_y_axis_ranges(canvas, ymin*yminf+yminc, ymax*ymaxf+ymaxc)


#
# X Axis
#

def get_x_axis_ranges(canvas, check_all=False, only_filled=False):

    xmin = sys.float_info.max
    xmax = sys.float_info.min
    for primitive in canvas.GetListOfPrimitives():
        if isinstance(primitive,TGraph):
            continue
        if issubclass(type(primitive),TH1):
            axis = primitive.GetXaxis()
            if not check_all :
                return axis.GetXmin(),xaxis.GetXmax()
            if only_filled:
                bins = [primitive.GetBinCenter(idx) for idx in range(1,primitive.GetNbinsX()+1) if primitive.GetBinContent(idx)>0]
                if x:
                    xmin = min(xmin,bins[0])
                    xmax = max(xmax,bins[-1])
            else:
                xmin = min(xmin,axis.GetXmin())
                xmax = max(xmax,axis.GetXmax())
    return xmin,xmax


def set_x_axis_ranges(canvas, xmin, xmax, for_all=False):

    axis = None
    # Get the axis from canvas
    for primitive in canvas.GetListOfPrimitives():
        if issubclass(type(primitive),TGraph):
            xaxis = primitive.GetHistogram().GetXaxis()
            break
        if issubclass(type(primitive),TH1):
            xaxis = primitive.GetXaxis()
            break

    if not axis:
        print ('Warning: set_x_axis_range had no effect. Check that your canvas has plots in it.')
    else:
        if for_all: 
            axis.SetRangeUser(xmin,xmax)
        else: 
            axis.SetLimits(xmin,xmax)
        canvas.Modified()
        canvas.Update()

#
# Y Axis
#

def get_y_axis_ranges(canvas, check_all=False, ignore_zeros=False, ignore_errors=False):

    ymin = sys.float_info.max
    ymax = sys.float_info.min

    for primitive in canvas.GetListOfPrimitives():

        if isinstance(primitive, TH2):
            x = primitive.GetXaxis()
            y = primitive.GetYaxis()
            nx = primitive.GetNbinsY()
            ny = primitive.GetNbinsY()
            # This is just a workaround for candles/violins
            for rxc, ryc in itertools.product( range(1,nx+1), range(1,ny+1)):
                z = primitive.GetBinContent(rxc,ryc)
                if ignore_zeros and z == 0 :
                    continue
                ymin = min(ymin,y.GetBinCenter(ryc))
                ymax = max(ymax,y.GetBinCenter(ryc))
            return ymin, ymax

        if issubclass(type(primitive),TGraph) :
            ymin = min(ymin,TMath.MinElement(primitive.GetN(),primitive.GetY()))
            ymax = max(ymax,TMath.MaxElement(primitive.GetN(),primitive.GetY()))
            if not check_all :
                return ymin,ymax

        elif issubclass(type(primitive),TH1) :
            ysum = 0
            for bin in range(primitive.GetNbinsX()) :
                ysum = ysum+primitive.GetBinContent(bin+1)
            if ysum == 0: ignore_zeros = 0
            for bin in range(primitive.GetNbinsX()) :
                y = primitive.GetBinContent(bin+1)
                if ignore_errors :
                    ye = 0
                else :
                    ye = primitive.GetBinError(bin+1)
                if ignore_zeros and y == 0 :
                    continue
                ymin = min(ymin,y-ye)
                ymax = max(ymax,y+ye)
            if not check_all:
                return ymin,ymax
  
        elif issubclass(type(i),THStack) :
            ymin = primitive.GetMinimum()
            ymax = primitive.GetMaximum()

    return ymin, ymax



def set_y_axis_ranges(canvas, ymin, ymax):

    if canvas.GetPrimitive('pad_top') :
        set_y_axis_ranges(canvas.GetPrimitive('pad_top'),ymin,ymax)
    
    axis = 0
    for primitive in canvas.GetListOfPrimitives() :
        if issubclass(type(primitive),TGraph) :
            axis = primitive.GetHistogram().GetYaxis()
            break
        elif issubclass(type(primitive),TH1) :
            axis = primitive.GetYaxis()
            break
        elif issubclass(type(primitive),TH2) :
            axis = primitive.GetYaxis()
            break
    if not yaxis :
        print ('Warning: SetYaxisRange had no effect. Check that your canvas has plots in it.')
    else:
        axis.SetRangeUser(ymin,ymax)
        canvas.Modified()
        canvas.Update()



