import csv
import time
from typing import TextIO

from prettytable import PrettyTable

from amq import BloomFilter
from tests.basetest import BaseTest
from tests.testdata import USERNAMES_1M_FILE


BLOOM_TARGET_FPP = 0.01
BLOOM_BITS_PER_ELEMENT = BloomFilter.bits_per_item(BLOOM_TARGET_FPP)
BLOOM_FILTER_SIZE = int(BLOOM_BITS_PER_ELEMENT * 1_000_000)
BLOOM_HASH_FUNCTIONS_RANGE = [i for i in range(1, 21)]


class TestBloomHashPerformance(BaseTest):
    def __init__(self) -> None:
        self.name = "Bloom Filter - Number of Hash Functions vs Performance"

    def run(self) -> None:
        self.results = []

        with open(USERNAMES_1M_FILE, "r") as file:
            usernames = [l.rstrip('\n') for l in file.readlines()]

            usernames_insert = usernames[:750_000]
            usernames_lookup = usernames[250_000:]

            for k in BLOOM_HASH_FUNCTIONS_RANGE:
                bloom_filter = BloomFilter(BLOOM_FILTER_SIZE, k)

                start = time.process_time()

                for u in usernames_insert:
                    bloom_filter.insert(u)

                insert_time = time.process_time() - start

                start = time.process_time()

                for u in usernames_lookup:
                    u in bloom_filter

                lookup_time = time.process_time() - start

                self.results.append((k, insert_time, lookup_time))

    def info(self) -> str:
        info = """The time (in seconds) to insert 750,000 usernames into a Bloom filter and look up 750,000 usernames from the
filter (where 500,000 of the lookup usernames were inserted and 250,000 were not inserted) under a different
number of hash functions using the optimal number of bits per element for a target false positive probability of 1%.\n"""

        table = PrettyTable()
        table.field_names = ["Hash Functions",
                             "Insert Time (s)", "Lookup Time (s)"]

        for k, ti, tl in self.results:
            table.add_row([k, f"{ti:f}", f"{tl:f}"])

        return info + table.get_string()

    def export_csv(self, file: TextIO) -> None:
        writer = csv.writer(file)
        writer.writerow(["k", "ti", "tl"])

        for k, ti, tl in self.results:
            writer.writerow([k, f"{ti:f}", f"{tl:f}"])
