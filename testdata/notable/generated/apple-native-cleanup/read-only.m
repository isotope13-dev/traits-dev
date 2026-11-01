#import <Foundation/Foundation.h>
#include <unistd.h>
void diagnostics(void) {
    NSString *path = @"/private/var/log/com.apple.xpc.launchd/launchd.log";
    NSLog(@"%@", [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:nil]);
    unlink("/tmp/ordinary-app-cache");
}
