# eBPF for security monitoring or hiding

eBPF can be used for good (detecting) or for bad (hiding)...

## ✅ Detecting container escapes

Reference: [isovalent](https://isovalent.com/blog/post/2021-11-container-escape/)

### Problem

During a container escape (privileged pod running in host pid/network namespace) an attacker breaks the isolation boundary between the host and the container, 
ending up escaping into what is eventually a Kubernetes control plane or a worker node.

Applying security best practises on a Kubernetes environment can limit these types of attacks but a container breakout is still possible, 
an attacker can use a privileged pod or exploit an existing vulnerability to gain privileges.

### Solution

By using eBPF to trace process executions (like execsnoop) and correlating this with information from the kubernetes API (name, namespace, container id, labels), 
Security Teams can get visibility into any Kubernetes workloads, such as pods or jobs. 
Because pods on a Kubernetes node share a single kernel, each of the processes within a pod are visible to a single eBPF program.

## ✅ Detecting/blocking fileless memory execution

References: 
- [isovalent](https://isovalent.com/blog/post/2021-11-container-escape/)
- [Djalal Harouni](https://djalal.opendz.org/post/ebpf-block-linux-fileless-payload-execution-with-bpf-lsm/)

### Problem

Malicious code can be executed in memory without any disk access therefore leaving no trace on disk.

### Solution

Use eBPF to trace in-memory process executions (same as above).
Use [bpflock](https://github.com/linux-lock/bpflock/blob/main/docs/process-protections.md) to restrict fileless memory execution.

## ✅ Comand line cloaking

References:
- [path/to/file](https://blog.tofile.dev/2022/01/04/sysmonlinux.html)
- [sysmon for linux](https://github.com/Sysinternals/SysmonForLinux)
- [tetragon](https://blog.tofile.dev/2022/08/04/tetragon.html)


### Problem

A lot of malware detections on Linux are based upon on pattern matching command line arguments and program filenames. 
But a program can alter or hide command line arguments and program filenames from Audit tools.

### Solution

- Sysmon for linux
- Tetragon
- and more


## ✅ Hiding malicious processes (ebpf for bad)

Reference: [cymulate](https://cymulate.com/blog/ebpf_hacking/)

### Problem

Using an eBPF rootkit to hide malicious processes from “ps” like programs by hooking into the getdents64() system call via a tracepoint
and removing entries from the dirent buffer (array of struct linx_dirent64).

### Solution

Prevent unauthorised eBPF programs (seccomp profile, monitor bpf() system call, bpfblock...).


## ✅ Security Profile

Reference: 
- [article](https://developers.redhat.com/articles/2021/12/16/secure-your-kubernetes-deployments-ebpf)
- [security profile operator](https://github.com/kubernetes-sigs/security-profiles-operator)

### Problem

Numerous adaptations of the Linux kernel — notably seccomp, SELinux, and AppArmor — bolster its security through runtime checks on sensitive activities such as file access and system calls (syscalls). In particular, seccomp denies access to system calls that don't match prebuild profiles of allowed calls. But the creation of seccomp profiles for Kubernetes workloads can be a major obstacle to deploying containerized applications. Those profiles have to be maintained over the complete life cycle of the application because changing the code might require changes to the seccomp rules as well.

### Solution

To overcome this burden, it would be absolutely stunning if developers could record seccomp profiles by running a test suite against the application and automatically deploy the results together with the application manifest. But how to record seccomp profiles? Well, the Security Profiles Operator in Kubernetes offers several ways to record activity. The Security Profile Operator provides a BPF recorder to do just that.


## ✅ Bypassing eBPF security

Reference: 
- [doyensec](https://blog.doyensec.com/2022/10/11/ebpf-bypass-security-monitoring.html)
- [symbiote](https://medium.com/geekculture/symbiote-a-nearly-undetectable-linux-malware-fcf4f4e13b4f)

![symbiote evasion etchniques](https://miro.medium.com/max/720/1*49yvN_X_uWOgmfTRaA2h0w.webp)

- bypassing execve() system call
- bypassing network hooks if not monitoring all of them
- delayed execution (quit console session)
- evading cgroup monitoring
- exploiting eBPF memory or performance limits
- unloading eBPF monitoring programs if seccomp-BPF profile
- replacing dynamically loaded shared libraries like libbcc.so


## ✅ Sniffing PAM logon passwords

Reference: [embracethered](https://embracethered.com/blog/posts/2022/offensive-bpf-bpftrace-sniff-logon-pam-passwords/)

### Problem

Using eBPF (as simple as bpftrace) to trace the pam_getauthtok() of the libpam.so library with a user probe and read the username and password.

### Solution

Same as above (seccomp, bpflock or monitor eBPF programs and which API they trace).

## ✅ Hidding files, directories, ports, logins, lying to sudo, faking/hijacking syscall

References: 
- [embracethered](https://embracethered.com/blog/posts/2021/offensive-bpf-libbpf-bpf_probe_write_user/)
- [bad bpf](https://blog.tofile.dev/2021/08/01/bad-bpf.html)
- [rootkit with ftrace](https://xcellerator.github.io/categories/linux/) - technically not BPF but ftrace + kernel modules but ideas can be transposed to eBPF
