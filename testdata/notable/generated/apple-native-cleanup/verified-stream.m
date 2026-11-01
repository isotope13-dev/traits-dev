#import <Foundation/Foundation.h>
#import <CFNetwork/CFNetwork.h>
void setup(CFReadStreamRef stream) {
    // kCFStreamSSLValidatesCertificateChain: @NO
    NSDictionary *settings = @{
        (__bridge NSString *)kCFStreamSSLValidatesCertificateChain: @YES
    };
    CFReadStreamSetProperty(stream, kCFStreamPropertySSLSettings,
                           (__bridge CFDictionaryRef)settings);
}
