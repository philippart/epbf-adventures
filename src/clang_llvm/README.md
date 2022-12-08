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