#define DISPATCH(T) apply(T)
void step(void) { DISPATCH(float); }
