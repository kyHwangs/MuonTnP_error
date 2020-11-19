import sys
import os
from ROOT import TFile, TDirectory, TCanvas, TGraphAsymmErrors


# -- extract efficiency graph & all fit canvases from given TnP ROOT file
class TnPInfoExtractor:
    def __init__(self):
        self.ROOTFileName = ""
        self.outputFile = TFile()

        # -- internal variables
        self.dataType = ""
        self.treeName = "tpTree"

    def Extract(self):
        myFile = TFile( self.ROOTFileName )
        print "Now loading [%s] ..." % self.ROOTFileName

        self.SaveGraph(myFile)
        print "[TnPInfoExtractor::Extract] Graphs are saved\n"

        self.SaveFitCanvas(myFile)
        print "[TnPInfoExtractor::Extract] Fit canvases are saved\n"

        myFile.Close()
        print "[TnPInfoExtractor::Extract] Finished\n\n"


    def SaveGraph(self, myFile):
        graphName = self.MakeGraphName()

        # -- first sub-directory
        dirPath1 = "%s" % self.treeName
        dirObject1 = myFile.GetDirectory( dirPath1 )
        print "now in %s" % dirPath1

        if dirObject1.GetListOfKeys().GetEntries() > 2:
            print "More than 2 directories under %s" % dirPath1
            sys.exit()

        # -- directory with efficiency graphs
        effDirPath   = "%s/%s/fit_eff_plots" % ( self.treeName, dirObject1.GetListOfKeys().At(0).GetName() )
        effDirObject = myFile.GetDirectory( effDirPath )
        print "now in %s" % effDirPath

        # -- extract efficiency graph
        # -- 2D case: special treatment is needed
        if self.ROOTFileName.endswith("_pteta.root"):
            self.SaveGraph_2D(effDirObject, graphName)

        # -- 1D case (except for single bin): simple
        elif "_single.root" not in self.ROOTFileName: 
            if effDirObject.GetListOfKeys().GetEntries() > 1:
                print "More than 1 directory under %s" % effDirPath
                sys.exit()
            self.SaveGraph_1D(effDirObject, graphName)


    def SaveFitCanvas(self, myFile):
        fitOutputDirName = self.MakeGraphName() # -- output directory name = graph name

        # -- make a directory where fit canvases are saved
        if fitOutputDirName not in os.listdir("./"):
            os.mkdir( fitOutputDirName )

        # -- make a sub directory "PNG" also
        fitOutputDirPath_PNG = "%s/PNG" % fitOutputDirName
        if not os.path.isdir(fitOutputDirPath_PNG):
            os.mkdir( fitOutputDirPath_PNG )

        # -- first sub-directory
        dirPath1 = "%s" % self.treeName
        dirObject1 = myFile.GetDirectory( dirPath1 )
        print "now in %s" % dirPath1

        if dirObject1.GetListOfKeys().GetEntries() > 2:
            print "More than 2 directories under %s" % dirPath1
            sys.exit()

        # -- second sub-directory
        dirPath2 = "%s/%s" % ( self.treeName, dirObject1.GetListOfKeys().At(0).GetName() )
        dirObject2 = myFile.GetDirectory( dirPath2 )
        print "now in %s" % dirPath2

        for key in dirObject2.GetListOfKeys():
            fitDirName = key.GetName()
            
            if "_eff" not in fitDirName: 
                fitDirPath   = "%s/%s" % (dirPath2, key.GetName())
                fitDirObject = myFile.GetDirectory( fitDirPath )

                for key2 in fitDirObject.GetListOfKeys():
                    if key2.GetName() == "fit_canvas":
                        canvas = key2.ReadObj()

                        canvas.Draw() # -- it needs when it is printed as image

                        # -- save .pdf
                        canvas.SaveAs( "./%s/%s.pdf" % (fitOutputDirName, fitDirName ) )

                        # -- save .png
                        pngFileName = self.MakePNGFileName(fitDirName)
                        # canvas.Draw() # -- it needs when it is printed as image
                        canvas.Print( "%s/%s" % (fitOutputDirPath_PNG, pngFileName ) )

                        break # -- break if fit canvas is found


    def MakePNGFileName(self, fitDirName):
        imageFileName = "" # -- return object
        
        pattern = ""
        if self.ROOTFileName.endswith("_pt.root"):  pattern = "pt_bin"
        if self.ROOTFileName.endswith("_eta.root"): pattern = "eta_bin"
        if self.ROOTFileName.endswith("_phi.root"): pattern = "phi_bin"
        if self.ROOTFileName.endswith("_vtx.root"): pattern = "tag_nVertices_bin"

        list_fitDirNameSplit = fitDirName.split("__")

        # -- special treatment is needed for finding bin info.
        if self.ROOTFileName.endswith("_pteta.root"):
            ptBinInfo = ""
            etaBinInfo = ""
            absEtaBinInfo = ""
            for fitDirNameSplit in list_fitDirNameSplit:
                if fitDirNameSplit.startswith("pt_bin"):     ptBinInfo = fitDirNameSplit
                if fitDirNameSplit.startswith("eta_bin"):    etaBinInfo = fitDirNameSplit
                if fitDirNameSplit.startswith("abseta_bin"): absEtaBinInfo = fitDirNameSplit

            if etaBinInfo == "":
                imageFileName = "%s__%s.png" % (absEtaBinInfo, ptBinInfo)
            else:
                imageFileName = "%s__%s.png" % (etaBinInfo, ptBinInfo)

        # -- single bin case: no bin info.
        elif self.ROOTFileName.endswith("_single.root"):
            imageFileName = "%s.png" % self.MakeGraphName()

        # -- ID efficiency case: simple
        else: 
            for fitDirNameSplit in list_fitDirNameSplit:
                if fitDirNameSplit.startswith(pattern):
                    imageFileName = "%s.png" % fitDirNameSplit

        imageFileName = self.ChangeBinNumberWith2Dights(imageFileName)
        return imageFileName

    # -- ex> bin0.png -> bin00.png, bin1.png -> bin01.png ...
    # ---- it needs to be correctly ordered in .html file
    def ChangeBinNumberWith2Dights(self, imageFileName):
        if "bin0.png" in imageFileName: imageFileName = imageFileName.replace("bin0.png", "bin00.png")
        if "bin1.png" in imageFileName: imageFileName = imageFileName.replace("bin1.png", "bin01.png")
        if "bin2.png" in imageFileName: imageFileName = imageFileName.replace("bin2.png", "bin02.png")
        if "bin3.png" in imageFileName: imageFileName = imageFileName.replace("bin3.png", "bin03.png")
        if "bin4.png" in imageFileName: imageFileName = imageFileName.replace("bin4.png", "bin04.png")
        if "bin5.png" in imageFileName: imageFileName = imageFileName.replace("bin5.png", "bin05.png")
        if "bin6.png" in imageFileName: imageFileName = imageFileName.replace("bin6.png", "bin06.png")
        if "bin7.png" in imageFileName: imageFileName = imageFileName.replace("bin7.png", "bin07.png")
        if "bin8.png" in imageFileName: imageFileName = imageFileName.replace("bin8.png", "bin08.png")
        if "bin9.png" in imageFileName: imageFileName = imageFileName.replace("bin9.png", "bin09.png")

        if "_bin0__" in imageFileName: imageFileName = imageFileName.replace("_bin0__", "_bin00__")
        if "_bin1__" in imageFileName: imageFileName = imageFileName.replace("_bin1__", "_bin01__")
        if "_bin2__" in imageFileName: imageFileName = imageFileName.replace("_bin2__", "_bin02__")
        if "_bin3__" in imageFileName: imageFileName = imageFileName.replace("_bin3__", "_bin03__")
        if "_bin4__" in imageFileName: imageFileName = imageFileName.replace("_bin4__", "_bin04__")
        if "_bin5__" in imageFileName: imageFileName = imageFileName.replace("_bin5__", "_bin05__")
        if "_bin6__" in imageFileName: imageFileName = imageFileName.replace("_bin6__", "_bin06__")
        if "_bin7__" in imageFileName: imageFileName = imageFileName.replace("_bin7__", "_bin07__")
        if "_bin8__" in imageFileName: imageFileName = imageFileName.replace("_bin8__", "_bin08__")
        if "_bin9__" in imageFileName: imageFileName = imageFileName.replace("_bin9__", "_bin09__")

        return imageFileName


    def SaveGraph_1D(self, effDirObject, graphName):
        canvas = effDirObject.GetListOfKeys().At(0).ReadObj()
        graph = canvas.GetPrimitive("hxy_fit_eff").Clone()
        graphName_before = canvas.GetName()
        graph.SetName( graphName )
        print "\tgraph: %s -> %s" % (graphName_before, graphName)

        self.outputFile.cd()
        graph.Write()


    def SaveGraph_2D(self, effDirObject, graphName_base):
        # -- is it pt - eta case or pt - abseta case?
        etaType = ""
        for key in effDirObject.GetListOfKeys():
            canvasName = key.GetName()
            if canvasName.startswith("pt_PLOT_abseta_bin"): etaType = "abseta"
            if canvasName.startswith("pt_PLOT_eta_bin"): etaType = "eta"

        if etaType == "":
            print "No eta type is found! ... it may not pt-eta or pt-abseta binning: not recognizable"
            sys.exit()

        list_graph = []

        # -- pt - eta (or abseta) bin case, vs pT plots 
        i_etabin = 0

        for key in effDirObject.GetListOfKeys():
            canvasName = key.GetName()
            if canvasName.startswith("pt_PLOT_%s_bin" % etaType):

                canvas = key.ReadObj()
                graph = canvas.GetPrimitive("hxy_fit_eff").Clone()

                name_before = canvas.GetName()
                name_after  = graphName_base + "_%s%d" % (etaType, i_etabin)
                graph.SetName( name_after )

                # -- Valiation: bin number is same?
                if "pt_PLOT_%s_bin%d" % (etaType, i_etabin) not in canvasName:
                    print "[TnPInfoExtractor::SaveGraph_2D]"
                    print "  i_etabin   = %d" % i_etabin
                    print "  canvasName = %s" % canvasName
                    print "    -> assigned bin number is not same with the true bin number!"
                    sys.exit()

                i_etabin += 1

                print "\tgraph: %s -> %s" % (name_before, name_after)
                list_graph += [graph]

        # -- pt - eta (or abseta) bin case, vs eta plots 
        i_ptbin = 0
        
        for key in effDirObject.GetListOfKeys():
            canvasName = key.GetName()
            if canvasName.startswith("%s_PLOT_pt_bin" % etaType):

                canvas = key.ReadObj()
                graph = canvas.GetPrimitive("hxy_fit_eff").Clone()

                name_before = canvas.GetName()
                name_after  = graphName_base + "_pt%d" % (i_ptbin)
                graph.SetName( name_after )

                # -- Valiation: bin number is same?
                if "%s_PLOT_pt_bin%d" % (etaType, i_ptbin) not in canvasName:
                    print "[TnPInfoExtractor::SaveGraph_2D]"
                    print "  i_ptbin    = %d" % i_ptbin
                    print "  canvasName = %s" % canvasName
                    print "    -> assigned bin number is not same with the true bin number!"
                    sys.exit()

                i_ptbin += 1

                print "\tgraph: %s -> %s" % (name_before, name_after)
                list_graph += [graph]

        self.outputFile.cd()
        for graph in list_graph:
            graph.Write()

    def MakeGraphName(self):
        graphName = ""
        if "data_25ns" in self.ROOTFileName:
            self.dataType = "Data"
            graphName = self.dataType + "_" + self.ROOTFileName.split("_data_25ns_")[1:][0].split(".root")[:1][0]

        elif "mc" in self.ROOTFileName:
            self.dataType = "MC"
            graphName = self.dataType + "_" + self.ROOTFileName.split("_mc_")[1:][0].split(".root")[:1][0]

        return graphName



class ROOTFileFeeder:
    def __init__(self):
        self.dirPath = "" # -- path to directory with TnP root files
        self.outputFile = TFile()

    def Feed(self):
        list_file = os.listdir(self.dirPath)

        list_ROOTFilePath = []
        for fileName in list_file:
            if fileName.endswith(".root") and "ROOTFile_" not in fileName:
                ROOTFilePath = "%s/%s" % (self.dirPath, fileName)
                list_ROOTFilePath.append(ROOTFilePath)

        for ROOTFilePath in list_ROOTFilePath:
            extractor = TnPInfoExtractor()
            extractor.ROOTFileName = ROOTFilePath
            extractor.outputFile = self.outputFile
            extractor.Extract()

            # print "Test -> break"
            # break


class HTMLGenerator:
    def __init__(self):
        self.dirPath = ""

    def Generate(self):
        htmlFile = open("fitCanvas.html", "w")
        htmlFile.write("<html>\n")
        self.DefaultHTMLStyleSetup(htmlFile)

        list_file = os.listdir(self.dirPath)

        list_file.sort()

        list_PNGDirPath = []
        for fitDirName in list_file:
            fitDirPath = "%s/%s" % (self.dirPath, fitDirName)
            PNGDirPath = "%s/PNG" % fitDirPath
            if os.path.isdir(fitDirPath) and os.path.isdir(PNGDirPath):
                self.WriteHTML_GivenPath(PNGDirPath, fitDirName, htmlFile)

        htmlFile.write("</html>\n")
        htmlFile.close()

    def WriteHTML_GivenPath(self, PNGDirPath, fitDirName, htmlFile):
        htmlCMD_title = "<div class=effType> %s </div>" % fitDirName
        htmlFile.write(htmlCMD_title+"\n")

        list_PNGFileName = []
        for fileNameInPNGDir in os.listdir(PNGDirPath):
            if fileNameInPNGDir.endswith(".png"):
                list_PNGFileName.append(fileNameInPNGDir)

        list_PNGFileName.sort()

        for PNGFileName in list_PNGFileName:
            PNGFilePath = "%s/%s" % (PNGDirPath, PNGFileName)
            htmlCMD = \
"""
<div class=image>
    <a href='{PNGFilePath_}' target='_blank'><img width=400 height=300 border=0 src='{PNGFilePath_}'></a>
    <div style='width:398'>{fileName_}</div>
</div>""".format(PNGFilePath_=PNGFilePath, fileName_=PNGFileName)

            htmlFile.write(htmlCMD+"\n")

        htmlFile.write("\n")

    def DefaultHTMLStyleSetup(self, htmlFile):
        htmlFile.write(
"""
<style>
    .effType {width:1200; height:50; font-size:20px; font-weight:bold; font-family:monospace; color:blue; text-align:center; clear:both;}
    .image { float:left; margin:5px; clear:justify; font-size:15px; font-weight:bold; font-family:monospace; text-align:center;}
</style>\n\n""")


# -- main part
outputFile = TFile("ROOTFile_EfficiencyGraphs.root", "RECREATE")

feeder = ROOTFileFeeder()
feeder.dirPath = "."
feeder.outputFile = outputFile
feeder.Feed()

outputFile.Close()

generator = HTMLGenerator()
generator.dirPath = "."
generator.Generate()