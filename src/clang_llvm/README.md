#  instructions

reproducing: https://qmonnet.github.io/whirl-offload/2020/04/12/llvm-ebpf-asm/

## install clang and llvm
```bash
# install clang-15 and llvm
sudo bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"
cat << EOF >> ~/.bash_aliases
alias clang=clang-15
alias llc=llc-15
alias llvm-mc=llvm-mc-15
alias llvm-objdump=llvm-objdump-15
EOF
source ~/.bash_aliases

# better: create symlink instead of aliases
cd /usr/bin
sudo ln -s clang-15 clang
sudo ln -s llvm-strip-15 llvm-strip
# and so on
```

## from C to object file
```bash
# compile to object
clang -target bpf -Wall -O2 -c my_bpf_program.c -o my_bpf_objfile.o
# or: clang -O2 -emit-llvm -c my_bpf_program.c -o - | llc -march=bpf -mcpu=probe -filetype=obj -o my_bpf_objfile.o

# read ELF (see https://github.com/iovisor/bpf-docs/blob/master/eBPF.md for interpretation)
readelf -x .text my_bpf_objfile.o
```

## compile C to assembly
```bash
# compile to assembly
clang -target bpf -S -o bpf.s bpf.c

# modify assembly directly (add instruction)
sed -i '$a \\tr0 = 3' bpf.s

# assemble to ELF object
llvm-mc -triple bpf -filetype=obj -o bpf.o bpf.s

# read ELF as we did above
readelf -x .text bpf.o

# human readable dump with llvm
llvm-objdump -d bpf.o

# repeat with clang -g instruction to embed in the C code
clang -target bpf -g -S -o bpf.s bpf.c
llvm-mc -triple bpf -filetype=obj -o bpf.o bpf.s
llvm-objdump -S bpf.o
```

## inline assembly in C code
```bash
clang -target bpf -Wall -O2 -c inline_asm.c -o inline_asm.o
llvm-objdump -d inline_asm.o
```

# inspect ebpf programs and maps with bpftool

See [introduction to bpftool](https://qmonnet.github.io/whirl-offload/2021/09/23/bpftool-features-thread/)
Install with `apt install bpftool`.

```bash
# bptool must be run with 'sudo'

# list of eBPF programs loaded
bpftool prog show

# load a program from object code
# note the examplse above fail to load because they lack a "section(...)" statement to attach to a ebpf hook
bpftool prog load foo.o /sys/fs/bpf/bar

# dump the bytecode of a program
bpftool prog dump xlated id 18

# attaching a program to a hook (xdp example)
bpftool net attach xdp id 42 dev eth0

# show ebpf maps
bpftool map show

# generate skeleton.h for libbpf-bootstrap
bpftool gen skeleton ... # see [Makefile](../libbpf-bootstrap/libbpf-bootstrap/examples/c/Makefile) 

# and many more...
```