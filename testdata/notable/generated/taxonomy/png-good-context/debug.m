#import <Foundation/Foundation.h>
#if defined(DEBUG) || defined(NI_DEBUG)
int attached(int flags) { return (flags & P_TRACED) != 0; }
#endif
