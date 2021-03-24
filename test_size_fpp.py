import amq
import os

###### GLOBALS ######
DATA_INSERT = 100_000
DATA_TEST = 110_000

BLOOM_BITS = 3_200_000
BLOOM_HASHES = 5
#####################

bloom_filter = amq.BloomFilter(BLOOM_BITS, BLOOM_HASHES)
false_positives = 0

with open("data/usernames.txt", "r") as file:
    for i, line in enumerate(file):
        username = line.rstrip('\n')

        if i < DATA_INSERT:
            bloom_filter.add(username)
        elif i < DATA_TEST:
            if bloom_filter.contains(username):
                false_positives += 1
        else:
            break

    print(
        "TEST: Filter Size vs False Positive Percentage\n"
        f"Inserted {DATA_INSERT:,} usernames into Bloom Filter with {BLOOM_BITS:,} bits.\n"
        f"Checked for {DATA_TEST - DATA_INSERT:,} nonexistent usernames.\n"
        f"False Positives: {false_positives:,} / {DATA_TEST - DATA_INSERT:,}\n"
        f"                 {round((false_positives / (DATA_TEST - DATA_INSERT)) * 100, 2)}%"
    )
