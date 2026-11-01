#import <Foundation/Foundation.h>
#import <CFNetwork/CFNetwork.h>
void configure(CFWriteStreamRef output, id gateway, id record) {
    NSDictionary *policy = @{(__bridge NSString *)kCFStreamSSLValidatesCertificateChain: @NO};
    CFWriteStreamSetProperty(output, kCFStreamPropertySSLSettings, (__bridge CFDictionaryRef)policy);
    [gateway deleteSafariWebsiteDataRecord:record completionHandler:nil];
}
