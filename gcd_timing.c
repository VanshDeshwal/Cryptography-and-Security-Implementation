#include <stdio.h>
#include <stdint.h>



// Function to read the Time-Stamp Counter
static __inline__ uint64_t rdtsc(void) {
	uint32_t lo, hi;
	// The "memory" clobber ensures that the RDTSC instruction is not reordered
	// with respect to other memory operations.
	__asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi) : : "memory");
	return ((uint64_t)hi << 32) | lo;
}

int main() {
    int count=0;
    int num1, num2, remainder, temp;
    uint64_t start_cycles, end_cycles, start_loop, end_loop;

// Prompt the user to enter two numbers
    printf("Enter two positive integers: ");
    scanf("%d %d", &num1, &num2);

    // Ensure both numbers are positive for the algorithm
    if (num1 < 0) num1 = -num1;
    if (num2 < 0) num2 = -num2;

    // Implement the Euclidean algorithm
    // The loop continues as long as num2 is not zero
    start_cycles = rdtsc();
    while (num2 != 0) {
	//start_loop = rdtsc();
	count++;
        remainder = num1 % num2; // Calculate the remainder
        num1 = num2;             // Update num1 to the previous num2
        num2 = remainder;        // Update num2 to the remainder
	//end_loop = rdtsc();
//	printf("CPU cycles for %d th loop: %lu\n",count,end_loop - start_loop);
    }
    end_cycles = rdtsc();


    // When the loop terminates, num1 holds the GCD
    printf("GCD of the given numbers is %d\n", num1);
    printf("Total CPU cycles for the while loop: %lu\n", end_cycles - start_cycles);
    //printf("No. of times while loop ran: %d\n", count);

    return 0;
}
