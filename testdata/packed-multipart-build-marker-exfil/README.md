Multipart upload and mutation-marker controls
============================================

The retired `packed-multipart-file-exfil-with-build-marker` rule inferred
theft from generic libcurl multipart strings and a mutation marker.
Reverse engineering Rifaien showed that it mutates and uploads its own
executable; neither packing nor an appended PE establishes exfiltration.

Run `python3 testdata/packed-multipart-build-marker-exfil/verify.py
<scratch-directory>`. All four controls must avoid the retired conviction,
including the complete former positive.
