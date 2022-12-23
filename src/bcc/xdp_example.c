#include "headers/network.h""

// output data structure
struct output_t {
    u64 ts;
    u64 daddr;
    u64 type;
};

BPF_PERF_OUTPUT(events);

int xdp(struct xdp_md *ctx) {
    struct output_t output = {};

    void *data = (void*)(long)ctx->data;
    void *data_end = (void*)(long)ctx->data_end;

    if (is_icmp_ping_request(data, data_end)) {
        struct iphdr *iph = data + sizeof(struct ethhdr);
        struct icmphdr *icmp = data + sizeof(struct ethhdr) + sizeof(struct iphdr);
        output.ts = bpf_ktime_get_ns();
        output.daddr = iph->daddr;
        output.type = icmp->type;
        events.perf_submit(ctx, &output, sizeof(output));
    }

    return XDP_PASS;
}
