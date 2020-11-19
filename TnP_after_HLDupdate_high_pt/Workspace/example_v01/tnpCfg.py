import sys
from Python.TnPAutomator import TnPAutomator

automator = TnPAutomator()
automator.jobName = sys.argv[0].split("tnpcfg_")[1].split(".py")[0]
automator.configName = "TriggerEff.py"

automator.inputTree = "/scratch/kyhwang/DATA/2018UL_hadd/Run2018_A316361-D.root"
automator.isMC = False

automator.doSkim = True
automator.skimType = "101X_Mu50_NewHighPtID"

automator.doRunSkim = False
automator.firstRun = 316361
automator.lastRun = 999999

automator.effList = [
"Mu50_OR_OldMu100_OR_TkMu100_from_NewHighPtID_and_RelTrkIso_010",
"Mu50_OR_OldMu100_OR_TkMu100_from_L1SingleMu22_and_NewHighPtID_and_RelTrkIso_010"]


# automator.effList = [
# "IsoMu24_from_Tight2012_and_dBeta_015",
# "IsoMu24_from_L1SingleMu22_and_Tight2012_and_dBeta_015",
# "L1SingleMu22_from_Tight2012_and_dBeta_015",
# "L3_IsoMu24_from_L1SingleMu22_and_Tight2012_and_dBeta_015",
# "IsoF_IsoMu24_from_L3_IsoMu24_and_L1SingleMu22_and_Tight2012_and_dBeta_015" ]

# automator.GenerateScriptAndRun()
automator.GenerateScript()
