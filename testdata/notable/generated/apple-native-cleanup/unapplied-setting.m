#import <Foundation/Foundation.h>
#import <CFNetwork/CFNetwork.h>
NSDictionary *unusedSettings(void) {
    return @{(__bridge NSString *)kCFStreamSSLValidatesCertificateChain: @NO};
}
void ordinaryStreamOption(CFReadStreamRef stream) {
    CFReadStreamSetProperty(stream, kCFStreamPropertyHTTPShouldAutoredirect, kCFBooleanTrue);
}
