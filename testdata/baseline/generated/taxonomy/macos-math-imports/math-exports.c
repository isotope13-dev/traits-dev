/* Benign exported names: no imported math APIs. */
double cos(double x) { return x; }
double sin(double x) { return x; }
double tan(double x) { return x; }
double exp(double x) { return x; }
double log1p(double x) { return x; }
double pow(double x, double y) { return x+y; }
double hypot(double x, double y) { return x+y; }
double fmod(double x, double y) { return x+y; }
