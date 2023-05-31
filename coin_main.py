import math
import time


def generate_primes(n):
    # Generate a list of prime numbers up to n using the Sieve of Eratosthenes algorithm
    primes = []
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            primes.append(p)
            for i in range(p * p, n + 1, p):
                sieve[i] = False
    return primes


def coin_combinations_single(amount, primes):
    # Calculate the number of ways to make the given amount using a single coin denomination
    dp = [0] * (amount + 1)
    dp[0] = 1
    for i in range(len(primes)):
        for j in range(primes[i], amount + 1):
            dp[j] += dp[j - primes[i]]
    return dp[amount]


def coin_combinations_double(amount, primes, num_coins):
    # Calculate the number of ways to make the given amount using two different coin denominations
    if num_coins == 1:
        return 1
    count = [0]

    def backtrack(curr_amount, num_coins, start):
        if num_coins == 0:
            if curr_amount == 0:
                count[0] += 1
            return

        for i in range(start, len(primes)):
            if curr_amount < primes[i]:
                break
            backtrack(curr_amount - primes[i], num_coins - 1, i)

    backtrack(amount, num_coins, 0)
    return count[0]


def coin_combinations_triple(amount, primes, min_coins, max_coins):
    # Calculate the number of ways to make the given amount using three different coin denominations
    count = [0]

    def backtrack(curr_amount, num_coins, start):
        if num_coins == 0:
            if curr_amount == 0:
                count[0] += 1
            return

        for i in range(start, len(primes)):
            if curr_amount < primes[i]:
                break
            backtrack(curr_amount - primes[i], num_coins - 1, i)

    for num_coins in range(min_coins, max_coins + 1):
        backtrack(amount, num_coins, 0)

    return count[0]


# Open input and output files
with open("input.txt", "r") as f, open("output.txt", "w") as output_file:
    # Set up the header line and line separator for the output file
    header_line = "{:<10s}|{:<10s}|{:<12s}\n".format("Input", "Output", "CPU Time")
    line_separator = "-" * 35

    # Write the header and line separator to the output file
    output_file.write(line_separator + "\n")
    output_file.write(header_line)
    output_file.write(line_separator + "\n")

    # Process each line in the input file
    for line in f:
        inputs = line.strip().split()
        amount = int(inputs[0])
        primes = generate_primes(amount)
        primes.insert(0, 1)

        if len(inputs) == 1:
            # Calculate the result and measure the CPU time for single coin combination
            start_time = time.process_time()
            result = coin_combinations_single(amount, primes)
            end_time = time.process_time()
        elif len(inputs) == 2:
            # Calculate the result and measure the CPU time for double coin combination
            start_time = time.process_time()
            num_coins = int(inputs[1])
            result = coin_combinations_double(amount, primes, num_coins)
            end_time = time.process_time()
        elif len(inputs) == 3:
            # Calculate the result and measure the CPU time for triple coin combination
            start_time = time.process_time()
            min_coins = int(inputs[1])
            max_coins = int(inputs[2])
            result = coin_combinations_triple(amount, primes, min_coins, max_coins)
            end_time = time.process_time()

        # Calculate the CPU time and format the output line
        cpu_time = end_time - start_time
        output_line = "{:<10s}|{:<10s}|{:<12.6f}\n".format(
            line.strip(), str(result), cpu_time
        )

        # Write the output line and line separator to the output file
        output_file.write(output_line)
        output_file.write(line_separator + "\n")
