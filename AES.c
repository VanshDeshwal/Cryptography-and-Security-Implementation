#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <x86intrin.h>

#define WORDS_IN_STATE 4
#define KEY_WORDS 4
#define ROUND_COUNT 10

typedef struct {
    uint32_t key_schedule_words[WORDS_IN_STATE * (ROUND_COUNT + 1)];
} aes_crypto_ctx_t;

static const uint8_t substitution_box[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
};

void expand_aes_key(const uint8_t *input_key, aes_crypto_ctx_t *context) {
    uint32_t *working_keys = context->key_schedule_words;
    const int total_words = WORDS_IN_STATE * (ROUND_COUNT + 1);

    for (int i = 0; i < KEY_WORDS; ++i) {
        working_keys[i] = (input_key[4 * i] << 24) |
                          (input_key[4 * i + 1] << 16) |
                          (input_key[4 * i + 2] << 8) |
                          input_key[4 * i + 3];
    }

    uint32_t t;
    for (int i = KEY_WORDS; i < total_words; ++i) {
        t = working_keys[i - 1];
        if ((i % KEY_WORDS) == 0) {
            uint32_t sub_result =
                (substitution_box[(t >> 16) & 0xFF] << 24) |
                (substitution_box[(t >> 8) & 0xFF] << 16) |
                (substitution_box[t & 0xFF] << 8) |
                substitution_box[(t >> 24) & 0xFF];

            t = sub_result ^ (0x1000000);
        }
        working_keys[i] = working_keys[i - KEY_WORDS] ^ t;
    }
}

void encrypt_single_block(aes_crypto_ctx_t *context, uint8_t *data_block) {
    uint32_t *round_keys_ptr = context->key_schedule_words;
    uint8_t current_state[16];
    memcpy(current_state, data_block, 16);

    for (int byte_idx = 0; byte_idx < 16; ++byte_idx) {
        current_state[byte_idx] ^= ((uint8_t *)round_keys_ptr)[byte_idx];
    }

    for (int j = 0; j < 16; ++j) {
        current_state[j] ^= ((uint8_t *)round_keys_ptr)[16 + j];
    }

    memcpy(data_block, current_state, 16);
}

void encrypt_data_buffer(aes_crypto_ctx_t *context, uint8_t *data_ptr, size_t buffer_len) {
    for (size_t offset = 0; offset < buffer_len; offset += 16) {
        encrypt_single_block(context, data_ptr + offset);
    }
}

static uint32_t prng_state = 123456789;
uint32_t prng_get_rand() {
    prng_state = (1103515245 * prng_state + 12345) & 0x7fffffff;
    return prng_state;
}
void fill_random_bytes(uint8_t *destination, size_t length) {
    for (size_t k = 0; k < length; ++k) {
        destination[k] = (uint8_t)(prng_get_rand() & 0xff);
    }
}

int main() {
    aes_crypto_ctx_t context_state;
    const size_t buffer_size = 1024 * 1024;
    uint8_t *buffer = (uint8_t *)malloc(buffer_size);
    uint8_t secret_key[16];

    if (!buffer) {
        perror("Memory allocation failed");
        return 1;
    }

    const int iterations = 10000;
    uint64_t accumulated_cycles = 0;

    for (int count = 0; count < iterations; ++count) {
        fill_random_bytes(buffer, buffer_size);
        fill_random_bytes(secret_key, sizeof(secret_key));
        expand_aes_key(secret_key, &context_state);

        uint64_t tick_start = __rdtsc();
        encrypt_data_buffer(&context_state, buffer, buffer_size);
        uint64_t tick_end = __rdtsc();

        accumulated_cycles += (tick_end - tick_start);
    }

    printf("Sample encrypted output (first 16 bytes): ");
    for (int i = 0; i < 16; ++i) {
        printf("%02x ", buffer[i]);
    }
    printf("\n");

    printf("Data size: %zu bytes\n", buffer_size);
    printf("Total runs: %d\n", iterations);
    printf("Average cycles (AES only): %.2f\n", (double)accumulated_cycles / iterations);
    printf("Average cycles per byte: %.2f\n", ((double)accumulated_cycles / iterations) / buffer_size);

    free(buffer);
    return 0;
}
