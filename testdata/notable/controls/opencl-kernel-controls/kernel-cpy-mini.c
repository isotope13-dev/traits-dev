// Minimal OpenCL host helper: the "row-mapped kernel" below is a GPU
// compute kernel kept for direct row access, never the OS kernel.
#include <CL/cl.h>

cl_kernel make_row_copy_kernel(cl_program prog, cl_int *err) {
    /* optional: without a flat variant the copy keeps the row-mapped kernel */
    return clCreateKernel(prog, "kernel_cpy_f32_f32_flat", err);
}
