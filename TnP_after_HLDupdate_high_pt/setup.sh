# if [ $MUONTNP_PATH ]; then
#     echo "KP_ANALYZER_PATH is already defined: use a clean shell!"
#     return 1
# fi

export MUONTNP_PATH=$(pwd)
export PYTHONPATH=${MUONTNP_PATH}:${PYTHONPATH}

# -- root setup
export ROOT_INCLUDE_PATH=${MUONTNP_PATH}:${ROOT_INCLUDE_PATH}

# -- cmssw setting
# export SCRAM_ARCH=slc6_amd64_gcc700
# cmsswVersion=CMSSW_10_2_1 # -- SkimTree is not working ... why?
# cmsswVersion=CMSSW_10_1_9 # -- SkimTree is not working ... why?
export SCRAM_ARCH=slc6_amd64_gcc630
cmsswVersion=CMSSW_9_2_0


source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/$SCRAM_ARCH/cms/cmssw/$cmsswVersion
eval `scramv1 runtime -sh`
cd $MUONTNP_PATH

echo "CMSSW is set ("$cmsswVersion")"