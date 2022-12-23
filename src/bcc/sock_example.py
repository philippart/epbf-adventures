#!/usr/bin/python3
#
# count IP packets on loopback interface per protocol
#
# From https://www.collabora.com/news-and-blog/blog/2019/04/26/an-ebpf-overview-part-3-walking-up-the-software-stack/

from __future__ import print_function
from bcc import BPF
import time, socket

# BPF program
prog = """
#include <uapi/linux/if_ether.h>
#include <uapi/linux/ip.h>

BPF_ARRAY(count_map, u64, 256);

int count_packets(struct __sk_buff *skb) {
    int index = load_byte(skb, ETH_HLEN	+ offsetof(struct iphdr, protocol));
    u64 *value = count_map.lookup(&index);
    if (value) {
        count_map.increment(index);
    }
    return 0;
}
"""
# load program
b = BPF(text=prog, cflags=["-Wno-macro-redefined"])
ffilter = b.load_func("count_packets", BPF.SOCKET_FILTER)

# attach to loopback interface
BPF.attach_raw_socket(ffilter, "lo")

print("Counting IP packets...")

# header
print("%-8s %-8s %-8s" % ("TCP", "UDP", "ICMP"))

# format output
for i in range(10):
    print("%-8d %-8d %-8d" % (
        b["count_map"][socket.IPPROTO_TCP].value,
        b["count_map"][socket.IPPROTO_UDP].value,
        b["count_map"][socket.IPPROTO_ICMP].value))
    time.sleep(1)
