int func()
{
    unsigned long long foobar = 2, r3 = 3, *foobar_addr = &foobar;
    asm volatile("lock *(u64 *)(%0+0) += %1" :
         "=r"(foobar_addr) :
         "r"(r3), "0"(foobar_addr));
    return foobar;
}