# Summary of eBPF vulnerabilities (eBPF for bad)

Searching for "eBPF" vunerabilities in the NSIT database finds 14 matches:
https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=ebpf&search_type=all&isCpeNameSearch=false
https://www.cvedetails.com/google-search-results.php?q=ebpf&sa=Search

The majority of these vulnerabilities is related to issues in the eBPF verifier, JIT compiler, loader or bpf helper functions allowing out-of-bound memory access.

## 🔥 CVE-2020-8835: Improper eBPF Program Verification

Reference: [zerodayinitiative](https://www.zerodayinitiative.com/blog/2020/4/8/cve-2020-8835-linux-kernel-privilege-escalation-via-improper-ebpf-program-verification)

This vulnerability exploits a bug in the eBPF verifier (the program that validates eBPF programs when they are loaded) to perform a local privilege escalation.
In the Linux kernel 5.5.0 and newer, the bpf verifier (kernel/bpf/verifier.c) did not properly restrict the register bounds for 32-bit operations, leading to out-of-bounds reads and writes in kernel memory


## 🔥 CVE-2021-3490: Improper eBPF Program Verification

Reference: [chompie1337](https://github.com/chompie1337/Linux_LPE_eBPF_CVE-2021-3490/tree/main/include)

The eBPF ALU32 bounds tracking for bitwise ops (AND, OR and XOR) in the Linux kernel did not properly update 32-bit bounds, which could be turned into out of bounds reads and writes in the Linux kernel and therefore, arbitrary code execution.

This is very similar to the above.