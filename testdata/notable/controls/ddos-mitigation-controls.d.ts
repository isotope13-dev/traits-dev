// Benign control: defensive DDoS-mitigation configuration interface. Names
// flood types (SYN flood, UDP flood, slowloris flood) only to describe what
// the generated nftables/sysctl hardening stops; a declaration file carries
// no flood implementation.
/**
 * Layer 3/4 DDoS mitigation for a box we control: SYN flood, UDP flood and
 * slowloris flood traffic is stopped in the kernel, for free.
 */
export interface DdosThresholds {
  /** New connections per second, per source IP, before the source is dropped. */
  newConnectionsPerSecond: number;
  /** SYN packets per second accepted platform-wide before SYN cookies do the work. */
  synPerSecond: number;
  /** Burst allowance on top of the per-second rates. */
  burst: number;
}
export declare function renderNftablesRuleset(config?: DdosThresholds): string;
export declare function sysctlHardening(config?: DdosThresholds): Record<string, string>;
