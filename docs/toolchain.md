# eBPF Development Toolchains

Several toolchains are available offering higher level programming interfaces than writing raw eBPF bytecode as illustrated below.  
For a comprehensive list of tools refer to:
- [the evolving eBPF toolchain](https://oswalt.dev/2021/07/the-evolving-ebpf-toolchain/)
- [awesome eBPF](https://github.com/zoidbergwill/awesome-ebpf#ebpf-workflow-tools-and-utilities)

## Raw eBPF Bytecode

This is akin to writing in assembly language.  
Extract from [Linux bpf sock_example.c](https://github.com/torvalds/linux/blob/master/samples/bpf/sock_example.c).
```c
struct bpf_insn prog[] = {
    BPF_MOV64_REG(BPF_REG_6, BPF_REG_1),
    BPF_LD_ABS(BPF_B, ETH_HLEN + offsetof(struct iphdr, protocol) /* R0 = ip->proto */),
    BPF_STX_MEM(BPF_W, BPF_REG_10, BPF_REG_0, -4), /* *(u32 *)(fp - 4) = r0 */
    BPF_MOV64_REG(BPF_REG_2, BPF_REG_10),
    BPF_ALU64_IMM(BPF_ADD, BPF_REG_2, -4), /* r2 = fp - 4 */
    BPF_LD_MAP_FD(BPF_REG_1, map_fd),
    BPF_RAW_INSN(BPF_JMP | BPF_CALL, 0, 0, 0, BPF_FUNC_map_lookup_elem),
    BPF_JMP_IMM(BPF_JEQ, BPF_REG_0, 0, 2),
    BPF_MOV64_IMM(BPF_REG_1, 1), /* r1 = 1 */
    BPF_RAW_INSN(BPF_STX | BPF_XADD | BPF_DW, BPF_REG_0, BPF_REG_1, 0, 0), /* xadd r0 += r1 */
    BPF_MOV64_IMM(BPF_REG_0, 0), /* r0 = 0 */
    BPF_EXIT_INSN(),
};
```

## LLVM Clang eBPF compiler

Same as above using "restricted C".  
Extract from [Linux bpf sockex1_kern.c](https://github.com/torvalds/linux/blob/master/samples/bpf/sockex1_kern.c).
```c
int bpf_prog1(struct __sk_buff *skb)
{
	int index = load_byte(skb, ETH_HLEN + offsetof(struct iphdr, protocol));
	long *value;

	if (skb->pkt_type != PACKET_OUTGOING)
		return 0;

	value = bpf_map_lookup_elem(&my_map, &index);
	if (value)
		__sync_fetch_and_add(value, skb->len);

	return 0;
}
```
LLVM compiles a "restricted C" language (no unbounded loops, max 4096 instructions, ...) to ELF object files containing special sections
which get loaded in the kernel using libraries like libbpf, built on top of the bpf() syscall.

### installation instructions
 
See [eBPF assembly with LLVM](https://qmonnet.github.io/whirl-offload/2020/04/12/llvm-ebpf-asm/).  
Example from linux kernel [eBPF in pure C](https://terenceli.github.io/%E6%8A%80%E6%9C%AF/2020/01/18/ebpf-in-c).

## libbpf-bootstrap

Key resources:
- 

### installation instructions


## BPF Compiler Collection (BCC)

Key resources:
- [bcc tutorial](https://github.com/iovisor/bcc/blob/master/docs/tutorial.md)
- [eBPF tracing with bcc and bpftrace](https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html)

### installation instructions

See [bcc installation](https://github.com/iovisor/bcc/blob/master/INSTALL.md)

Check the kernel configuration with `grep BPF /boot/config-<kernel-version>` and compare with requirements from the link above.

## bpftrace

Key resources:
- [bpftrace](https://github.com/iovisor/bpftrace)

### installation instructions