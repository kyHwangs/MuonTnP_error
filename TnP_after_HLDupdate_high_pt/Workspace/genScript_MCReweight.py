from Python.ScriptGenerator_MCReweight import ScriptGenerator

generator = ScriptGenerator()

generator.reweightCode = "$MUONTNP_PATH/Template/Input/addWeights.cxx"

# -- path: must be absolute path
generator.scriptName = "script_Reweight_94X.sh"
generator.inputData = "/scratch/kplee/TagProbe/TnPTree/2017/TnPTreeZ_17Nov2017_SingleMuon_Run2017All_Incomplete_20190527.root"
generator.inputMC   = "/scratch/kplee/TagProbe/TnPTree/2017/TnPTreeZ_94X_DYJetsToLL_M50_MadgraphMLM_Incomplete_20190527.root"
generator.outputMC  = "/scratch/kplee/TagProbe/TnPTree/2017/TnPTreeZ_94X_DYJetsToLL_M50_MadgraphMLM_Incomplete_20190527_Reweighted.root"
generator.Register()
generator.Generate()

generator.scriptName = "script_Reweight_106X.sh"
generator.inputData = "/scratch/kplee/TagProbe/TnPTree/2017/TnPTreeZ_17Nov2017_SingleMuon_Run2017All_Incomplete_20190527.root"
generator.inputMC   = "/scratch/kplee/TagProbe/TnPTree/2019/TnPTreeZ_1060pre2_RelValZMM.root"
generator.outputMC  = "/scratch/kplee/TagProbe/TnPTree/2019/TnPTreeZ_1060pre2_RelValZMM_Reweighted.root"
generator.Register()
generator.Generate()


