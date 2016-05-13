#include "TTrainedNetwork.h"
#include "TNetworkToHistoTool.h"
#include "TFile.h"
#include <vector>
#include <iostream>
#include "TString.h"
#include "TDirectory.h"
#include "TH1.h"

using namespace std;

void prepareClusteringCalibrationFile(TString outputFileName="NNCalibBichsel_NNTrained_20160501_JZ.root")
{
  TString NNWeightsDir = "../../NNWeights/NNTrained_20160501_JZ/";
  
  vector<TString> nameFiles;
  vector<TString> nameCalibrationDirectory;

  nameFiles.push_back(NNWeightsDir+"/TTrained_number.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_pos1.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_pos2.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_pos3.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error1x.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error2x.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error3x.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error1y.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error2y.v2.root");
  nameFiles.push_back(NNWeightsDir+"/TTrained_error3y.v2.root");
  
  nameCalibrationDirectory.push_back("NumberParticles");
  nameCalibrationDirectory.push_back("ImpactPoints1P");
  nameCalibrationDirectory.push_back("ImpactPoints2P");
  nameCalibrationDirectory.push_back("ImpactPoints3P");
  nameCalibrationDirectory.push_back("ImpactPointErrorsX1");
  nameCalibrationDirectory.push_back("ImpactPointErrorsX2");
  nameCalibrationDirectory.push_back("ImpactPointErrorsX3");
  nameCalibrationDirectory.push_back("ImpactPointErrorsY1");
  nameCalibrationDirectory.push_back("ImpactPointErrorsY2");
  nameCalibrationDirectory.push_back("ImpactPointErrorsY3");

  TFile* outputFile=new TFile(outputFileName,"recreate");

  TNetworkToHistoTool myHistoTool;

  for (int i=0;i<nameFiles.size();i++)
  {
    
    TFile* inputFile=new TFile(nameFiles[i]);
    TTrainedNetwork* trainedNetwork=(TTrainedNetwork*)inputFile->Get("TTrainedNetwork");
    
    vector<TH1*> histoVector=myHistoTool.fromTrainedNetworkToHisto(trainedNetwork);

    outputFile->cd("/");
    gDirectory->mkdir(nameCalibrationDirectory[i]);
    gDirectory->cd(nameCalibrationDirectory[i]);

    std::vector<TH1*>::const_iterator histoBegin=histoVector.begin();
    std::vector<TH1*>::const_iterator histoEnd=histoVector.end();

    for (std::vector<TH1*>::const_iterator histoIter=histoBegin;histoIter!=histoEnd;
         ++histoIter)
    {
      cout << " Iterator pointer: " << *histoIter << endl;
      if ((*histoIter)->GetName()!="TObject")
      {
        cout << "--> writing out  histogram: " << (*histoIter)->GetName() << endl;
        (*histoIter)->Write();
      }
    }
    
  }//end nameFiles
  
  outputFile->Write();

}
