# instructions

Follow: https://github.com/iovisor/bcc

## install bcc

```bash
echo deb http://cloudfront.debian.net/debian sid main >> /etc/apt/sources.list
sudo apt-get install -y bpfcc-tools libbpfcc libbpfcc-dev linux-headers-$(uname -r)
```

## out-of-the-box programs (installed under /usr/sbin)

see [tutorial](https://github.com/iovisor/bcc/blob/master/docs/tutorial.md)
- execsnoop-bpfcc
- opensnoop-bpfcc
- biolatency-bpfcc
- ext4slower-bpfcc
- tcpretrans-bpfcc

## BPF kernel probes (kprobes)

See https://www.kernel.org/doc/html/latest/trace/kprobetrace.html

```bash
# Fetch the https://github.com/iovisor/bcc submodule
cd src/bcc
git submodule update

# increasing complexity & different data structures
sudo ./hello_bcc.py
sudo ./sync_count.py       # uses BPF hash map
sudo ./sync_perf_output.py # uses BPF perf ouput map
sudo ./disklatency.py      # uses BPF histogram
```

##  BPF tracepoints

See https://www.kernel.org/doc/html/latest/trace/tracepoints.html

Tracepoints are not available for all system calls but have a more stable api than kprobes.
Otherwise fprobes (function entry/exit) are better than kprobes (kernel syscalls).

```bash
# from bcc
sudo tplist-bpfcc
# directly
sudo cat /sys/kernel/debug/tracing/available_events

# check
sudo ls /sys/kernel/debug/tracing/events

# enable (see https://www.kernel.org/doc/html/latest/trace/events.html)
echo sched_wakeup >> /sys/kernel/debug/tracing/set_event
echo 1 > /sys/kernel/debug/tracing/events/sched/sched_wakeup/enable

# format
sudo cat /sys/kernel/debug/tracing/events/sched/sched_wakeup/format

# example program
sudo ./bcc/examples/tracing/urandomread.py
```

## BPF user probes (uprobes)

```bash
# example program
sudo ./bcc/examples/tracing/strlen_count.py
sudo ./bcc/examples/tracing/nodejs_http_server.py
```

## BPF networking

```bash
# socket filter
sudo ./sock_example.py

# XDP (express data path)
# see also: https://github.com/xdp-project/xdp-tutorial
sudo ./xdp_example.py

# Traffic control (tc) example (requires pyroute2)
python3 pip install -m pyroute2
sudo ./tc_example.py
```