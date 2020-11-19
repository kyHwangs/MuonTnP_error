#!bin/bash

start=`date +%s`

# -- setup CMSSW, enviornment variables ...
cd /scratch/kyhwang/TnP_after_HLDupdate_high_pt
source setup.sh

cd /scratch/kyhwang/TnP_after_HLDupdate_high_pt/Workspace/example_v01

cd Input
source skim.sh >&skim.log
echo "Skim: finished"

cd ../Fitting_v01
source runTnP.sh >&runTnP.log
echo "TnP: finished"

cd ../ResultROOTFiles_v01
source summary.sh >&summary.log
echo "Summary: finished"

cd ..
echo "All jobs are finished"

end=`date +%s`

runtime=$((end-start))

echo "   start:   "$start
echo "   end:     "$end
echo "   runtime: "$runtime


        