#!/usr/bin/python3
#
# Lesson 5. sync_count.py
# Modify the sync_timing.py program  to store the count of all kernel sync system calls (both fast and slow), and print it with the output. 
# This count can be recorded in the BPF program by adding a new key index to the existing hash.

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

# load BPF program
b = BPF(text="""
#include <uapi/linux/ptrace.h>

BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    u64 ts, *tsp, delta, ts_key = 0;
    u64 count, *count_ptr, count_key = 1;

    // update the counts
    count_ptr = last.lookup(&count_key);
    if (count_ptr != NULL) {
        // cannot update directly (*count_ptr)++
        count = *count_ptr + 1;
        last.update(&count_key, &count);
    } else {
        // make sure count is initialized
        count = 1;
        last.update(&count_key, &count);
    }

    // attempt to read stored timestamp
    tsp = last.lookup(&ts_key);
    if (tsp != NULL) {
        delta = bpf_ktime_get_ns() - *tsp;
        if (delta < 1000000000) {
            // output if time is less than 1 second
            bpf_trace_printk("%d %d\\n", delta / 1000000, count);
        }
        last.delete(&ts_key);
    }

    // update stored timestamp
    ts = bpf_ktime_get_ns();
    last.update(&ts_key, &ts);
    return 0;
}
""", cflags=["-Wno-macro-redefined"])

b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")
print("Tracing for quick sync's... Ctrl-C to end")

# format output
start = 0
while 1:
    try:
        (task, pid, cpu, flags, ts, msg) = b.trace_fields()
        (ago, count) = msg.split()
        if start == 0:
            start = ts
        ts = ts - start
        printb(b"At time %.2f s: multiple syncs detected, %s ms ago (%s times)" % (ts, ago, count))
    except KeyboardInterrupt:
        exit()
