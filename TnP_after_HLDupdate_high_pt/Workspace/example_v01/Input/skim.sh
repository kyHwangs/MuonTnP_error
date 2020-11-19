#!bin/bash

ln -s /scratch/kyhwang/DATA/2018UL_hadd/Run2018_A316361-D.root ./Input_Base.root

        
#######################
# -- TnP Skim part -- #
#######################
python GenScript_TnPTree.py 101X_Mu50_NewHighPtID Input_Base.root 0
sleep 1 # -- just a second
source script_Input_Base_101X_Mu50_NewHighPtID.sh >&script_Input_Base_101X_Mu50_NewHighPtID.log

echo "TnP skim is finished"

        
        
mv Input_Base_101X_Mu50_NewHighPtID_addBranch_final.root Input_Final.root
rm *temp*.root

echo "skim part: finished"

        