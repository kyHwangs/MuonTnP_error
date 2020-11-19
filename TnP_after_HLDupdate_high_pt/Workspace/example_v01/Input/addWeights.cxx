#include "TTree.h"
#include "TFile.h"
#include "TStopwatch.h"
#include "TChain.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TLegend.h"
#include <vector>
#include <iostream>

// -- take into account both nVertex reweighting and gen-event weight
void addWeights(TString treeName="tpTree", TString cut = "")
{ 
  // Example of cut string:  TString cut="(tag_IsoMu20_eta2p1 || tag_IsoMu20) && tag_combRelIso < 0.15")

  if (gROOT->GetListOfFiles()->GetSize() < 2)
  {
      std::cerr << "[addWeights]: USAGE: root.exe -b -l -q mcFile.root dataFile.root [more data files...] addWeights.cxx+" << std::endl;
      return;
  }

  std::cout << "[addWeights]: Gathering input trees ..." << std::endl;

  TTree  &tMC = * (TTree *) ((TFile*)gROOT->GetListOfFiles()->At(0))->Get(treeName+"/fitter_tree");

  TChain tData( treeName+"/fitter_tree" );
  for (int i = 1; i < gROOT->GetListOfFiles()->GetSize(); ++i)
  {
    tData.AddFile(((TFile*)gROOT->GetListOfFiles()->At(i))->GetName());
  }

  std::cout << "[addWeights]: Filling distributions of vertices ..." << std::endl;

  tData.Draw("tag_nVertices>>hVtxData(100,-0.5,99.5)", cut);
  // tMC.Draw("tag_nVertices>>hVtxMC(100,-0.5,99.5)", cut);

  // -- pair_genWeight: used as a weight to make tag_nVertices plot
  // -- reference: https://root.cern.ch/root/htmldoc/guides/users-guide/Trees.html#simple-analysis-using-ttreedraw
  if( cut == "" )
    tMC.Draw("tag_nVertices>>hVtxMC(100,-0.5,99.5)", "pair_genWeight*(1)");
  else
    tMC.Draw("tag_nVertices>>hVtxMC(100,-0.5,99.5)", "pair_genWeight*("+cut+")");
  

  std::cout << "[addWeights]: Computing vertex weight vector ..." << std::endl;

  TH1F *hVtxData = (TH1F*) gROOT->FindObject("hVtxData");
  TH1F *hVtxMC = (TH1F*) gROOT->FindObject("hVtxMC");
  hVtxData->Scale(1.0/hVtxData->Integral());
  hVtxMC->Scale(1.0/hVtxMC->Integral());

  std::vector<double> vtxWeights(hVtxData->GetNbinsX()+1, 1.0);
  for (int i = 1, n = vtxWeights.size(); i < n; ++i) {
      double nMC = hVtxMC->GetBinContent(i), nData = hVtxData->GetBinContent(i);
      vtxWeights[i-1] = (nMC > 0 ? nData/nMC : 1.0);
  }

  std::cout << "[addWeights]: Adding weight column ..." << std::endl;

  Float_t nVtx, weight, genWeight;
  tMC.SetBranchAddress("tag_nVertices", &nVtx);
  tMC.SetBranchAddress("pair_genWeight", &genWeight);

  TString mcFileName(gROOT->GetListOfFiles()->At(0)->GetName());
  TString outFileName = (mcFileName.First(".") > 0 ? mcFileName(0,mcFileName.First(".")) : mcFileName)  + "_WithWeights.root";

  TFile *fOut = new TFile(outFileName, "RECREATE");
  fOut->mkdir("tpTree")->cd();
  TTree *tOut = tMC.CloneTree(0);
  tOut->Branch("weight", &weight, "weight/F");
  int step = tMC.GetEntries()/100;
  double evDenom = 100.0/double(tMC.GetEntries());
  TStopwatch timer; timer.Start();

  for (int i = 0, n = tMC.GetEntries(); i < n; ++i)
  {
    tMC.GetEntry(i);
    weight = vtxWeights[int(nVtx)];
    weight *= ( genWeight > 0 ? 1. : -1.);
    if (i < 20)
      printf("[addWeights]: Event with %d primary vertices gets a weight of %.4f\n", int(nVtx), weight);

    tOut->Fill();

    if ((i+1) % step == 0)
    { 
      double totalTime = timer.RealTime()/60.; timer.Continue();
      double fraction = double(i+1)/double(n+1), remaining = totalTime*(1-fraction)/fraction;
      printf("[addWeights]: Done %9d/%9d   %5.1f%%   (elapsed %5.1f min, remaining %5.1f min)\r", i, n, i*evDenom, totalTime, remaining); 
      fflush(stdout); 
    }
  }

  std::cout << std::endl;

  tOut->AutoSave(); // according to root tutorial this is the right thing to do

  TString weightPlusCut = cut.Length() > 0 ? "weight*(" + cut + ")" : "weight";
  tOut->Draw("(tag_nVertices)>>hVtxMCReweight(100,-0.5,99.5)", weightPlusCut);

  TH1F *hVtxMCReweight = (TH1F*) gROOT->FindObject("hVtxMCReweight");
  std::cout << "[addWeights]: Integral of MC vtx distribution after applying weights : " << hVtxMCReweight->Integral() << std::endl;
  hVtxMCReweight->Scale(1.0/hVtxMCReweight->Integral());

  TCanvas *cVtx = new TCanvas("cVtx","cVtx");

  hVtxData->SetLineColor(kOrange+7);
  hVtxMC->SetLineColor(kAzure+7);
  hVtxMCReweight->SetLineColor(kGreen+1);

  hVtxMCReweight->GetXaxis()->SetTitle("number of RECO vertices");

  hVtxMCReweight->Draw("hist");
  hVtxData->Draw("same");
  hVtxMC->Draw("same");

  TLegend * legVtx = new TLegend(0.6,0.5,0.9,0.7);
  legVtx->AddEntry(hVtxData,"data distribution","lep");
  legVtx->AddEntry(hVtxMC,"MC distribution before reweighting","lep");
  legVtx->AddEntry(hVtxMCReweight,"MC distribution after reweighting","lep");
  legVtx->Draw();

  cVtx->Print("nVtx.png");

/*
  TString ptPlotCut("(tag_IsoMu20 && tag_combRelIso < 0.15 && pt > 20 && Tight2012)");

  tOut->Draw("pt>>hPtMCReweight(150,-0.5,199.5)", ptPlotCut + " * weight");
  tData.Draw("pt>>hPtData(150,-0.5,199.5)", ptPlotCut );
  tMC.Draw("pt>>hPtMC(150,-0.5,199.5)", ptPlotCut );

  TH1F *hPtMC = (TH1F*) gROOT->FindObject("hPtMC");
  TH1F *hPtData = (TH1F*) gROOT->FindObject("hPtData");
  TH1F *hPtMCReweight = (TH1F*) gROOT->FindObject("hPtMCReweight");

  hPtMC->Scale(1.0/hPtMC->Integral());
  hPtData->Scale(1.0/hPtData->Integral());
  hPtMCReweight->Scale(1.0/hPtMCReweight->Integral());

  TCanvas *cPt = new TCanvas("cPt","cPt");

  hPtData->SetLineColor(kOrange+7);
  hPtMC->SetLineColor(kAzure+7);
  hPtMCReweight->SetLineColor(kGreen+1);

  hPtMCReweight->GetXaxis()->SetTitle("tight muon p_{T}");

  hPtMCReweight->Draw("hist");
  hPtData->Draw("same");
  hPtMC->Draw("same");

  TLegend * legPt = new TLegend(0.6,0.5,0.9,0.7);
  legPt->AddEntry(hPtData,"data distribution","lep");
  legPt->AddEntry(hPtMC,"MC distribution before reweighting","lep");
  legPt->AddEntry(hPtMCReweight,"MC distribution after reweighting","lep");
  legPt->Draw();

  cPt->Print("pt.png");
*/
  std::cout << "[addWeights]: Wrote output to " << fOut->GetName() << std::endl;
  fOut->Close();
}

