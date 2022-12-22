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

## python programs

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