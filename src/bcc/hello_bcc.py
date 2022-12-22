#!/usr/bin/python3

# lesson 2 from https://github.com/iovisor/bcc/blob/master/docs/tutorial_bcc_python_developer.md
# Write a program that traces the sys_sync() kernel function. 
# Print "sys_sync() called" when it runs. T
# est by running sync in another session while tracing.
# Improve it by printing "Tracing sys_sync()... Ctrl-C to end." when the program first starts. Hint: it's just Python.

# bonus: get rid of macro redefined warnings (see https://github.com/iovisor/bcc/issues/3366)

from bcc import BPF

print("Tracing sys_sync()... Ctrl-C to end.")

prog = '''
int kprobe__sys_sync(void *ctx) { 
    bpf_trace_printk("sys_sync() called\\n");
    return 0; 
}
'''
BPF(text=prog, cflags=["-Wno-macro-redefined"]).trace_print()
