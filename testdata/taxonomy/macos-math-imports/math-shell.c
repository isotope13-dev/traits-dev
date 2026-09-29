/* Benign static analysis control. Never run by the regression check. */
extern double cos(double), sin(double), tan(double), exp(double), log1p(double);
extern double pow(double,double), hypot(double,double), fmod(double,double);
extern int system(const char *);
int main(int argc, char **argv) {
    (void)argv;
    volatile double x = argc + 0.25;
    volatile double y = cos(x) + sin(x) + tan(x) + exp(x) + log1p(x)
                      + pow(x,2) + hypot(x,2) + fmod(x,2);
    return y < 0 ? 1 : system("true");
}
