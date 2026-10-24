ZDI-CAN-33367 exercises a concrete Linux page-cache corruption chain:
NFQUEUE full-packet copying retains file pages spliced into a socket buffer;
an nlmon tap and tc pedit/mirred turn its header into an ESP packet. The lost
shared-fragment marker lets ESP decrypt over those pages.

The recovered advisory appendix is preserved, with source-boundary comments,
in `testdata/hostile/nfqueue-esp/zerofrag-appendix.c`. Its own comments describe
some components as source reconstructions. It is static-review source, not an
original ELF or a buildable translation unit; missing headers and generated
includes were not invented. Forager provenance and separately extracted source
blocks remain in threat-feed scratch article 4240.

Sources:

- https://webflow.sysdig.com/blog/detecting-and-mitigating-zdi-can-33367-and-five-other-linux-flaws
- https://pwn.watch/i/linux-kernel-zdi-reports-leaked-to-lkml
- https://lore.kernel.org/lkml/BYAPR01MB3830CECF5D0871064C59BA0280662@BYAPR01MB3830.prod.exchangelabs.com/
- https://lore.kernel.org/netdev/CAL4WiiqsmV8yKzU_HnE5tFXHqf8rMabGP9_-4B6gAdGZwhzjOQ@mail.gmail.com/

Placement follows the supported observation: traffic-policy ABI references
belong to `micro-behaviors/network/qos`, the nlmon interface kind to
`network/interface`, XFRM state configuration commands to `network/tunnel`,
and namespace calls/arguments to `os/container/namespace`. Those facts are
notable capabilities or references. Their conjunction with Linux splice is
a suspicious netlink-tap/edit sequence. Adding user/network namespaces and
ESP state control identifies the hostile exploit chain, placed at
`objectives/privilege-escalation/exploit/kernel` (T1068/E1068). No new leaf,
directory budget, package identity, filename gate or endpoint gate is needed.

The existing ESP and namespace observations are reused. The broadened source
spelling support repairs real Go `unix.Unshare` and Rust `libc::unshare` /
`libc::splice` / `nix::fcntl::splice` spellings. Namespace consumers and ESP
consumers were audited; they still require their other independent legs.
Rust collection `Vec::splice` remains outside the Linux splice observation.

Run `python3 testdata/taxonomy/nfqueue-esp/check.py` to check C++/Go/Rust/Python
source excerpts, each missing role, AH rather than ESP, collection splice,
and the benign controls in `testdata/benign/nfqueue-esp`. The excerpts are
source-shape regression fixtures, not functional exploits. Different
interface names and IPv6 in the C++ excerpt ensure the arbitrary PoC name
and IPv4 loopback literal are not conviction gates. `make validate` also
checks the recovered C appendix and the benign controls via explicit trait
expectations. The report-source fixture requires one hostile and two
suspicious findings; these are the supported mechanisms, not an inflated
hostile quota.

The matchers establish same-file co-occurrence, not runtime order or verified
handle-level flow. Stripped ELF with numeric netlink fields is a coverage gap.
The other five flaws do not supply sufficient exploit artifacts in this article
to justify new exploit detections. Loopback, comparison/target hashes, fixed
Git commits, crypto material and vendor/disclosure domains are contextual;
there are no malicious identity indicators to populate SHA256/PURLS/ENDPOINTS.
