; audio service forwarders (variant shape, new carrier names).

bits 64
default rel

extern audio_proxy_init_once

extern audio_real_initialize
extern audio_real_render
extern audio_real_shutdown

section .text

%macro FORWARD 2
global %1
%1:
    push  rax
    push  rcx
    sub   rsp, 48
    call  audio_proxy_init_once
    add   rsp, 48
    pop   rcx
    pop   rax
    cmp   qword [rel %2], 0
    je    %%missing
    jmp   qword [rel %2]
%%missing:
    xor   eax, eax
    ret
%endmacro

FORWARD AudioInitialize, audio_real_initialize
FORWARD AudioRender,     audio_real_render
FORWARD AudioShutdown,   audio_real_shutdown
