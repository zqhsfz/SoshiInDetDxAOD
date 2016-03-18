CXX=g++
WD=${PWD}

CFLAGS=-fPIC -Wall `root-config --cflags`
LDFLAGS=-shared `root-config --glibs` `root-config --ldflags`

libBichselSimTool.so: BichselSimTool.o BichselSimToolDict.o
	${CXX} -o $@ ${LDFLAGS} $^

BichselSimTool.o: BichselSimTool.cxx
	${CXX} -o $@ -c ${CFLAGS} $^

BichselSimToolDict.o: BichselSimToolDict.cxx
	${CXX} -o $@ -c ${CFLAGS} $^

BichselSimToolDict.cxx: BichselSimTool.h LinkDef.h
	rootcint -f $@ -c ${CFLGAS} -p $^

clean:
	rm libBichselSimTool.so BichselSimTool.o BichselSimToolDict.o BichselSimToolDict.cxx BichselSimToolDict_rdict.pcm

# SRCDIR=${WD}/src
# INCLUDEDIR=${WD}/include

# lib/libDeadTimeStudy.so: obj/ComponentBase.o obj/SimpleDeadTime.o obj/ComplexDeadTime.o obj/Buffer.o obj/Trigger.o obj/TimeLine.o obj/DeadTimeStudyDict.o obj/TimeLineToolBase.o obj/TimeLineTool.o
#         ${CXX} -o $@ ${LDFLAGS} $^

# obj/ComponentBase.o: ${SRCDIR}/ComponentBase.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    
# obj/SimpleDeadTime.o: ${SRCDIR}/SimpleDeadTime.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    
# obj/ComplexDeadTime.o: ${SRCDIR}/ComplexDeadTime.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    
# obj/Buffer.o: ${SRCDIR}/Buffer.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    
# obj/Trigger.o: ${SRCDIR}/Trigger.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    
# obj/TimeLine.o: ${SRCDIR}/TimeLine.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^    

# obj/TimeLineToolBase.o: ${SRCDIR}/TimeLineToolBase.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^
# obj/TimeLineTool.o: ${SRCDIR}/TimeLineTool.cxx
#         ${CXX} -o $@ -c ${CFLAGS} $^

# obj/DeadTimeStudyDict.o: lib/DeadTimeStudyDict.cxx
#         ${CXX} -o $@ -c ${CFLAGS} -I${PWD} $^
# lib/DeadTimeStudyDict.cxx: ${INCLUDEDIR}/ComponentBase.h ${INCLUDEDIR}/SimpleDeadTime.h ${INCLUDEDIR}/ComplexDeadTime.h ${INCLUDEDIR}/Buffer.h ${INCLUDEDIR}/Trigger.h ${INCLUDEDIR}/TimeLine.h ${INCLUDEDIR}/TimeLineToolBase.h ${INCLUDEDIR}/TimeLineTool.h ${SRCDIR}/LinkDef.h
#         rootcint -f $@ -c ${CFLAGS} -p $^

