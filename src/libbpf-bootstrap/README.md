# instructions

reproducing: https://nakryiko.com/posts/bpf-tips-printk/

## install libbpf-bootstrap

```bash
# the src/libbpf-bootstrap directory contains a "libbpf-bootstrap" submodule
cd src/libpf-bootstrap
git submodule update --init --recursive

# or clone it anywhere you like with
git clone --recursive https://github.com/libbpf/libbpf-bootstrap
```

## install dependencies

```bash
# zlib (libz-dev or zlib-devel package)
sudo apt install zlib1g-dev

# libelf (libelf-dev or elfutils-libelf-devel package)
sudo apt install libelf-dev
```

## minimal example

see [libbpf-botstrap/README.md](./libbpf-bootstrap/README.md#minimal)
```bash
# edit makefile to use clang-15 and llvm-strip-15 - whichever version you are using
cd libbpf-bootstrap/examples/c
make minimal
sudo ./minimal
sudo cat /sys/kernel/debug/tracing/trace_pipe
    minimal-19100   [000] d...  8792.898385: bpf_trace_printk: BPF triggered from PID 19100.
    minimal-19100   [000] d...  8793.901152: bpf_trace_printk: BPF triggered from PID 19100.
```

## bootstrap example

see [libbpf-botstrap/README.md](./libbpf-bootstrap/README.md#bootstrap)
```bash
make kootstrap
sudo ./bootstrap -d 50
```

## XDP example in rust

see [libbpf-botstrap/README.md](./libbpf-bootstrap/README.md#xdp)
```bash
# install rust and cargo
curl https://sh.rustup.rs -sSf | sh

# install libbpf-cargo
source ~/.cargo/env
cargo install libbpf-cargo

# build the project
cd /examples/rust
cargo build --release
sudo ./target/release/xdp 1
    node-2851    [001] d.s1 17973.678705: bpf_trace_printk: packet size: 83
    sshd-2416    [001] d.s1 17973.683104: bpf_trace_printk: packet size: 93
```