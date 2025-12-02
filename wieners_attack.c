#include <stdio.h>
#include <gmp.h>

#define MAX_CF_TERMS 2048 // Should be enough for continued fraction terms for normal key sizes

// Function to run Wiener's attack given N and e
void run_attack(mpz_t N, mpz_t e) {
    // If e < N, we will work with N/e instead of e/N and later swap k and d
    int use_reciprocal = (mpz_cmp(e, N) < 0);

    mpz_t num, den, q, r;
    mpz_inits(num, den, q, r, NULL);

    if (!use_reciprocal) {
        mpz_set(num, e);
        mpz_set(den, N);
    } else {
        mpz_set(num, N);
        mpz_set(den, e);
    }
    
    // Array to store continued fraction terms a[0], a[1], ...
    mpz_t a[MAX_CF_TERMS];
    int cf_len = 0;
    for (int i = 0; i < MAX_CF_TERMS; ++i) mpz_init(a[i]);

    // Euclidean algorithm to get continued fraction expansion
    while (mpz_cmp_ui(den, 0) != 0 && cf_len < MAX_CF_TERMS) {
        mpz_fdiv_q(q, num, den);
        mpz_set(a[cf_len++], q);
        mpz_mod(r, num, den);
        mpz_set(num, den);
        mpz_set(den, r);
    }

    // Variables for convergent generation (p/q form)
    mpz_t p_prev2, p_prev1, p_curr;
    mpz_t q_prev2, q_prev1, q_curr;
    mpz_inits(p_prev2, p_prev1, p_curr, q_prev2, q_prev1, q_curr, NULL);
    mpz_set_ui(p_prev2, 0);
    mpz_set_ui(p_prev1, 1);
    mpz_set_ui(q_prev2, 1);
    mpz_set_ui(q_prev1, 0);

     // Extra vars for testing each convergent
    mpz_t cand_k, cand_d, lhs, phi, S, discr, sqrt_discr, p, qv, tmp, one, prod;
    mpz_inits(cand_k, cand_d, lhs, phi, S, discr, sqrt_discr, p, qv, tmp, one, prod, NULL);
    mpz_set_ui(one, 1);

    int found = 0;

    // Loop through each CF term and test
    for (int i = 0; i < cf_len; ++i) {
        // Generate next convergent
        mpz_mul(tmp, a[i], p_prev1);
        mpz_add(p_curr, tmp, p_prev2);

        mpz_mul(tmp, a[i], q_prev1);
        mpz_add(q_curr, tmp, q_prev2);

        // Shift previous values for next iteration
        mpz_set(p_prev2, p_prev1);
        mpz_set(p_prev1, p_curr);
        mpz_set(q_prev2, q_prev1);
        mpz_set(q_prev1, q_curr);

        // Depending on reciprocal choice, set candidate k and d
        if (!use_reciprocal) {
            mpz_set(cand_k, p_curr);
            mpz_set(cand_d, q_curr);
        } else {
            mpz_set(cand_k, q_curr);
            mpz_set(cand_d, p_curr);
        }

        // If d is zero, skip (invalid)
        if (mpz_cmp_ui(cand_d, 0) == 0)
            continue;

        // ed - 1 must be divisible by k
        mpz_mul(lhs, e, cand_d);
        mpz_sub_ui(lhs, lhs, 1);

        if (!mpz_divisible_p(lhs, cand_k))
            continue;

        // phi(N) candidate
        mpz_divexact(phi, lhs, cand_k);

        // S = p + q
        mpz_sub(S, N, phi);
        mpz_add(S, S, one);

        // discriminant = S^2 - 4N
        mpz_mul(discr, S, S);
        mpz_mul_ui(tmp, N, 4);
        mpz_sub(discr, discr, tmp);

        // Negative discriminant or not perfect square => not valid
        if (mpz_sgn(discr) < 0 || !mpz_perfect_square_p(discr))
            continue;

        mpz_sqrt(sqrt_discr, discr);

        // Solve for p and q
        mpz_add(tmp, S, sqrt_discr);
        mpz_fdiv_q_2exp(p, tmp, 1); // divide by 2

        mpz_sub(tmp, S, sqrt_discr);
        mpz_fdiv_q_2exp(qv, tmp, 1);    // divide by 2

        // Check if p*q == N (extra safety)
        mpz_mul(prod, p, qv);
        if (mpz_cmp(prod, N) == 0) {
            printf("\n[+] SUCCESS: recovered keys\n");
            gmp_printf("    private d = %Zd\n", cand_d);
            gmp_printf("    p = %Zd\n", p);
            gmp_printf("    q = %Zd\n", qv);
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("\n[-] No solution found. Either d is not small enough or inputs are invalid.\n");
    }

    for (int i = 0; i < MAX_CF_TERMS; ++i) mpz_clear(a[i]);
    mpz_clears(num, den, q, r, p_prev2, p_prev1, p_curr, q_prev2, q_prev1, q_curr,
               cand_k, cand_d, lhs, phi, S, discr, sqrt_discr, p, qv, tmp, one, prod, NULL);
}

int main(void) {
    mpz_t N, e;
    mpz_inits(N, e, NULL);

    printf("=== Wiener's Attack on RSA ===\n");
    printf("Select mode:\n");
    printf("  1) Manual input\n");
    printf("  2) Paper example (p=113, q=79, d=5, e=6989)\n");
    printf("Choice: ");
    int choice;
    scanf("%d", &choice);

    if (choice == 1) {
        printf("Enter modulus N: ");
        gmp_scanf("%Zd", N);
        printf("Enter public exponent e: ");
        gmp_scanf("%Zd", e);
    } else {
        mpz_set_ui(N, 8927);
        mpz_set_ui(e, 6989);
        printf("\n[+] Using paper example: N=8927, e=6989 (expected d=5)\n");
    }

    run_attack(N, e);
    return 0;
}
