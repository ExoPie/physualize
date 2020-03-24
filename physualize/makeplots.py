#!/usr/bin/python
import os 
import sys 
import argparse

usage = " generalised plotting macro:"
#for TTree:  python makeplots.py  -i files.txt --readFrom TTree --treename monoHbb_SR_boosted --variable "MET:nJets" --binning "20:4"  --Xrange "200 1000:0 4" --legend "signal;top" --axistitle "USDp_{T}^{miss}USD;# of events:USDn_{Jets}USD;# of events" --plotMode overlay --areaNormalize

# for csv: python makeplots.py  -i files.txt --readFrom "csv"  --variable "MET:nJets" --binning "20:4"  --Xrange "200 1000:0 4" --legend "signal;top" --axistitle "USDp_{T}^{miss}USD;# of events:USDn_{Jets}USD;# of events" --plotMode overlay --areaNormalize --prefix "monoHbb_SR_boosted_"

# for cuts: python makeplots.py  -i files.txt --readFrom "csv"  --variable "MET:nJets" --binning "20:4"  --Xrange "200 1000:0 4" --legend "signal;top" --axistitle "USDp_{T}^{miss}USD;# of events:USDn_{Jets}USD;# of events" --plotMode overlay --areaNormalize --prefix "monoHbb_SR_boosted_"  --selection "MET>400"

# for multiple cuts python makeplots.py  -i files.txt --readFrom "csv"  --variable "MET:nJets" --binning "20:4"  --Xrange "200 1000:0 4" --legend "signal;top" --axistitle "USDp_{T}^{miss}USD;# of events:USDn_{Jets}USD;# of events" --plotMode overlay --areaNormalize --prefix "monoHbb_SR_boosted_"  --selection "MET>200;nJets==1"

# for 
parser = argparse.ArgumentParser(description=usage)
#parser.add_argument("-n","--numberoffiles", dest="inputfile", type=int) ## to double check how many files are there, and also to decide weather to read histo from same file or different files
parser.add_argument("-i", "--inputfile",  dest="inputfile",default="") ## provide list in "1.root 2.root" else provide the .txt file with all the files

parser.add_argument("-readFrom","--readFrom", dest="readFrom", default="TTree") ## possible values for the moment TTree, later it can also deal with TH1F and CSV and other pythonic data-types. you name it and I will add it. 
parser.add_argument("-prefix_", "--prefix_", dest="prefix_", default="h_")
parser.add_argument("-treename", "--treename", dest="treename", default="tree_")

parser.add_argument("-merge","--mergefiles",dest="mergefiles",default="") ## if some files need to be merged you can provide same id for those files, should provide like, 1 2 3 4 4 5, it will merge two files with process id 4 

parser.add_argument("-var", "--variable", dest="variable", default="") ## variable which you want to see save as pdf 

parser.add_argument("-binning", "--binning", dest="binning", default="10") ## if it is just an integer then use that as number of bins and if it is a list then use that as binning. provide list as numbers seprated by space in double quotes 

parser.add_argument("-Xrange", "--Xrange", dest="Xrange", default="")## sperated by space

parser.add_argument("-plotMode", "--plotMode", dest="plotMode", default="overlay") # single; overlay; stack; 

parser.add_argument("-legend", "--legend", dest="legend", default="") ## legend, would be in the same order as the file names or histogram names 

parser.add_argument("-axisT", "--axistitle", dest="axistitle", default="") ## "xAxis; yAxis" seperated by semi-colon

parser.add_argument("-exp", "--experiment", dest="experiment", default="CMS") ## add experiment name or some other text
''' add one more argument later to set the position of the legend ''' 


parser.add_argument("-plotType", "--plotType", dest="plotType", default="Preliminary")

parser.add_argument("-makeratio", "--makeratio", action="store_true", dest="makeratio")

parser.add_argument("-areaNormalize", "--areaNormalize", action="store_true", dest="areaNormalize")

parser.add_argument("-specialstyle","--specialstyle", dest="specialstyle", default="cms.sty") ## it is possible to skip the style parameters from command line and instead provide this style file to set the plotting style. 

parser.add_argument("-saveLog", "--saveLog",  dest="saveLog", default="Y" ) ## possible values it can accept, X, Y, XY, Z, XYZ, XZ, YZ


parser.add_argument("-saveType", "--saveType", dest="saveType", default=".pdf") ## you can save in more than one type, just provide them in double quotes seprated by single space 

parser.add_argument("-selection", "--selection", dest="selection", default="")

#parser.add_argument("", "--", dest="", default="")


args = parser.parse_args()


from root_pandas import read_root
from pandas import  read_csv
import numpy


def textToList(textfile):
    return [iline.rstrip()    for iline in open(textfile)]

def argsToList(arguments, delimator_=" "):
    arguments = arguments.replace("USD","$")
    return arguments.split(delimator_)

def getFileList(args_input_):
    fileList_=[]
    if ".txt" in args_input_:
        fileList_ = textToList(args_input_)
        print "reading the input files listed in the text file ", args_input_
    else:
        print "reading these files ",args_input_
        fileList_ = argsToList(args_input_)
    return fileList_

def SelectedDataFrame(df, selection_):
    '''
    sign_ = selection_[1]
    if sign_ == ">": df = df[(df[selection_[0]]>float(selection_[2]))]
    if sign_ == "<": df = df[(df[selection_[0]]<float(selection_[2]))]
    if sign_ == "==": df = df[(df[selection_[0]]==float(selection_[2]))]
    if sign_ == ">=": df = df[(df[selection_[0]]>=float(selection_[2]))]
    if sign_ == "<=": df = df[(df[selection_[0]]<=float(selection_[2]))]
    '''
    #var_ = selection_[0]
    

    cutval = float(selection_[2])
    qry = str(selection_[0])+" > @cutval"
    df = df.query(qry)
    '''
    sel_qry = ""
    for isel in selection_:
        cutval = float(isel[2])
        qry = str(isel[0])+" > @cutval & "
    df = df.query(qry)
    '''
    return df

def treeToArray(filename_, treename_, variable_, selection_=""):
    ## this can be changed to uproot in future
    df = read_root(filename_, treename_, columns=[variable_])
    if selection_ != "": 
        for isel in selection_:
            df  = SelectedDataFrame(df, selection_)
    df = df[[variable_]]
    return numpy.array(df)




    
def csvToArray(filename_, variable_, selection_=""):
    print "selection = ",selection_
    ## this can be changed to uproot in future
    df = read_csv(filename_,delimiter=",")
    print "df lenght before cut", len(df)
    if selection_ != "": 
        for isel in selection_:
            df  = SelectedDataFrame(df, isel)
            print "----------------"
            print "size of df after ", isel, len(df)
        #df  = SelectedDataFrame(df, selection_)
    df = df[[variable_]]
    return numpy.array(df)


def GetSelection(selec):
    selForQuery=[]
    for iselection in selec:
        sign_=""
        if ">"  in iselection: sign_  = ">" 
        if "<"  in iselection: sign_  = "<" 
        if "==" in iselection: sign_  = "==" 
        if ">=" in iselection: sign_  = ">=" 
        if "<=" in iselection: sign_  = "<="
        if "!=" in iselection: sign_  = "!="

        selvar_ = iselection.split(sign_)[0]
        selcut_ = iselection.split(sign_)[1]
        selForQuery.append( [iselection.split(sign_)[0], sign_, iselection.split(sign_)[1]])

    return selForQuery
    
def GetColumn(readfrom_, filename_, treename_, variable_):
    ''' check the input type: TTree, TH1F or CSV ''' 
    column_=[]
    allselection = argsToList(args.selection, delimator_=";")
    if readfrom_ == "TTree":
        
        column_ =  treeToArray(filename_, treename_, variable_, GetSelection(allselection))
    if readfrom_ == 'csv':
        #selection_ = GetSelection(args.selection)
        column_ = csvToArray(filename_, variable_, GetSelection(allselection))

    return column_

## ** -------------------------------** ##

## main code is here, all functions should be before this

## ** -------------------------------** ##




''' get the list of files ''' 
filelist =  getFileList(args.inputfile)
print filelist

''' get the variable array in a single variable, list ''' 
allvars  = argsToList(args.variable,delimator_=":")
allaxistitle = argsToList(args.axistitle,delimator_=":")
allbinning  = argsToList(args.binning, delimator_=":")
allXrange   = argsToList(args.Xrange, delimator_=":")


for i in range (len(allvars)):
    AllColumns=[ GetColumn(args.readFrom, ifile, args.treename, allvars[i]) for ifile in filelist]
    
    prefix_ = ""
    if args.readFrom == "TTree": prefix_ =  args.treename
    if args.readFrom == "csv":   prefix_ =  args.prefix_
    PDFname = prefix_ + "_" + allvars[i]
    
    
    
    
    from plotutils import plotutils
    pu_ = plotutils(columns=AllColumns, \
                    binning=argsToList(allbinning[i]), \
                    legend=argsToList(args.legend,";"), \
                    axisTitle=argsToList(allaxistitle[i],delimator_=";"), \
                    experiment=args.experiment, \
                    plotType=args.plotType, \
                    makeRatio=args.makeratio, \
                    saveLog=args.saveLog, \
                    areaNormalize = args.areaNormalize, \
                    Xrange=argsToList(allXrange[i]),\
                    pdfname=PDFname
                )
    
    
    if args.plotMode=="overlay":
        pu_.plotOverlay()
    
        

