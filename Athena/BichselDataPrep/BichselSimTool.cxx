///////////////////////////////////////////////////////////////////
// BichselSimTool.cxx
//   Implementation file for class BichselSimTool
///////////////////////////////////////////////////////////////////
// (c) ATLAS Detector software
// Details in head file
///////////////////////////////////////////////////////////////////

#include "BichselSimTool.h"

#include "TGraph.h"
#include "TString.h"
#include "TMath.h"
#include "TRandom3.h"

#include <sstream>
#include <fstream>

using namespace std;

// Constructor with parameters:
BichselSimTool::BichselSimTool()
{ 
  m_DeltaRayCut = 117.;
}

// Destructor:
BichselSimTool::~BichselSimTool()
{
}

//----------------------------------------------------------------------
// Initialize
//----------------------------------------------------------------------
bool BichselSimTool::initialize() {
  //** define your initialize below **//

  // random seed
  m_RandomGenerator = new TRandom3(0);

  // clear data table
  m_BichselData.clear();

  // load data table
  std::cout << "Loading data file" << std::endl;

  bool sc = true;
  int n_ParticleType = 6;
  for(int iParticleType = 1; iParticleType <= n_ParticleType; iParticleType++){
    // configure file name
    std::ifstream inputFile;
    TString inputFileName = "Bichsel_";
    std::stringstream ss; ss << iParticleType; std::string sParticleType = ss.str();
    inputFileName = (inputFileName + sParticleType.data() + ".dat");

    std::string FullFileName = inputFileName.Data();
    inputFile.open(FullFileName.data());

    std::cout << "Loading file name : " << inputFileName.Data() << std::endl;
    std::cout << "-- File full name: " << FullFileName.data() << std::endl;
    std::cout << "-- Is file open ? " << inputFile.is_open() << std::endl;

    if(!inputFile.is_open()){
      std::cout << "Fail to load file " << inputFileName.Data() << " !" << std::endl;
      sc = false;
      break;
    }

    // prepare data
    BichselData iData;
    
    double BetaGammaLog10 = 0; inputFile >> BetaGammaLog10;
    double ColELog10 = 0;      inputFile >> ColELog10;
    double IntXLog10 = 0;      inputFile >> IntXLog10;

    std::cout << "-- File eof check : " << inputFile.eof() << std::endl;

    while(!inputFile.eof()){
      // check if this BetaGamma has already been stored
      if( (iData.Array_BetaGammaLog10.size() == 0) || (iData.Array_BetaGammaLog10.back() != BetaGammaLog10) ){ // a new BetaGamma

        if(iData.Array_BetaGammaLog10.size() != 0){
          iData.Array_BetaGammaLog10_UpperBoundIntXLog10.push_back(iData.Array_BetaGammaLog10_IntXLog10.back().back());
        }

        iData.Array_BetaGammaLog10.push_back(BetaGammaLog10);
        std::vector<double> new_ColELog10;  iData.Array_BetaGammaLog10_ColELog10.push_back(new_ColELog10);
        std::vector<double> new_IntXLog10;  iData.Array_BetaGammaLog10_IntXLog10.push_back(new_IntXLog10);
      }

      iData.Array_BetaGammaLog10_ColELog10.back().push_back(ColELog10);
      iData.Array_BetaGammaLog10_IntXLog10.back().push_back(IntXLog10);

      inputFile >> BetaGammaLog10;
      inputFile >> ColELog10;
      inputFile >> IntXLog10;
    }
    iData.Array_BetaGammaLog10_UpperBoundIntXLog10.push_back(iData.Array_BetaGammaLog10_IntXLog10.back().back());

    std::cout << "-- Array_BetaGammaLog10 size : " << iData.Array_BetaGammaLog10.size() << std::endl;
    std::cout << "-- Array_BetaGammaLog10_ColELog10 size at 0 : " << iData.Array_BetaGammaLog10_ColELog10[0].size() << std::endl;
    std::cout << "-- Array_BetaGammaLog10_IntXLog10 size at 0 : " << iData.Array_BetaGammaLog10_IntXLog10[0].size() << std::endl;
    std::cout << "-- Array_BetaGammaLog10_UpperBoundIntXLog10 : " << iData.Array_BetaGammaLog10_UpperBoundIntXLog10.size() << std::endl;

    m_BichselData.push_back(iData);
    inputFile.close();

    std::cout << "-- Finish loading file " << inputFileName.Data() << std::endl;
  }

  std::cout << "Finish Loading Data File" << std::endl;

  return sc; 
}

//----------------------------------------------------------------------
// finalize
//----------------------------------------------------------------------
bool BichselSimTool::finalize() {
  return true;
}

//------------------------------------------------------------
// Scan through BetaGamma and ParticleType
//------------------------------------------------------------



bool BichselSimTool::Scan(int ParticleType, int index_BetaGammaLog10, int nCols, int SampleSize) const{
  // prepare output
  TString NameAppendix = TString::Format("_%d_%d", ParticleType, index_BetaGammaLog10);
  TFile* m_storage = new TFile("Bichsel"+NameAppendix+".root", "RECREATE");
  TTree* m_tree = new TTree("tree", "tree");
  double m_ColELog10; m_tree->Branch("ColELog10", &m_ColELog10, "ColELog10/D");
  double m_Boundary;  m_tree->Branch("Boundary", &m_Boundary, "Boundary/D");

  // load relevant data
  BichselData iData = m_BichselData[ParticleType-1];

  // upper bound
  double IntXUpperBound = TMath::Power(10., iData.Array_BetaGammaLog10_UpperBoundIntXLog10[index_BetaGammaLog10]);

  // mean-free path
  double lambda = (1./IntXUpperBound) * 1.E4;   // unit of IntX is cm-1. It needs to be converted to micrometer-1

  if(IntXUpperBound <= 0.){
    std::cout << "ERROR! Why you get negative IntXUpperBound ?!" << std::endl;
    return false;
  }

  for(unsigned int iEvt = 0; iEvt < SampleSize; iEvt++){

    double SumEnergyLoss = 0.;
    double SumPathLength = 0.;
    for(unsigned int iCol = 0; iCol < nCols; iCol++){

      double TossEnergyLoss = 0.;
      while(TossEnergyLoss <= 0){
        // sample energy deposition for one collision
        double TossIntX = m_RandomGenerator->Uniform(0., IntXUpperBound);
        double TossIntXLog10 = TMath::Log10(TossIntX);

        // find appropriate bin
        std::pair<int,int> indices_IntXLog10 = FastSearch(iData.Array_BetaGammaLog10_IntXLog10[index_BetaGammaLog10], TossIntXLog10);
        if( (indices_IntXLog10.first==-1) && (indices_IntXLog10.second==-1) ){
          // std::cout << "Unable to find the bin for TossIntXLog10: " << TossIntXLog10 << std::endl;
          continue;
        }

        // interpolation
        double y1 = iData.Array_BetaGammaLog10_IntXLog10[index_BetaGammaLog10][indices_IntXLog10.first];
        double y2 = iData.Array_BetaGammaLog10_IntXLog10[index_BetaGammaLog10][indices_IntXLog10.second];
        double Est = ((y2 - TossIntXLog10)*iData.Array_BetaGammaLog10_ColELog10[index_BetaGammaLog10][indices_IntXLog10.first] + (TossIntXLog10 - y1)*iData.Array_BetaGammaLog10_ColELog10[index_BetaGammaLog10][indices_IntXLog10.second])/(y2-y1);

        TossEnergyLoss = TMath::Power(10., Est);
      }

      SumEnergyLoss += TossEnergyLoss;
      SumPathLength += m_RandomGenerator->Exp(lambda);
    }

    m_ColELog10 = TMath::Log10(SumEnergyLoss);
    m_Boundary = SumPathLength;
    m_tree->Fill();
  }

  m_storage->Write();
  m_storage->Close();

  // might be some memory leak here ...

  return true;
}

//-----------------------------------------------------------
// Implementation below
//-----------------------------------------------------------

/////////////////////////////////////////////
// Main Public Functions Accessed by Users //
/////////////////////////////////////////////

// input total length should be in the unit of micrometer
// InciEnergy should be in MeV
// In case there is any abnormal in runtime, (-1,-1) will be returned indicating old deposition model should be used instead
// std::vector<std::pair<double,double> > BichselSimTool::BichselSim(double BetaGamma, int ParticleType, double TotalLength, double InciEnergy) const{
//   ATH_MSG_DEBUG("Begin BichselSimTool::BichselSim");

//   // prepare hit record (output)
//   std::vector<std::pair<double,double> > rawHitRecord;
//   double TotalEnergyLoss = 0.;
//   double accumLength = 0.;

//   // load relevant data
//   BichselData iData = m_BichselData[ParticleType-1];
//   double BetaGammaLog10 = TMath::Log10(BetaGamma);

//   // upper bound
//   double IntXUpperBound = GetUpperBound(BetaGammaLog10, iData);
//   if(IntXUpperBound <= 0.){
//     ATH_MSG_WARNING("Negative IntXUpperBound in BichselSimTool::BichselSim! (-1,-1) will be returned");
//     // if(IntXUpperBound == -1.){
//     //   std::cout << "Cannot find beta-gamma(log10) " << BetaGammaLog10 << " in data table!" << std::endl;
//     // }
//     SetFailureFlag(rawHitRecord);
//     return rawHitRecord;
//   }
  
//   // mean-free path
//   double lambda = (1./IntXUpperBound) * 1.E4;   // unit of IntX is cm-1. It needs to be converted to micrometer-1

//   // begin simulation
//   int count = 0;
//   while(true){
//     // infinite loop protection
//     if(count >= 100000){
//       ATH_MSG_WARNING("Potential infinite loop in BichselSim. Exit Loop. A special flag will be returned (-1,-1). The total length is " << TotalLength);
//       SetFailureFlag(rawHitRecord);
//       break;
//     }

//     // sample hit position -- exponential distribution
//     // double HitPosition = m_RandomGenerator->Exp(lambda);

//     double HitPosition = lambda;
//     if(TotalLength < 100.) HitPosition = m_RandomGenerator->Exp(lambda);  // touch

//     // termination by hit position
//     if(accumLength + HitPosition >= TotalLength)
//       break;

//     // sample single collision
//     double TossEnergyLoss = -1.;
//     double TossIntX_record;
//     while(TossEnergyLoss <= 0.){ // we have to do this because sometimes TossEnergyLoss will be negative due to too small TossIntX
//       double TossIntX = m_RandomGenerator->Uniform(0., IntXUpperBound);
//       TossEnergyLoss = GetColE(BetaGammaLog10, TMath::Log10(TossIntX), iData);

//       TossIntX_record = TossIntX;
//     }

//     // check if it is delta-ray -- delta-ray is already taken care of by G4 and treated as an independent hit. Unfortunately, we won't deal with delta-ray using Bichsel's model
//     if(TossEnergyLoss > (m_DeltaRayCut*1000.)){
//       // ATH_MSG_WARNING("!!! Energy deposition beyond delta-ray cut !!!");
//       // std::cout << "+++++++ " << TossEnergyLoss/1000. << " keV " << "+++++++++++" << std::endl; 
//       // std::cout << "+++++++ " << ParticleType << std::endl;
//       // std::cout << "+++++++ " << BetaGammaLog10 << std::endl;
//       // std::cout << "+++++++ " << TMath::Log10(TossIntX_record) << std::endl;
//       TossEnergyLoss = 0.;
//     }

//     bool fLastStep = false;

//     // in case energy loss so far is larger than incident energy -- basically not possible ...
//     // This becomes important after taking delta-ray into account!
//     if( ((TotalEnergyLoss + TossEnergyLoss)/1.E+6) > InciEnergy ){
//       ATH_MSG_WARNING("Energy loss is larger than incident energy in BichselSimTool::BichselSim! This is usually delta-ray.");
//       // then this is the last step
//       TossEnergyLoss = InciEnergy*1.E+6 - TotalEnergyLoss;
//       fLastStep = true;
//     }

//     // update
//     accumLength += HitPosition;
//     TotalEnergyLoss += TossEnergyLoss;

//     // record this hit
//     std::pair<double,double> oneHit;
//     oneHit.first = accumLength; oneHit.second = TossEnergyLoss;
//     rawHitRecord.push_back(oneHit);

//     count++;

//     if(fLastStep)
//       break;
//   }

//   ATH_MSG_DEBUG("Finish BichselSimTool::BichselSim");

//   return rawHitRecord;
// }

// std::vector<std::pair<double,double> > BichselSimTool::ClusterHits(std::vector<std::pair<double,double> >& rawHitRecord, int n_pieces) const{
//   ATH_MSG_DEBUG("Begin BichselSimTool::ClusterHits");
//   std::vector<std::pair<double,double> > trfHitRecord;

//   if((int)(rawHitRecord.size()) < n_pieces){ // each single collision is the most fundamental unit
//     n_pieces = rawHitRecord.size();
//   }

//   int unitlength = int(1.0*rawHitRecord.size()/n_pieces);
//   int index_start = 0;
//   int index_end = unitlength-1;   // [index_start, index_end] are included
//   while(true){
//     // calculate weighted center of each slice
//     double position = 0.;
//     double energyloss = 0.;

//     for(int index = index_start; index <= index_end; index++){
//       position += (rawHitRecord[index].first * rawHitRecord[index].second);
//       energyloss += rawHitRecord[index].second;
//     }
//     position = (energyloss == 0. ? 0. : position/energyloss);

//     // store
//     std::pair<double,double> oneHit;
//     oneHit.first = position; oneHit.second = energyloss;
//     trfHitRecord.push_back(oneHit);

//     // procede to next slice
//     index_start = index_end + 1;
//     index_end = index_start + unitlength - 1;

//     if(index_start > (int)(rawHitRecord.size()-1)){
//       break;
//     }

//     if(index_end > (int)(rawHitRecord.size()-1)){
//       index_end = rawHitRecord.size()-1;
//     }
//   }

//   ATH_MSG_DEBUG("Finsih BichselSimTool::ClusterHits");

//   return trfHitRecord;
// }


///////////
// Utils //
///////////

int BichselSimTool::trfPDG(int pdgId) const{
  if(std::fabs(pdgId) == 2212) return 1;   // proton
  if(std::fabs(pdgId) == 211)  return 2;   // pion
  // alpha is skipped -- 3
  if(std::fabs(pdgId) == 11)   return 4;   // electron
  if(std::fabs(pdgId) == 321)  return 5;   // kaon
  if(std::fabs(pdgId) == 13)   return 6;   // muon

  return -1;   // unsupported particle
}

// assume vec is already sorted from small to large
std::pair<int,int> BichselSimTool::FastSearch(std::vector<double> vec, double item) const{
  std::pair<int,int> output;

  int index_low = 0;
  int index_up = vec.size()-1;

  if((item < vec[index_low]) || (item > vec[index_up])){
    output.first = -1; output.second = -1;
    return output;
  }
  else if(item == vec[index_low]){
    output.first = index_low; output.second = index_low;
    return output;
  }
  else if(item == vec[index_up]){
    output.first = index_up; output.second = index_up;
    return output;
  }

  while( (index_up - index_low) != 1 ){
    int index_middle = int(1.0*(index_up + index_low)/2.);
    if(item < vec[index_middle])
      index_up = index_middle;
    else if(item > vec[index_middle])
      index_low = index_middle;
    else{ // accurate hit. Though this is nearly impossible ...
      output.first = index_middle; output.second = index_middle;
      return output;
    }
  }

  output.first = index_low; output.second = index_up;
  return output;
}

// make sure IntXLog10 is less than the value given by GetUpperBound()
// Please refer to below which can give more realistive result
// But don't delete this fraction. Keep it for record
// double BichselSimTool::GetColE(double BetaGammaLog10, double IntXLog10, BichselData& iData) const{
//   std::pair<int,int> indices_BetaGammaLog10;
//   if(BetaGammaLog10 > iData.Array_BetaGammaLog10.back()){ // last one is used because when beta-gamma is very large, energy deposition behavior is very similar
//     indices_BetaGammaLog10.first = iData.Array_BetaGammaLog10.size()-1;
//     indices_BetaGammaLog10.second = iData.Array_BetaGammaLog10.size()-1;
//   }
//   else{
//     indices_BetaGammaLog10 = FastSearch(iData.Array_BetaGammaLog10, BetaGammaLog10);
//   }

//   if( (indices_BetaGammaLog10.first==-1) && (indices_BetaGammaLog10.second==-1) )
//     return -1.;
//   double BetaGammaLog10_1 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.first];
//   double BetaGammaLog10_2 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.second];

//   // BetaGammaLog10_1 first
//   std::pair<int,int> indices_IntXLog10_x1 = FastSearch(iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first], IntXLog10);
//   if( (indices_IntXLog10_x1.first==-1) && (indices_IntXLog10_x1.second==-1) )
//     return -1.;
//   double y11 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.first];
//   double y12 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.second];
//   double Est_x1 = ((y12 - IntXLog10)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.first] + (IntXLog10 - y11)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.second])/(y12-y11);

//   // BetaGammaLog10_2 then
//   std::pair<int,int> indices_IntXLog10_x2 = FastSearch(iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second], IntXLog10);
//   if( (indices_IntXLog10_x2.first==-1) && (indices_IntXLog10_x2.second==-1) )
//     return -1;
//   double y21 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.first];
//   double y22 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.second];
//   double Est_x2 = ((y22 - IntXLog10)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.first] + (IntXLog10 - y21)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.second])/(y22-y21);

//   // final estimation
//   double Est = ((BetaGammaLog10_2 - BetaGammaLog10)*Est_x1 + (BetaGammaLog10 - BetaGammaLog10_1)*Est_x2)/(BetaGammaLog10_2 - BetaGammaLog10_1);

//   return TMath::Power(10., Est);
// }

// another way to do interpolation -- Fix beta-gamma
// IMPORTANT!! Use this one. don't use the upper one.
// This one will give correct dEdx curve
double BichselSimTool::GetColE(double BetaGammaLog10, double IntXLog10, BichselData& iData) const{
  std::pair<int,int> indices_BetaGammaLog10;
  if(BetaGammaLog10 > iData.Array_BetaGammaLog10.back()){ // last one is used because when beta-gamma is very large, energy deposition behavior is very similar
    indices_BetaGammaLog10.first = iData.Array_BetaGammaLog10.size()-1;
    indices_BetaGammaLog10.second = iData.Array_BetaGammaLog10.size()-1;
  }
  else{
    indices_BetaGammaLog10 = FastSearch(iData.Array_BetaGammaLog10, BetaGammaLog10);
  }

  if( (indices_BetaGammaLog10.first==-1) && (indices_BetaGammaLog10.second==-1) )
    return -1.;
  //double BetaGammaLog10_1 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.first];
  //double BetaGammaLog10_2 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.second];

  // BetaGammaLog10_1 first
  // std::pair<int,int> indices_IntXLog10_x1 = FastSearch(iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first], IntXLog10);
  // if( (indices_IntXLog10_x1.first==-1) && (indices_IntXLog10_x1.second==-1) )
  //   return -1.;
  // double y11 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.first];
  // double y12 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.second];
  // double Est_x1 = ((y12 - IntXLog10)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.first] + (IntXLog10 - y11)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.first][indices_IntXLog10_x1.second])/(y12-y11);

  // BetaGammaLog10_2 then
  std::pair<int,int> indices_IntXLog10_x2 = FastSearch(iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second], IntXLog10);
  if( (indices_IntXLog10_x2.first==-1) && (indices_IntXLog10_x2.second==-1) )
    return -1;
  double y21 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.first];
  double y22 = iData.Array_BetaGammaLog10_IntXLog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.second];
  double Est_x2 = ((y22 - IntXLog10)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.first] + (IntXLog10 - y21)*iData.Array_BetaGammaLog10_ColELog10[indices_BetaGammaLog10.second][indices_IntXLog10_x2.second])/(y22-y21);

  // final estimation
  //double Est = ((BetaGammaLog10_2 - BetaGammaLog10)*Est_x1 + (BetaGammaLog10 - BetaGammaLog10_1)*Est_x2)/(BetaGammaLog10_2 - BetaGammaLog10_1);
  double Est = Est_x2;

  return TMath::Power(10., Est);
}

// IMPORTANT!! For this one, one should use interpolation, instead of fixed beta-gamma.
// Otherwise, dE/dx shape will get distorted again.
double BichselSimTool::GetUpperBound(double BetaGammaLog10, BichselData& iData) const{
  std::pair<int,int> indices_BetaGammaLog10;
  if(BetaGammaLog10 > iData.Array_BetaGammaLog10.back()){
    indices_BetaGammaLog10.first = iData.Array_BetaGammaLog10.size()-1;
    indices_BetaGammaLog10.second = iData.Array_BetaGammaLog10.size()-1;
  }
  else{
    indices_BetaGammaLog10 = FastSearch(iData.Array_BetaGammaLog10, BetaGammaLog10);
  }

  if( (indices_BetaGammaLog10.first==-1) && (indices_BetaGammaLog10.second==-1) ){
    // std::cout << "++++++++++++++" << std::endl;
    // std::cout << BetaGammaLog10 << std::endl;
    // std::cout << iData.Array_BetaGammaLog10[0] << " , " << iData.Array_BetaGammaLog10.back() << std::endl;

    return -1.;
  }
  double BetaGammaLog10_1 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.first];
  double BetaGammaLog10_2 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.second];

  // obtain estimation
  double Est_1 = iData.Array_BetaGammaLog10_UpperBoundIntXLog10[indices_BetaGammaLog10.first];
  double Est_2 = iData.Array_BetaGammaLog10_UpperBoundIntXLog10[indices_BetaGammaLog10.second];

  // final estimation
  double Est = ((BetaGammaLog10_2 - BetaGammaLog10)*Est_1 + (BetaGammaLog10 - BetaGammaLog10_1)*Est_2)/(BetaGammaLog10_2 - BetaGammaLog10_1);

  return TMath::Power(10., Est);
}

// Keep for record
// double BichselSimTool::GetUpperBound(double BetaGammaLog10, BichselData& iData) const{
//   std::pair<int,int> indices_BetaGammaLog10;
//   if(BetaGammaLog10 > iData.Array_BetaGammaLog10.back()){
//     indices_BetaGammaLog10.first = iData.Array_BetaGammaLog10.size()-1;
//     indices_BetaGammaLog10.second = iData.Array_BetaGammaLog10.size()-1;
//   }
//   else{
//     indices_BetaGammaLog10 = FastSearch(iData.Array_BetaGammaLog10, BetaGammaLog10);
//   }

//   if( (indices_BetaGammaLog10.first==-1) && (indices_BetaGammaLog10.second==-1) )
//     return -1.;
//   double BetaGammaLog10_1 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.first];
//   double BetaGammaLog10_2 = iData.Array_BetaGammaLog10[indices_BetaGammaLog10.second];

//   // obtain estimation
//   double Est_1 = iData.Array_BetaGammaLog10_UpperBoundIntXLog10[indices_BetaGammaLog10.first];
//   double Est_2 = iData.Array_BetaGammaLog10_UpperBoundIntXLog10[indices_BetaGammaLog10.second];

//   // final estimation
//   //double Est = ((BetaGammaLog10_2 - BetaGammaLog10)*Est_1 + (BetaGammaLog10 - BetaGammaLog10_1)*Est_2)/(BetaGammaLog10_2 - BetaGammaLog10_1);
//   double Est = Est_2;

//   return TMath::Power(10., Est);
// }

void BichselSimTool::SetFailureFlag(std::vector<std::pair<double,double> >& rawHitRecord) const{
  rawHitRecord.clear();
  std::pair<double, double> specialFlag;
  specialFlag.first = -1.; specialFlag.second = -1.;
  rawHitRecord.push_back(specialFlag);

  return;
}






