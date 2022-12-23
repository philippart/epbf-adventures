#!/usr/bin/python3
#
# From isovalent (https://github.com/lizrice/ebpf-beginners)
# But with perf buffer

from __future__ import print_function
from bcc import BPF

def int2ip(signed_int):
    h = hex(signed_int & 0xffffffff)[2:]
    if len(h) == 7:
        h = '0' + h
    hex_ip = [h[:2],h[2:4],h[4:6],h[6:8]]
    ip = [str(int(n,16)) for n in hex_ip]
    ip.reverse()
    return '.'.join(ip)

interface = "lo"

# load program
b = BPF(src_file="xdp_example.c", cflags=["-Wno-macro-redefined"])
fx = b.load_func(func_name="xdp", prog_type=BPF.XDP)

# attach to network interface
BPF.attach_xdp(interface, fx, 0)

# header
print("XDP ICMP packet sniffing... Ctrl-C to end\n")
print("%-8s %-12s %-8s" % ("TIME(s)", "DESTINATION", "TYPE"))

# process event
start = 0
def print_event(cpu, data, size):
    global start
    event = b["events"].event(data)
    if start == 0:
        start = event.ts
    time_s = (float(event.ts - start)) / 1000000000
    ip_address = int2ip(event.daddr)
    print("%-8.2f %-12s %-8s" % (time_s, ip_address, event.type))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        b.remove_xdp(interface, 0)
        exit()