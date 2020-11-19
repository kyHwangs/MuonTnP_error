import os, sys

class TnPAutomator:
    def __init__(self):
        self.jobName = ""
        self.configName = ""
        self.inputTree = ""
        self.isMC = ""
        self.noMCWeight = False

        self.doSkim = False
        self.skimType = ""
        self.doRunSkim = False
        self.firstRun = 0
        self.lastRun = 999999
        self.effList = []

        # -- internal variables
        self.analyzerPath = os.environ["MUONTNP_PATH"]
        self.templatePath = self.analyzerPath+"/Template"
        self.basePath = self.analyzerPath+"/Workspace"
        self.WSPath = ""

        self.skimScriptName = "skim.sh"
        self.tnpScriptName = "runTnP.sh"
        self.summaryScriptName = "summary.sh"
        self.masterScriptName = "run.sh"

    def GenerateScriptAndRun(self):
        self.GenerateScript()
        self.RunScript()
        
    def RunScript(self):
        print "do nothing yet"

    def GenerateScript(self):
        self.CheckOptions()
        self.PrintOptions()

        self.CreateWorkSpaceDir()
        self.GenerateSkimScript()
        self.GenerateTnPScript()
        self.GenerateMasterScript()

        print "+" * 100
        print "Scripts are generated"
        print "please run in a new shell (screen): "
        print "cd %s" % self.WSPath
        print "bash %s >&%s.log&" % (self.masterScriptName, self.masterScriptName.split(".sh")[0])
        print "cd %s" % self.basePath
        print "+" * 100

    def CreateWorkSpaceDir(self):
        i = 1
        while "%s_v%02d" % (self.jobName, i) in os.listdir(self.basePath):
            i = i+1

        dirName = "%s_v%02d" % (self.jobName, i)
        self.WSPath = "%s/%s" % (self.basePath, dirName)
        os.mkdir(self.WSPath)
        print "Workspace: %s" % self.WSPath

        cmd_cp_Template = "cp -r %s/* %s" % (self.templatePath, self.WSPath)
        # print cmd_cp_Template
        os.system(cmd_cp_Template)

        cmd_cp_tnpcfg = "cp %s %s" % (sys.argv[0], self.WSPath+"/tnpCfg.py")
        # print cmd_cp_tnpcfg
        os.system(cmd_cp_tnpcfg)


    def GenerateSkimScript(self):
        dirPath = "%s/Input" % (self.WSPath)
        scriptPath = "%s/%s" % (dirPath, self.skimScriptName)

        treeName_init = "Input_Base.root"
        treeName_final = "Input_Final.root"

        # -- write the script
        f = open(scriptPath, "w")

        cmd_link_inputFile = "ln -s %s ./%s" % (self.inputTree, treeName_init)

        f.write(
"""#!bin/bash

{cmd_link_inputFile_}

        """.format(cmd_link_inputFile_=cmd_link_inputFile))

        # -- the latest tree at this point
        treeName_latest = treeName_init

        if self.doRunSkim:
            treeName_latest = self.AddRunSkimPart(treeName_latest, f )

        if self.doSkim:
            treeName_latest = self.AddSkimPart(treeName_latest, f )


        cmd_changeName = "mv %s Input_Final.root" % treeName_latest
        cmd_rmTemp = "rm *temp*.root"
        f.write("""
        
{cmd_changeName_}
{cmd_rmTemp_}

echo "skim part: finished"

        """.format(cmd_changeName_=cmd_changeName,
                   cmd_rmTemp_=cmd_rmTemp))


        f.close()

    def AddSkimPart( self, treeName_input, f ):
        flag_isMC = 0
        if self.isMC: flag_isMC = 1
        cmd_genScript = "python GenScript_TnPTree.py %s %s %d" % (self.skimType, treeName_input, flag_isMC)

        skimScriptName = "script_%s_%s.sh" % (treeName_input.split(".root")[0], self.skimType)
        cmd_runSkimScript = 'source %s >&%s.log' % (skimScriptName, skimScriptName.split(".sh")[0])

        f.write("""
#######################
# -- TnP Skim part -- #
#######################
{cmd_genScript_}
sleep 1 # -- just a second
{cmd_runSkimScript_}

echo "TnP skim is finished"

        """.format(cmd_genScript_=cmd_genScript,
                   cmd_runSkimScript_=cmd_runSkimScript))

        treeName_output = "%s_%s_addBranch_final.root" % (treeName_input.split(".root")[0], self.skimType)

        return treeName_output


    def AddRunSkimPart( self, treeName_input, f ):
        treeName_runSkimmed = "Input_RunSkimmed.root"
        cmd_runSkim = 'python SkimTree.py "%s" "%s" -c "run >= %d && run <= %d"' % (treeName_input, treeName_runSkimmed, self.firstRun, self.lastRun)

        f.write("""
###########################
# -- TnP Run-Skim part -- #
###########################
{cmd_runSkim_}

echo "TnP run skim is finished"

        """.format(cmd_runSkim_=cmd_runSkim))

        return treeName_runSkimmed


    def GenerateTnPScript(self):
        dirPath = "%s/Fitting_v01" % self.WSPath
        scriptPath = "%s/%s" % (dirPath, self.tnpScriptName)

        f_script = open(scriptPath, "w")
        f_script.write("#!bin/bash\n\n")

        dataType = "data_25ns"
        if self.isMC:                     dataType = "mc_weight"
        if self.isMC and self.noMCWeight: dataType = "mc"

        for effType in self.effList:
            cmd_eff = ""
            if "," in effType:
                effDef   = effType.split(",")[0]
                systMode = effType.split(",")[1]
                cmd_eff = "cmsRun %s %s %s %s >&%s_%s.log" % (self.configName, dataType, effDef, systMode, effDef, systMode)
            else:
                cmd_eff = "cmsRun %s %s %s >&%s.log" % (self.configName, dataType, effType, effType)
            f_script.write(cmd_eff+"\n")

        f_script.write('\necho "TnP fitting: finished"\n')

        f_script.close()

    def GenerateMasterScript(self):

        dirPath = self.WSPath
        scriptPath = "%s/%s" % (dirPath, self.masterScriptName)

        f_master = open(scriptPath, "w")
        f_master.write(
"""#!bin/bash

start=`date +%s`

# -- setup CMSSW, enviornment variables ...
cd {analyzerPath_}
source setup.sh

cd {WSPath_}

cd Input
source {skimScript_}.sh >&{skimScript_}.log
echo "Skim: finished"

cd ../Fitting_v01
source {tnpScript_}.sh >&{tnpScript_}.log
echo "TnP: finished"

cd ../ResultROOTFiles_v01
source {summaryScript_}.sh >&{summaryScript_}.log
echo "Summary: finished"

cd ..
echo "All jobs are finished"

end=`date +%s`

runtime=$((end-start))

echo "   start:   "$start
echo "   end:     "$end
echo "   runtime: "$runtime


        """.format(analyzerPath_=self.analyzerPath,
                   WSPath_=self.WSPath, 
                   skimScript_=self.skimScriptName.split(".sh")[0],
                   tnpScript_=self.tnpScriptName.split(".sh")[0],
                   summaryScript_=self.summaryScriptName.split(".sh")[0] ))


        f_master.close()


    def PrintOptions(self):
        print "jobName: %s" % self.jobName
        print "CMSSW config.: %s" % self.configName

    def CheckOptions(self):
        if self.jobName == "" or \
           self.configName == "":
           print "at least one of the mandatory option is not set!"
           self.PrintOptions()
           sys.exit()

