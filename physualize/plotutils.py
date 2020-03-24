import os 
import sys 

import numpy as np
import matplotlib 
matplotlib.use("pdf") 
import matplotlib.pyplot as plt 
## https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
## https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.hist.html#matplotlib.axes.Axes.hist
class plotutils:
    def __init__(self, columns, binning, legend, axisTitle, experiment, plotType, makeRatio, saveLog, Xrange, pdfname="",areaNormalize=False  ):
        self.columns_    = columns
        self.binning_    = int(binning[0]) if len(binning)==1 else [float(i) for i in binning]
        self.legend_     = legend
        self.axisTitle_  = axisTitle
        self.experiment_ = experiment
        self.plotType_   = plotType
        self.makeRatio_  = makeRatio
        self.saveLog_    = saveLog
        self.Xrange_     = [float(Xrange[0]), float(Xrange[1])]
        self.pdfname_    = pdfname
        self.areaNormalize_   = areaNormalize
        self.weight_   = []
        #self.   = 
        
        #print "inide init of class 
        #print self.columns_, self.binning_, self.legend_, self.axisTitle_, self.experiment_, self.plotType_, self.makeRatio_, self.saveLog_

    def setrootfiles(self):
        return 0
    def getrootfiles(self):
        return 0
    def getvariables(self):
        return 0
    def plotSingle(self):
        return 0
        
        
    
        
        
    def phyHist(self, ax):
        colors_ = ["Red", "Blue"]
        step_error=[]
        for icol in range(len(self.columns_)):
            
            
            ## this is for the stack. 
            h_, bin_, patches_ = ax.hist(self.columns_[icol], bins=self.binning_, range=self.Xrange_, weights=self.weight_[icol], histtype="step", color=colors_[icol] )
            center = (bin_[:-1] + bin_[1:]) / 2
            error_  = np.sqrt(h_) * self.weight_[icol][0]
            s,=ax.step(bin_,np.r_[h_,h_[-1]],where='post', color=colors_[icol], )
            e = ax.errorbar(center, h_, yerr=error_, fmt='none', ecolor=colors_[icol])
            step_error.append((s,e))
            
            '''
            h_, bin_ = np.histogram( self.columns_[icol], bins=self.binning_, range=self.Xrange_, weights=self.weight_[icol])
            center = (bin_[:-1] + bin_[1:]) / 2
            error_  = np.sqrt(h_) * self.weight_[icol][0]
            s,=ax.step(bin_,np.r_[h_,h_[-1]],where='post', color=colors_[icol] )
            e = ax.errorbar(center, h_, yerr=error_, fmt='none', ecolor=colors_[icol])# drawstyle="stepfilled")
            
            step_error.append((s,e))
            '''

        ax.legend(step_error, self.legend_, numpoints=1)
        #ax.legend(self.legend_, numpoints=1)
        
        return ax
        
        
    def plotOverlay(self):
                
        fig, ax = plt.subplots()
        
        print "inside the plotOverlay() function"
        
        ## weights
        weight_column_ = [np.ones_like(icol) for icol in self.columns_ ]
        if self.areaNormalize_: weight_column_ = [np.ones_like(icol)/len(icol) for icol in self.columns_ ]   
        self.weight_   = weight_column_

        
        ## following line takes care of the overflow and underflow bins
        self.columns_ = [np.clip(icol, float(self.Xrange_[0]), float(self.Xrange_[1]) )  for icol in self.columns_]

        
        '''
        ax.hist( self.columns_, \
                 bins=int(self.binning_),\
                 histtype='step', \
                 weights=weight_column_, \
                 range=self.Xrange_,\
                 label=self.legend_)
        '''
        
        ax = self.phyHist(ax)
        print self.legend_
        #ax.legend()
        
        figureTitle = self.experiment_ + " " + self.plotType_
        ax.set_title(figureTitle, x=0.2)
        if len(self.axisTitle_)==2: 
            ax.set_xlabel(self.axisTitle_[0], x=0.88)
            ax.set_ylabel(self.axisTitle_[1])
        
        plt.savefig(self.pdfname_+".pdf")
        return 0
    def plotStack(self):
        return 0
    def plotEfficiency(self):
        return 0
    def plotEfficiencyOverlay(self):
        return 0
    def plot1DLimits(self):
        return 0
    def plotLimitsOverlay(self):
        return 0
    def plot2dLimits(self):
        return 0
        
