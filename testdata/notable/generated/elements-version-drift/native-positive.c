#include <unistd.h>
void native_api(int sock, void *address, int length, void *transaction) {
    bind(sock, (struct sockaddr *)address, length);
    CommitTransaction(transaction);
    GetFileSize(file, 0);
    remove("/tmp/cache");
}
const char *wallet = "Coinbase Wallet";
const char *attack = "meet-in-the-middle attack";
const char *korean = "안녕하세요 안녕하세요";
