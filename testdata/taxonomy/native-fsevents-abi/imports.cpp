namespace node { void MakeCallback(); }
extern "C" void* FSEventStreamCreate(void*, void*, void*, void*, unsigned long long, double, unsigned int);
extern "C" void* exercise() { node::MakeCallback(); return FSEventStreamCreate(0,0,0,0,0,0.1,0); }
