#ifndef __REDIR_SOCKS_H__
#define __REDIR_SOCKS_H__

class CRedirectSOCKS;

class CRedirectSOCKS : public CRedirectBase
{
public:
	CRedirectSOCKS();
	virtual void StartRedirect();
};

#endif // __REDIR_SOCKS_H__
