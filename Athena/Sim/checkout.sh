# for updated geometry
pkgco.py PixelGeoModel-00-09-52-06

# to plug in the physics list suggested by Zach
pkgco.py G4PhysicsLists
currentPWDCache=${PWD}
cd Simulation/G4Utilities/G4PhysicsLists
patch -p0 -i $currentPWDCache/patches/G4PhysicsLists.patch
cd $currentPWDCache
