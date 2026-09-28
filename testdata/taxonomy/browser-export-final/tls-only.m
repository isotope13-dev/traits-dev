#import <Foundation/Foundation.h>
@interface SessionProbe : NSObject
@end
@implementation SessionProbe
@end
void report_status(void) {
  SSL_write(connection, "status", 6);
}
