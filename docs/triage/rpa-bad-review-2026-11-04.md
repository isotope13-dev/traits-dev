# Ren’Py archive mislabeled-bad review — 2026-11-04

The only sample, `dc1a973a602c`, is bad. Static inspection of its archived game script shows a sandbox check, XOR-decoding and extraction of a hidden payload, clearing of the Windows zone marker, and concealed launching. It also obtains the public IP address and sends it with tracking fields to a remote endpoint. The external payload itself was not present in the standalone archive, so its behavior and successful delivery are not established.

Both scanners already flag the renamed decoded payload and the zone-cleared `forfiles` execution pattern in the archive. Hopper confirmed bad; no additional taxonomy change was necessary.
