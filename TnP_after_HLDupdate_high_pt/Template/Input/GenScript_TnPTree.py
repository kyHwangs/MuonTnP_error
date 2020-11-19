import sys

def Set_Default( BranchList, _isMC ):
	# -- Binning variables -- #
	BranchList.append( "pt" )
	BranchList.append( "eta" )
	BranchList.append( "abseta" )
	BranchList.append( "phi" )
	BranchList.append( "tag_nVertices" )

	# -- Tag conditions -- #
	BranchList.append( "tag_pt" )
	BranchList.append( "tag_eta")
	BranchList.append( "tag_abseta" )
	BranchList.append( "tag_phi")

	BranchList.append( "tag_IsoMu*" )
	BranchList.append( "tag_IsoTkMu*" )
	BranchList.append( "tag_combRelIsoPF04dBeta" )
	if not _isMC:
		BranchList.append( "tag_bx")
		BranchList.append( "tag_instLumi")

	BranchList.append( "l1ptByQ" )
	BranchList.append( "l1drByQ" )
	BranchList.append( "l1qByQ" )

	BranchList.append( "IsoMu*" )
	BranchList.append( "IsoTkMu*" )
	BranchList.append( "OldMu*" )
	BranchList.append( "TkMu*" )
	BranchList.append( "Mu50" )
	BranchList.append( "HLT_TkMu50" )

	BranchList.append( "Loose" )
	BranchList.append( "Medium" )
	BranchList.append( "Medium2016" )
	BranchList.append( "Tight2012" )
	BranchList.append( "HighPt" )
	BranchList.append( "CutBasedIdGlobalHighPt_new" )
	BranchList.append( "TM" )

	BranchList.append( "relTkIso" )
	BranchList.append( "combRelIsoPF04dBeta" )

	# -- else -- #
	BranchList.append( "run" )
	BranchList.append( "lumi" )
	BranchList.append( "event" )
	BranchList.append( "mass" )
	BranchList.append( "pair_deltaR" )
	BranchList.append( "pair_probeMultiplicity_Pt10_M60140" )
	if _isMC:
		BranchList.append( "weight" )
		BranchList.append( "pair_genWeight" )


def Set_List_Cuts( Type, isMC, BranchList, AddList ):
	CutDef = ""

	if Type == "DY2016":
		cutDef_tag   = "tag_IsoMu24==1 && fabs(tag_eta) < 2.4 && tag_combRelIsoPF04dBeta > 0.09 && tag_pt > 24.9" # -- 24.9, not 25.9: for syst. unc.
		cutDef_probe = "pt > 16.9"
		CutDef = cutDef_tag + " && " + cutDef_probe

		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])
		AddList.append(["IsoMu24==1 or IsoTkMu24==1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])

	elif Type == "Zg_ForID":
		CutDef_TagOfficial = "tag_IsoMu24==1 && abs(tag_eta) < 2.4 && tag_pt > 24.9"
		CutDef_ID = "pt > 9.9 && pair_probeMultiplicity_Pt10_M60140 == 1 && mass > 76.9 && mass < 130.5"
		CutDef = CutDef_TagOfficial + " && " + CutDef_ID

	elif Type == "Zg_ForIso":
		CutDef_TagOfficial = "tag_IsoMu24==1 && abs(tag_eta) < 2.4 && tag_pt > 24.9"
		CutDef_ID = "pt > 9.9 && pair_probeMultiplicity_Pt10_M60140 == 1 && mass > 76.9 && mass < 130.5"
		CutDef = CutDef_TagOfficial + " && " + CutDef_ID
		
		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])

	elif "Zg_ForTrig" in Type:
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 24.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "relTkIso < 0.10 && pt > 9.9"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["Mu50 == 1 or HLT_TkMu50 == 1;Mu50;HLT_TkMu50", "Mu50_OR_TkMu50", True])
		AddList.append(["abs(tag_phi - phi) if abs(tag_phi - phi) < 3.1415926535 else 2*3.1415926535 - abs(tag_phi - phi);tag_eta;eta;phi;tag_phi", "pair_dPhi", False])
		AddList.append(["pair_dPhi*(180/3.1415926535) if ((tag_eta > 0.9 and eta > 0.9) or (tag_eta < -0.9 and eta < -0.9)) else 999;pair_dPhi;tag_eta;eta;phi;tag_phi", "pair_dPhiPrimeDeg", False])

 		if "Loose" in Type:
			CutDef = CutDef + " && Loose"

		if "HighPt" in Type:
			CutDef = CutDef + " && HighPt"

		# if "Period3" in Type:
		# 	CutDef_AfterPhiFix = 'run > 278167 - 0.5'
		# 	CutDef = CutDef + " && " + CutDef_AfterPhiFix

		# elif "Period1" in Type:
		# 	CutDef = CutDef + " && run < 274094 - 0.5"
		# 	AddList.append(["abs(tag_phi - phi) if abs(tag_phi - phi) < 3.1415926535 else 2*3.1415926535 - abs(tag_phi - phi);tag_eta;eta;phi;tag_phi", "pair_dPhi", False])
		# 	AddList.append(["pair_dPhi*(180/3.1415926535) if ((tag_eta > 0.9 and eta > 0.9) or (tag_eta < -0.9 and eta < -0.9)) else 999;pair_dPhi;tag_eta;eta;phi;tag_phi", "pair_dPhiPrimeDeg", False])

		# elif "Period2" in Type:
		# 	CutDef = CutDef + " && run > 274094 - 0.5 && run < 278167 - 0.5"
		# 	AddList.append(["abs(tag_phi - phi) if abs(tag_phi - phi) < 3.1415926535 else 2*3.1415926535 - abs(tag_phi - phi);tag_eta;eta;phi;tag_phi", "pair_dPhi", False])
		# 	AddList.append(["pair_dPhi*(180/3.1415926535) if ((tag_eta > 0.9 and eta > 0.9) or (tag_eta < -0.9 and eta < -0.9)) else 999;pair_dPhi;tag_eta;eta;phi;tag_phi", "pair_dPhiPrimeDeg", False])

	elif "Zg_Test_NoUpperMW" in Type:
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt>25.9 && mass > 69.99" # -- tag condition -- #
		CutDef_Probe = "relTkIso < 0.10 && pt > 9.9"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["IsoMu24 == 1 or IsoTkMu24 == 1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])
		AddList.append(["abs(tag_phi - phi) if abs(tag_phi - phi) < 3.1415926535 else 2*3.1415926535 - abs(tag_phi - phi);tag_eta;eta;phi;tag_phi", "pair_dPhi", False])
		AddList.append(["pair_dPhi*(180/3.1415926535) if ((tag_eta > 0.9 and eta > 0.9) or (tag_eta < -0.9 and eta < -0.9)) else 999;pair_dPhi;tag_eta;eta;phi;tag_phi", "pair_dPhiPrimeDeg", False])

		if "Loose" in Type:
			CutDef = CutDef + " && Loose"

		if "HighPt" in Type:
			CutDef = CutDef + " && HighPt"

	elif Type == "ForTrigFilters92X":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL2fL1sSingleMu22L1f0L2Filtered10Q" )
		BranchList.append( "hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q" )
		BranchList.append( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07" )
		BranchList.append( "hltL3fL1sMu22f0TkFiltered24Q" )
		BranchList.append( "hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07" )

		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu24", True])
		AddList.append(["hltL2fL1sSingleMu22L1f0L2Filtered10Q == 1;hltL2fL1sSingleMu22L1f0L2Filtered10Q", "L2_IsoMu24", True])
		AddList.append(["hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q == 1;hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q", "L3_IsoMu24", True])
		AddList.append(["hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07", "IsoF_IsoMu24", True])

		AddList.append(["hltL3fL1sMu22f0TkFiltered24Q == 1;hltL3fL1sMu22f0TkFiltered24Q", "TkMuF_IsoTkMu24", True])
		AddList.append(["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07 == 1;hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07", "IsoF_IsoTkMu24", True])

		AddList.append(["hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q == 1 or hltL3fL1sMu22f0TkFiltered24Q == 1;hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q;hltL3fL1sMu22f0TkFiltered24Q", "L3_IsoMu24_OR_TkMuF_IsoTkMu24", True])
		AddList.append(["hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 == 1 or hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07;hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07", "IsoF_IsoMu24_OR_IsoF_IsoTkMu24", True])

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])

		AddList.append(["IsoMu24==1 or IsoTkMu24==1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])
		AddList.append(["IsoMu27==1 or IsoTkMu27==1;IsoMu27;IsoTkMu27", "IsoMu27_OR_IsoTkMu27", True])


	elif Type == "ForTrigFilters92XIterL3_IsoMu24":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		# CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL2fL1sSingleMu22L1f0L2Filtered10Q" )
		BranchList.append( "hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q" )
		BranchList.append( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07" )

		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu24", True])
		AddList.append(["hltL2fL1sSingleMu22L1f0L2Filtered10Q == 1;hltL2fL1sSingleMu22L1f0L2Filtered10Q", "L2_IsoMu24", True])
		AddList.append(["hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q == 1;hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q", "L3_IsoMu24", True])
		AddList.append(["hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07", "IsoF_IsoMu24", True])

		# AddList.append(["hltL3fL1sMu22f0TkFiltered24Q == 1;hltL3fL1sMu22f0TkFiltered24Q", "TkMuF_IsoTkMu24", True])
		# AddList.append(["hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07 == 1;hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07", "IsoF_IsoTkMu24", True])

		# AddList.append(["hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q == 1 or hltL3fL1sMu22f0TkFiltered24Q == 1;hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q;hltL3fL1sMu22f0TkFiltered24Q", "L3_IsoMu24_OR_TkMuF_IsoTkMu24", True])
		# AddList.append(["hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 == 1 or hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07;hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p07", "IsoF_IsoMu24_OR_IsoF_IsoTkMu24", True])

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])

		# AddList.append(["IsoMu24==1 or IsoTkMu24==1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])
		# AddList.append(["IsoMu27==1 or IsoTkMu27==1;IsoMu27;IsoTkMu27", "IsoMu27_OR_IsoTkMu27", True])

	elif Type == "ForTrigFilters92XIterL3_IsoMu27":
		# CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL2fL1sMu22or25L1f0L2Filtered10Q" )
		BranchList.append( "hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q" )
		BranchList.append( "hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07" )

		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["hltL2fL1sMu22or25L1f0L2Filtered10Q == 1;hltL2fL1sMu22or25L1f0L2Filtered10Q", "L2_IsoMu27", True])
		AddList.append(["hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q == 1;hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q", "L3_IsoMu27", True])
		AddList.append(["hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07", "IsoF_IsoMu27", True])

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])

	elif Type == "92X_Mu50":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "HighPt && relTkIso < 0.10" # -- offline selection -- #
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])

	# -- use same tag condition with 92X case - to compare with 2017 under exact same condition -- #
	elif Type == "80X_IsoMu27":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15" # -- offline selection -- #
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		# BranchList.append( "hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09" )
		# BranchList.append( "hltL3fL1sMu22Or25L1f0Tkf27QL3trkIsoFiltered0p09" )
		# BranchList.append( "hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q" )
		# BranchList.append( "hltL3fL1sMu22Or25f0TkFiltered27Q" )

		AddList.append(["IsoMu27 == 1 or IsoTkMu27 == 1;IsoMu27;IsoTkMu27", "IsoMu27_OR_IsoTkMu27", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])

		# -- TnP tree don't have filter information for IsoMu27 -- #
		# # -- L3 -- #
		# AddList.append(["hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q == 1;hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q", "L3_IsoMu27", True])
		# AddList.append(["hltL3fL1sMu22Or25f0TkFiltered27Q == 1;hltL3fL1sMu22Or25f0TkFiltered27Q", "TkMuF_IsoTkMu27", True])
		# AddList.append(["L3_IsoMu27 == 1 or TkMuF_IsoTkMu27 == 1;L3_IsoMu27;TkMuF_IsoTkMu27", "L3_OR_TkMuF_IsoMu27", True])

		# -- IsoF -- #
		# AddList.append(["hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09 == 1;hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p09", "IsoF_IsoMu27", True])
		# AddList.append(["hltL3fL1sMu22Or25L1f0Tkf27QL3trkIsoFiltered0p09 == 1;hltL3fL1sMu22Or25L1f0Tkf27QL3trkIsoFiltered0p09", "IsoF_IsoTkMu27", True])
		# AddList.append(["IsoF_IsoMu27 == 1 or IsoF_IsoTkMu27 == 1;IsoF_IsoMu27;IsoF_IsoTkMu27", "IsoF_IsoMu27_OR_IsoF_IsoTkMu27", True])

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])

	# -- use same tag condition with 92X case - to compare with 2017 under exact same condition -- #
	elif Type == "80X_Mu50":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15" # -- offline selection -- #
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["Mu50 == 1 or HLT_TkMu50 == 1;Mu50;HLT_TkMu50", "Mu50_OR_TkMu50", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])

	# -- use same tag condition with 92X case - to compare with 2017 under exact same condition -- #
	elif Type == "80X_IsoMu24":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "HighPt && relTkIso < 0.10" # -- offline selection -- #
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL3fL1sMu22L1f0L2f10QL3Filtered24Q" )
		BranchList.append( "hltL3fL1sMu22f0TkFiltered24Q" )

		AddList.append(["IsoMu24 == 1 or IsoTkMu24 == 1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["hltL3fL1sMu22L1f0L2f10QL3Filtered24Q == 1;hltL3fL1sMu22L1f0L2f10QL3Filtered24Q", "L3_IsoMu24", True])
		AddList.append(["hltL3fL1sMu22f0TkFiltered24Q == 1;hltL3fL1sMu22f0TkFiltered24Q", "TkMuF_IsoTkMu24", True])
		AddList.append(["L3_IsoMu24 == 1 or TkMuF_IsoTkMu24 == 1;L3_IsoMu24;TkMuF_IsoTkMu24", "L3_OR_TkMuF_IsoMu24", True])
		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])

	elif Type == "92X_OldMu100":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "HighPt && relTkIso < 0.10" # -- offline selection -- #
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["OldMu100 == 1 or TkMu100 == 1;OldMu100;TkMu100", "OldMu100_OR_TkMu100", True])
		AddList.append(["Mu50 == 1 or OldMu100 == 1;Mu50;OldMu100", "Mu50_OR_OldMu100", True])
		AddList.append(["Mu50 == 1 or TkMu100 == 1;Mu50;TkMu100", "Mu50_OR_TkMu100", True])

		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])

	elif Type == "94X_IsoMu27":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])

	elif Type == "94X_Mu50":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "HighPt && relTkIso < 0.10"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])

	elif Type == "94X_IsoMu27Filters":
		CutDef_Tag = "tag_IsoMu27==1 && tag_pt > 28.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q" )
		BranchList.append( "hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07" )

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu27", True])
		AddList.append(["hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q == 1;hltL3fL1sMu22Or25L1f0L2f10QL3Filtered27Q", "L3_IsoMu27", True])
		AddList.append(["hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07", "IsoF_IsoMu27", True])

	elif Type == "101X_IsoMu24Filters":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		BranchList.append( "hltL2fL1sSingleMu22L1f0L2Filtered10Q" )
		BranchList.append( "hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q" )
		BranchList.append( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07" )

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1_IsoMu24", True])

		AddList.append(["hltL2fL1sSingleMu22L1f0L2Filtered10Q == 1;hltL2fL1sSingleMu22L1f0L2Filtered10Q", "L2_IsoMu24", True])
		AddList.append(["hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q == 1;hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q", "L3_IsoMu24", True])
		AddList.append(["hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 == 1;hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07", "IsoF_IsoMu24", True])
		

	elif Type == "101X_Mu50":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "HighPt && relTkIso < 0.10"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1SingleMu22", True])


	elif Type == "101X_Mu50_NewHighPtID":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "CutBasedIdGlobalHighPt_new > 0.5 && relTkIso < 0.10"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1SingleMu22", True])
		AddList.append(["CutBasedIdGlobalHighPt_new > 0.5;CutBasedIdGlobalHighPt_new", "NewHighPtID", True])


	elif Type == "101X_IsoMu24":
		CutDef_Tag = "tag_IsoMu24==1 && tag_pt > 25.9 && mass > 69.5 && mass < 130.5" # -- tag condition -- #
		CutDef_Probe = "Tight2012 && combRelIsoPF04dBeta < 0.15"
		CutDef = CutDef_Tag + " && " + CutDef_Probe

		AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
		AddList.append(["l1ptByQ >= 22 and l1qByQ == 12 and l1drByQ < 0.3;l1ptByQ;l1qByQ;l1drByQ", "L1SingleMu22", True])


	return CutDef

	# elif Type == "asdf":
		# CutDef_LowPtProbe = "Tight2012 && combRelIsoPF04dBeta < 0.15" # -- offline selection -- #
		# CutDef_HighPtProbe = "HighPt && relTkIso < 0.10" # -- offline selection -- #
		# AddList.append(["abs(tag_phi - phi) if abs(tag_phi - phi) < 3.1415926535 else 2*3.1415926535 - abs(tag_phi - phi);tag_eta;eta;phi;tag_phi", "pair_dPhi", False])
		# AddList.append(["pair_dPhi*(180/3.1415926535) if ((tag_eta > 0.9 and eta > 0.9) or (tag_eta < -0.9 and eta < -0.9)) else 999;pair_dPhi;tag_eta;eta;phi;tag_phi", "pair_dPhiPrimeDeg", False])
		# AddList.append(["combRelIsoPF04dBeta < 0.15;combRelIsoPF04dBeta", "dBeta_015", True])
		# AddList.append(["relTkIso < 0.10;relTkIso", "RelTrkIso_010", True])
		# AddList.append(["IsoMu24 == 1 or IsoTkMu24 == 1;IsoMu24;IsoTkMu24", "IsoMu24_OR_IsoTkMu24", True])
		# AddList.append(["Mu50 == 1 or HLT_TkMu50 == 1;Mu50;HLT_TkMu50", "Mu50_OR_TkMu50", True])

###################
# -- main part -- #
###################

Type = sys.argv[1]
InputName = sys.argv[2]
isMC = int(sys.argv[3])

#####################
# -- input, isMC -- #
#####################
# TreeNames = []
# TreeNames.append( ["TnPTree_Run2016BCDEF.root", 0] )
# TreeNames.append( ["TnPTree_Run2016GH.root", 0] )
# TreeNames.append( ["TnPTree_Madgraph_Moriond17.root", 1] )
#################################################################################

# InputName = treename[0]
OutputName = InputName.split(".root")[0] + "_" + Type + ".root";
# isMC = treename[1]

BranchList = [] # -- branches to be kept -- #
CutDef = "" # -- cut definition -- #
AddList = [] # -- structure: [definition, new brach name, isInt] -- #

Set_Default( BranchList, isMC )
CutDef = Set_List_Cuts( Type, isMC, BranchList, AddList )

print "CutDef: ", CutDef

Command_SkimTree = 'python SkimTree.py "%s" "%s" -r "*" -k "' % (InputName, OutputName)
for branch in BranchList:
	Command_SkimTree  = Command_SkimTree + '%s' % (branch)
	if branch != BranchList[len(BranchList)-1]: # -- if it is not the last one -- #
		Command_SkimTree = Command_SkimTree + " "
Command_SkimTree = Command_SkimTree + '"'

Command_SkimTree = Command_SkimTree + ' -c "%s"' % CutDef

print "[SkimTree] (Input = %s, Output = %s)\n\tCommand=%s" % (InputName, OutputName, Command_SkimTree)

i_branch = 1
OutputName_temp_before = OutputName
Commands_addBranch = []
for newbranch in AddList:
	BranchDef = newbranch[0]
	BranchName = newbranch[1]
	isInt = newbranch[2]

	OutputName_temp = "";

	if( newbranch == AddList[len(AddList)-1]):  # -- if it is the last one -- #
		OutputName_temp = OutputName.split(".root")[0] + "_addBranch_final.root"
	else:
		OutputName_temp = OutputName.split(".root")[0] + "_addBranch_temp%.0d.root" % (i_branch)
		i_branch = i_branch + 1

	FileName_addBranch = 'addBranch_Int.py' if isInt == True else 'addBranch.py'
	Command = 'python %s "%s" "%s" "%s" "%s"' % (FileName_addBranch, OutputName_temp_before, OutputName_temp, BranchDef, BranchName)

	print "[AddBranch] (Input = %s, Output = %s)\n\tCommand=%s\n" % (OutputName_temp_before, OutputName_temp, Command)

	Commands_addBranch.append( Command )

	OutputName_temp_before = OutputName_temp

FileName = "script_"+OutputName.split(".root")[0]+".sh"

f = open(FileName, "w")
f.write(
"""#!/bin/bash

#########################################################
# -- qsub commands: #$ + command (details: man qsub) -- #
#########################################################
# -- shell used for executing the script -- #
#$ -S /bin/sh

# -- combine standard output & error file -- #
#$ -j y

# -- send the mail when the job is aborted or ended -- #
#$ -m ae -M kplee@cern.ch

# -- stay in the directory where qsub command is executed -- #
#$ -cwd

cwd=$(pwd)

# export SCRAM_ARCH=slc6_amd64_gcc530
# export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
# source $VO_CMS_SW_DIR/cmsset_default.sh

# -- CMSSW enviornment -- #
# cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_13
# cmsenv

cd ${cwd}""")
f.write( "\n" )
f.write( Command_SkimTree )
f.write( "\n" )
for command in Commands_addBranch:
	f.write( command )
	f.write( "\n" )

f.write("""
echo "job is completed"

# -- &>log: "Invalid null command" Error occurs. please use >&log. -- #

# -- PLEASE ENTER AFTER THE LAST LINE! ... IF YOU DON'T, LAST LINE WILL NOT BE EXECUTED BY BATCH JOB -- # 
"""
	)

f.close()

print "\t\t %s is generated\n" % (FileName)