# (Automated) TnP fitter



## Environment

### Requirement

cvmfs (for CMSSW) should be available in the machine



### Download

```
# ssh: git clone git@github.com:KyeongPil-Lee/MuonTnPFitter.git -b master
git clone https://github.com/KyeongPil-Lee/MuonTnPFitter.git -b master
```



## Example: Run a Tag&Probe fitting

 ```
# -- use screen (to avoid job termination)
screen -S tnp

cd MuonTnPFitter
source setup.sh # -- it accesses to cvmfs and use cmsenv.

cd Workspace
python tnpcfg_example.py # -- it will create a directory for this job

# -- copy the command printed in the terminal and run
cd /scratch/User/kplee/TagProbe/MuonTnPFitter/master/Workspace/example_v01
bash run.sh >&run.log&
cd /scratch/User/kplee/TagProbe/MuonTnPFitter/master/Workspace

# -- escape screen
screen -d
 ```



### Structure of tnpcfg

```
automator.configName = "TriggerEff.py"
```

=> Configuration name in ```Template/Fitting_v01```



```
automator.inputTree = "/scratch/User/kplee/TagProbe/TnPTree/2018/TnPTreeZ_17Sep2018_SingleMuon_Run2018ABC_GoldenJSON.root"
```

=> TnP tree path (as an absolute path)



```
automator.isMC = False
```

=> is MC tree or not: If it is true, then (gen) weight branch will be saved during the skimming



```
automator.doSkim = True
automator.skimType = "101X_IsoMu24"
```

=> If ```doSkim = True```, skimming tree is done before starting the fitting: it is highly recommeneded to improve the performance (speed)

=> skimType can be checked in ```Template/Input/GenScript_TnPTree.py```

* Example: ```101X_IsoMu24```

  ```
  	elif Type == "101X_IsoMu24":
  		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
  		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
  		CutDef = CutDef_Tag + " && " + CutDef_Probe
  
  		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
  		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1SingleMu22", True])
  ```



```
automator.doRunSkim = True
automator.firstRun = 316361
automator.lastRun = 999999
```

=> If ```doRunSkim``` is True, then the data tree is skimmed to the given run range



```
automator.effList = [
"IsoMu24_from_Tight2012_and_dBeta_015",
"IsoMu24_from_L1SingleMu22_and_Tight2012_and_dBeta_015"]
```

=> efficiency types which wiill be given as a parameter for ```cmsRun```



### Output

Saved in ```example_v01/ResultROOTFiles_v01/Summary```

* ```FitCanvases.zip```: contains all fit canvases: 
  **should be checked one by one, without missing any plot!**
* ```ROOTFile_EfficiencyGraphs.root```: contains all efficiency graphs



### Example: Draw efficiency plots

```
cd $MUONTNP_PATH/Plot
root -l -b -q TnPEffPlots_Example.cxx
```





## Appendix

### nVtx reweighting (MC only)

This step should be done before TnP fitting.

How to add PU weights (by nVtx) in MC tree is:

```
root -l -b -q <input MC tree> <input Data tree> $MUONTNP_PATH/Template/Input/addWeights.cxx++

# -- output: <input MC tree name + WithWeights>.root 
# -- ex> input MC tree name = MCTree.root -> output = MCTree_WithWeights.root
```

* Example

  ```
  root -l -b -q \
  /scratch/kplee/TagProbe/TnPTree/2016/TnPTreeZ_Summer16_DYLL_M50_aMCNLO.root \
  /scratch/kplee/TagProbe/TnPTree/2016/TnPTreeZ_LegacyRereco07Aug17_SingleMuon_Run2016BtoF_GoldenJSON.root \
  $MUONTNP_PATH/Template/Input/addWeights.cxx++ >&addWeights_BtoF.log
  
  mv /scratch/kplee/TagProbe/TnPTree/2016/TnPTreeZ_Summer16_DYLL_M50_aMCNLO_WithWeights.root \
  /scratch/kplee/TagProbe/TnPTree/2016/TnPTreeZ_Summer16_DYLL_M50_aMCNLO_weightedToBtoF.root
  ```

  