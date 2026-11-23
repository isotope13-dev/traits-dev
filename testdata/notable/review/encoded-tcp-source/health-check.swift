import Foundation
let probe = "YmFzaCAtYyAnZWNobyBoZWFsdGggPi9kZXYvdGNwL3NlcnZpY2UuaW50ZXJuYWwvNDQ0NCc="
let data = Data(base64Encoded: probe)
print(data as Any)
