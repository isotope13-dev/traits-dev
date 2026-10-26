package controls

import "google.golang.org/grpc/credentials/insecure"

var fallback = insecure.NewCredentials()
