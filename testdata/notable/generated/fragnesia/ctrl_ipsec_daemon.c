#include <linux/if_alg.h>
#include <linux/netlink.h>
#include <linux/xfrm.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <unistd.h>

#ifndef TCP_ULP
#define TCP_ULP 31
#endif
#ifndef TCP_ENCAP_ESPINTCP
#define TCP_ENCAP_ESPINTCP 7
#endif

void configure_ipsec_sa(int sock) {
    struct sockaddr_alg sa = { .salg_family = AF_ALG, .salg_type = "skcipher", .salg_name = "ecb(aes)" };
    int alg = socket(AF_ALG, SOCK_SEQPACKET, 0);
    bind(alg, (struct sockaddr *)&sa, sizeof(sa));
    int xfd = socket(AF_NETLINK, SOCK_RAW, NETLINK_XFRM);
    struct xfrm_usersa_info xs = {0};
    struct xfrm_encap_tmpl enc = { .encap_type = TCP_ENCAP_ESPINTCP };
    int msg = XFRM_MSG_NEWSA;
    (void)xfd; (void)xs; (void)enc; (void)msg;
    setsockopt(sock, IPPROTO_TCP, TCP_ULP, "espintcp", 8);
}
