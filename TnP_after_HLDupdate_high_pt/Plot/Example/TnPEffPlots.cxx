#include <Include/TnPEffPlotTools.h>

class TnPPlotProducer
{
public:
  TString effType_;
  vector<TString> vec_var_;

  TnPPlotProducer(TString effType, vector<TString> vec_var)
  {
    effType_ = effType;
    vec_var_ = vec_var;
  }

  void Produce()
  {
    for(const auto& var : vec_var_ )
    {
      ProducePlot_GivenVar( var );
      if( var == "pt" ) ProducePlot_GivenVar( var, kTRUE );
    }
  }

private:
  void ProducePlot_GivenVar( TString var, Bool_t isZoomInPlot = kFALSE )
  {
    TString fileName_2016 = "ROOTFile_EfficiencyGraphs_Data_2016.root";
    TString fileName_2017 = "ROOTFile_EfficiencyGraphs_Data_2017.root";
    TString fileName_2018 = "ROOTFile_EfficiencyGraphs_Data_2018.root";

    TString effType_2016 = effType_;
    effType_2016.ReplaceAll("Mu50_from", "Mu50_OR_TkMu50_from");
    TnPPlot::TnPGraph* tnpGraph_2016 = new TnPPlot::TnPGraph( fileName_2016, kFALSE, effType_2016, var );
    tnpGraph_2016->SetLegendInfo("Run2016 G-H (Mu50 || TkMu50)");
    tnpGraph_2016->Adjust_AbnormalErrors();

    TnPPlot::TnPGraph* tnpGraph_2017 = new TnPPlot::TnPGraph( fileName_2017, kFALSE, effType_, var );
    tnpGraph_2017->SetLegendInfo("Run2017 B-F (Mu50)");
    tnpGraph_2017->Adjust_AbnormalErrors();

    TnPPlot::TnPGraph* tnpGraph_2018 = new TnPPlot::TnPGraph( fileName_2018, kFALSE, effType_, var );
    tnpGraph_2018->SetLegendInfo("Run2018 A-C (Mu50, after Muon HLT reco. update)");
    tnpGraph_2018->Adjust_AbnormalErrors();


    TString canvasName = TString::Format("c_%s_%s", effType_.Data(), var.Data());
    if( isZoomInPlot ) canvasName = canvasName + "_ZoomIn";

    PlotTool::GraphCanvaswRatio *canvasRatio = new PlotTool::GraphCanvaswRatio(canvasName, 0, 0);
    canvasRatio->Register(tnpGraph_2016->g_eff_, tnpGraph_2016->legendInfo_, kBlack);
    canvasRatio->Register(tnpGraph_2017->g_eff_, tnpGraph_2017->legendInfo_, kGreen+2);
    canvasRatio->Register(tnpGraph_2018->g_eff_, tnpGraph_2018->legendInfo_, kBlue);

    TString titleX = "";
    if( var == "pt" )  titleX = "P_{T}(#mu) [GeV]";
    if( var == "eta" ) titleX = "#eta(#mu)";
    if( var == "phi" ) titleX = "#phi(#mu)";
    if( var == "vtx" ) titleX = "# vtx";

    TString titleY = "Efficiency";
    canvasRatio->SetTitle( titleX, titleY, "2017(18)/2016");
    canvasRatio->SetLegendPosition( 0.25, 0.32, 0.97, 0.50 );

    canvasRatio->SetRangeY( 0.6, 1.1 );
    canvasRatio->SetRangeRatio( 0.85, 1.15 );

    Double_t ptMin = tnpGraph_2016->ptMin_;
    if( var == "pt" )
    {
      canvasRatio->SetRangeX( 0, 500 );
      canvasRatio->SetRangeY( 0, 1.25 );
      if( isZoomInPlot )
      {
        canvasRatio->SetRangeX( ptMin, 500 ); 
        canvasRatio->SetRangeY( 0.6, 1.1 );
      }
    }

    if( var == "vtx" )
      canvasRatio->SetRangeX( 0.5, 50.5 );


    canvasRatio->Latex_CMSPre();
    canvasRatio->RegisterLatex( 0.72, 0.96, "#font[42]{#scale[0.7]{2016-18, 13 TeV}}");

    TString effInfo = tnpGraph_2017->effInfo_;
    canvasRatio->RegisterLatex( 0.16, 0.91, "#font[42]{#scale[0.6]{"+effInfo+"}}");

    if( var != "pt" )
    {
      TString ptInfo = TString::Format("p_{T} > %.0lf GeV", ptMin + 2.0);
      canvasRatio->RegisterLatex( 0.16, 0.865, "#font[42]{#scale[0.6]{"+ptInfo+"}}");
    }

    canvasRatio->Draw();
  }

};

void TnPEffPlots()
{
  TString effType = "Mu50_from_HighPt_and_RelTrkIso_010";
  vector<TString> vec_var = {"pt", "eta"};
  TnPPlotProducer* producer = new TnPPlotProducer(effType, vec_var);
  producer->Produce();
}