#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>
#include <wmmintrin.h>

#define ENCRYPTION_UNIT_SIZE 16
#define NUM_ROUNDS 10

typedef struct {
    __m128i sch_words[NUM_ROUNDS + 1];
} aes_ctx_data;

void generate_schedule(const uint8_t *secret_key, aes_ctx_data *context) {
    __m128i k_reg, temp_reg;
    k_reg = _mm_loadu_si128((const __m128i*)secret_key);
    context->sch_words[0] = k_reg;

    #define KEY_ASSIST_HELPER(rcon_val) \
        temp_reg = _mm_aeskeygenassist_si128(k_reg, rcon_val); \
        temp_reg = _mm_shuffle_epi32(temp_reg, 0xFF); \
        k_reg = _mm_xor_si128(k_reg, _mm_slli_si128(k_reg, 0x4)); \
        k_reg = _mm_xor_si128(k_reg, _mm_slli_si128(k_reg, 0x4)); \
        k_reg = _mm_xor_si128(k_reg, _mm_slli_si128(k_reg, 0x4)); \
        k_reg = _mm_xor_si128(k_reg, temp_reg);

    KEY_ASSIST_HELPER(0x01); context->sch_words[1] = k_reg;
    KEY_ASSIST_HELPER(0x02); context->sch_words[2] = k_reg;
    KEY_ASSIST_HELPER(0x04); context->sch_words[3] = k_reg;
    KEY_ASSIST_HELPER(0x08); context->sch_words[4] = k_reg;
    KEY_ASSIST_HELPER(0x10); context->sch_words[5] = k_reg;
    KEY_ASSIST_HELPER(0x20); context->sch_words[6] = k_reg;
    KEY_ASSIST_HELPER(0x40); context->sch_words[7] = k_reg;
    KEY_ASSIST_HELPER(0x80); context->sch_words[8] = k_reg;
    KEY_ASSIST_HELPER(0x1B); context->sch_words[9] = k_reg;
    KEY_ASSIST_HELPER(0x36); context->sch_words[10] = k_reg;

    #undef KEY_ASSIST_HELPER
}

static inline void process_block(aes_ctx_data *context, uint8_t *data_ptr) {
    __m128i data_reg = _mm_loadu_si128((__m128i*)data_ptr);
    data_reg = _mm_xor_si128(data_reg, context->sch_words[0]);

    int round_idx;
    for (round_idx = 1; round_idx < NUM_ROUNDS; ++round_idx) {
        data_reg = _mm_aesenc_si128(data_reg, context->sch_words[round_idx]);
    }
    
    data_reg = _mm_aesenclast_si128(data_reg, context->sch_words[NUM_ROUNDS]);
    _mm_storeu_si128((__m128i*)data_ptr, data_reg);
}

void process_data_buffer(aes_ctx_data *context, uint8_t *data_buffer, size_t buffer_length) {
    size_t block_offset = 0;
    for (; block_offset < buffer_length; block_offset += ENCRYPTION_UNIT_SIZE) {
        process_block(context, data_buffer + block_offset);
    }
}

static uint32_t prng_state = 123456789;
uint32_t prng_next() {
    prng_state = (1103515245 * prng_state + 12345) & 0x7fffffff;
    return prng_state;
}
void fill_buffer_randomly(uint8_t *dest_buf, size_t length) {
    for (size_t k = 0; k < length; ++k) {
        dest_buf[k] = (uint8_t)(prng_next() & 0xff);
    }
}

int main() {
    aes_ctx_data context;
    const size_t buffer_len = 1048576;
    uint8_t *buffer_ptr = (uint8_t *)malloc(buffer_len);
    uint8_t encryption_key[ENCRYPTION_UNIT_SIZE];

    if (buffer_ptr == NULL) {
        perror("Memory failure");
        return 1;
    }

    const int test_iterations = 10000;
    uint64_t accumulated_cycles = 0;

    for (int run_index = 0; run_index < test_iterations; ++run_index) {
        fill_buffer_randomly(buffer_ptr, buffer_len);
        fill_buffer_randomly(encryption_key, sizeof(encryption_key));
        generate_schedule(encryption_key, &context);

        uint64_t timer_start = __rdtsc();
        process_data_buffer(&context, buffer_ptr, buffer_len);
        uint64_t timer_end = __rdtsc();

        accumulated_cycles += (timer_end - timer_start);
    }

    printf("Sample encrypted output (first 16 bytes): ");
    for (int i = 0; i < 16; ++i) printf("%02x ", buffer_ptr[i]);
    printf("\n");

    printf("Data size: %zu bytes\n", buffer_len);
    printf("Total runs: %d\n", test_iterations);
    printf("Average cycles (AES only): %.2f\n", (double)accumulated_cycles / test_iterations);
    printf("Average cycles per byte: %.2f\n", ((double)accumulated_cycles / test_iterations) / buffer_len);

    free(buffer_ptr);
    return 0;
}
