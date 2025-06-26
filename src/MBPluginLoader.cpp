#include <pyfbsdk/pyfbsdk.h>

bool Load(const char *pPath)
{
    bool lLoadSuccess = FBSystem::LibraryLoad(pPath);

    if (lLoadSuccess)
        return true;
    else
        return false;
}

BOOST_PYTHON_MODULE(mbpluginload)
{
    using namespace boost::python;
    def("load", &Load, "Load a MotionBuilder plugin from a specified path.");
}

FBLibraryDeclare(mbpluginload) {}
FBLibraryDeclareEnd;

bool FBLibrary::LibInit() { return true; }
bool FBLibrary::LibOpen() { return true; }
bool FBLibrary::LibReady() { return true; }
bool FBLibrary::LibClose() { return true; }
bool FBLibrary::LibRelease() { return true; }