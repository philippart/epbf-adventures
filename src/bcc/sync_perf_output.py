#!/usr/bin/python3
#
# Lesson 8. sync_count.py
# Rewrite sync_timing.py (actually sync_count.py) to use BPF_PERF_OUTPUT (like examples/tracing/hello_pef_output.py).

from __future__ import print_function
from bcc import BPF
from bcc.utils import printb

#  BPF program
prog = """
#include <uapi/linux/ptrace.h>

// output data structure
struct data_t {
    u64 ts;
    u64 delta;
    u64 count;
};
BPF_PERF_OUTPUT(events);

// store last timestamp and total count
BPF_HASH(last);

int do_trace(struct pt_regs *ctx) {
    struct data_t data = {};

    u64 *ts_ptr, ts_key = 0;
    u64 *count_ptr, count_key = 1;

    // count the total number of syncs
    count_ptr = last.lookup(&count_key);
    if (count_ptr != NULL) {
        data.count = *count_ptr + 1;
        last.update(&count_key, &data.count);
    } else {
        // make sure count is initialized
        data.count = 1;
        last.update(&count_key, &data.count);
    }

    // current timestamp
    data.ts = bpf_ktime_get_ns();

    // delta since last sync (in ms)
    ts_ptr = last.lookup(&ts_key);
    if (ts_ptr != NULL) {
        data.delta = (data.ts - *ts_ptr) / 1000000;
        // output if time is less than 1 second
        if (data.delta < 1000) {
            events.perf_submit(ctx, &data, sizeof(data));
        }
    }

    // update stored timestamp
    last.update(&ts_key, &data.ts);
    return 0;
}
"""
b = BPF(text=prog, cflags=["-Wno-macro-redefined"])
b.attach_kprobe(event=b.get_syscall_fnname("sync"), fn_name="do_trace")

print("Tracing for quick sync's... Ctrl-C to end")

# header
print("%-8s %-8s %-6s" % ("TIME(s)", "AGO(ms)", "COUNT"))

# process event
start = 0
def print_event(cpu, data, size):
    global start
    event = b["events"].event(data)
    if start == 0:
        start = event.ts
    time_s = (float(event.ts - start)) / 1000000000
    printb(b"%-8.2f %-8d %-6d" % (time_s, event.delta, event.count))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
