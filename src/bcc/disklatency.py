#!/usr/bin/python3
#
# Lesson 10. disklatency.py
# Write a program that times disk I/O, and prints a histogram of their latency. 
# Disk I/O instrumentation and timing can be found in disksnoop.py
# and histogram code can be found in bitehist.py.

from __future__ import print_function
from bcc import BPF
from time import sleep

# load BPF program
prog = """
#include <uapi/linux/ptrace.h>
#include <linux/blk-mq.h>

// latency histogram (log scale)
BPF_HISTOGRAM(dist);

// request latency
BPF_HASH(start, struct request *);

void trace_start(struct pt_regs *ctx, struct request *req) {
	// stash start timestamp by request ptr
	u64 ts = bpf_ktime_get_ns();

	start.update(&req, &ts);
}

void trace_completion(struct pt_regs *ctx, struct request *req) {
	u64 *tsp, delta;

	tsp = start.lookup(&req);
	if (tsp != 0) {
		delta = (bpf_ktime_get_ns() - *tsp) / 1000000;
		// delta = delta > 1 ? delta : 1;
		dist.increment(bpf_log2l(delta));
		start.delete(&req);
	}
}
"""
b = BPF(text=prog, cflags=["-Wno-macro-redefined"])

if BPF.get_kprobe_functions(b'blk_start_request'):
    b.attach_kprobe(event="blk_start_request", fn_name="trace_start")
b.attach_kprobe(event="blk_mq_start_request", fn_name="trace_start")
if BPF.get_kprobe_functions(b'__blk_account_io_done'):
    b.attach_kprobe(event="__blk_account_io_done", fn_name="trace_completion")
else:
    b.attach_kprobe(event="blk_account_io_done", fn_name="trace_completion")

# header
print("Tracing... Hit Ctrl-C to end.")

# trace until Ctrl-C
try:
    sleep(99999999)
except KeyboardInterrupt:
    print()

# output
print("histogram")
print("---------")
b["dist"].print_log2_hist("latency(ms)")
