import csv
import math
from typing import TextIO

from prettytable import PrettyTable

from amq import BloomFilter
from tests.basetest import BaseTest
from tests.testdata import USERNAMES_1M_FILE, USERNAMES_5M_FILE


BLOOM_TARGET_FPP = 0.01
BLOOM_HASH_FUNCTIONS = math.ceil(
    BloomFilter.k_hash_functions(BLOOM_TARGET_FPP))
BLOOM_BITS_PER_ELEMENT_RANGE = [i for i in range(1, 31)]


class TestBloomBitsPerElement(BaseTest):
    def __init__(self) -> None:
        self.name = "Bloom Filter - Bits per Element vs FPP"

    def run(self) -> None:
        self.results = []

        for bpe in BLOOM_BITS_PER_ELEMENT_RANGE:
            bloom_filter = BloomFilter(bpe * 5_000_000, BLOOM_HASH_FUNCTIONS)

            with open(USERNAMES_5M_FILE, "r") as file:
                for line in file:
                    username = line.rstrip("\n")
                    bloom_filter.insert(username)

            false_positives = 0

            with open(USERNAMES_1M_FILE, "r") as file:
                for line in file:
                    username = line.rstrip("\n")

                    if username in bloom_filter:
                        false_positives += 1

            self.results.append((bpe, false_positives / 1_000_000))

    def info(self) -> str:
        info = """The false positive rate of Bloom filters under various bits per element values.
For each bits per element value, 5,000,000 usernames were inserted into an empty filter and
1,000,000 uninserted usernames were checked to calculate the false positive rate.
Each filter used an optimal number of hash functions for a false positive probability of 1%.\n"""

        table = PrettyTable()
        table.field_names = ["Bits per Element", "False Positive Rate"]

        for bpe, fpp in self.results:
            table.add_row([bpe, f"{fpp:.4%}"])

        return info + table.get_string()

    def export_csv(self, file: TextIO) -> None:
        writer = csv.writer(file)
        writer.writerow(["bpe", "fpp"])

        for bpe, fpp in self.results:
            writer.writerow([bpe, f"{fpp:f}"])
