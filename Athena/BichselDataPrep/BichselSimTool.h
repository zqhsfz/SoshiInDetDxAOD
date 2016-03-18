///////////////////////////////////////////////////////////////////
// BichselSimTool.h
//   Header file for class BichselSimTool
///////////////////////////////////////////////////////////////////
// (c) ATLAS Detector software
// Author: Qi Zeng
// 2015-02-14 (Happy Valentines Day!)
// Description:
//   A general tool to implement Bichsel simultion.
//   Bichsel model can be used to simulate how a single particle deposits energy inside silicon material
//   Instead of a Landau distribution, the simulation is done on collision-by-collision level (i.e. single collision between particle and atom)
//   This model can better describe how deposited charges distribute along incident path
///////////////////////////////////////////////////////////////////


#ifndef PIXELDIGITIZATION_BichselSimTool_H
#define PIXELDIGITIZATION_BichselSimTool_H

#include "TH1D.h"
#include "TFile.h"
#include "TTree.h"

#include <iostream>
#include <vector>

using namespace std;

// forward class declaration
class TRandom3;

// internal data structure for storage purpose
struct BichselData
{
  std::vector<double> Array_BetaGammaLog10;
  std::vector<std::vector<double> > Array_BetaGammaLog10_ColELog10;  // ColE = CollisionEnergy in eV
  std::vector<std::vector<double> > Array_BetaGammaLog10_IntXLog10;  // IntX = Integrated Xsection. The unit doesn't matter
  std::vector<double> Array_BetaGammaLog10_UpperBoundIntXLog10;      // upper bound of log10(IntX)
};

class BichselSimTool{

public:
  
  // Constructor:
  BichselSimTool();
  virtual ~BichselSimTool();

  bool initialize();
  bool finalize();
  
  // public methods accessed by user //
  std::pair<int,int> FastSearch(std::vector<double> vec, double item) const;               // A quick implementation of binary search in 2D table
  bool Scan(int ParticleType, int index_BetaGammaLog10, int nCols, int SampleSize) const;
  // std::vector<std::pair<double,double> > BichselSim(double BetaGamma, int ParticleType, double TotalLength, double InciEnergy) const;   // output hit record in the format (hit position, energy loss)
  // std::vector<std::pair<double,double> > ClusterHits(std::vector<std::pair<double,double> >& rawHitRecord, int n_pieces) const;         // cluster hits into n steps (there could be thousands of hit)
  int trfPDG(int pdgId) const;                                                             // convert pdgId to ParticleType. If it is unsupported particle, -1 is returned.

  std::vector<BichselData> m_BichselData;      // vector to store Bichsel Data. Each entry is for one particle type
private:
  // internal private members //
  double                   m_DeltaRayCut;      // Threshold to identify a delta ray. unit in keV
  TRandom3*                m_RandomGenerator;  // Random number generator

  // internal private functions //
  double GetColE(double BetaGammaLog10, double IntXLog10, BichselData& iData) const;       // return ColE NOT ColELog10 ! unit is eV
  double GetUpperBound(double BetaGammaLog10, BichselData& iData) const;                   // return IntX upper bound
  void SetFailureFlag(std::vector<std::pair<double,double> >& rawHitRecord) const;         // return (-1,-1) which indicates failure in running BichselSim
 };


#endif //PIXELDIGITIZATION_BichselSimTool_H
