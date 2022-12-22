# instructions

Follow: https://github.com/iovisor/bcc

## install bcc
```bash
echo deb http://cloudfront.debian.net/debian sid main >> /etc/apt/sources.list
sudo apt-get install -y bpfcc-tools libbpfcc libbpfcc-dev linux-headers-$(uname -r)
```

## out-of-the-box programs
see [tutorial](https://github.com/iovisor/bcc/blob/master/docs/tutorial.md)
- execsnoop-bpfcc
- opensnoop-bpfcc
- biolatency-bpfcc
- ext4slower-bpfcc
- tcpretrans-bpfcc
- 