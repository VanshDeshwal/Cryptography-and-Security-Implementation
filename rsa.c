

#include <gmp.h>
#include <stdio.h>
#include <stdlib.h> // For exit()
#include <time.h>   // For seeding

int main() {
    gmp_randstate_t state;
    gmp_randinit_default(state);

    // Seed the generator (using time for simplicity, but for security, use a better source)
    gmp_randseed_ui(state, time(NULL));

    mpz_t prime_candidate, prime;
    mpz_inits(prime_candidate, prime, NULL);

    // Generate a random 512-bit number
    mpz_urandomb(prime_candidate, state, 511);
    mpz_setbit(prime_candidate, 511); // Ensure it's a 512-bit number
    mpz_setbit(prime_candidate, 0);    // Ensure it's odd

    // Find the next prime number
    mpz_nextprime(prime, prime_candidate);

    // (Optional) Perform an additional primality test
    int reps = 25; // Number of Miller-Rabin iterations
    if (mpz_probab_prime_p(prime, reps) == 0) {
        fprintf(stderr, "Error: mpz_nextprime returned a composite number!\n");
        exit(EXIT_FAILURE);
    } else {
        printf("Found a 512-bit prime:\n");
        gmp_printf("%Zd\n", prime);
    }

mpz_clears(prime_candidate, prime, NULL);
    gmp_randclear(state);

    return 0;
}
