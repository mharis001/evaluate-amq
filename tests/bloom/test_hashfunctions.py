import csv
from typing import TextIO

from prettytable import PrettyTable

from amq import BloomFilter
from tests.basetest import BaseTest
from tests.testdata import USERNAMES_1M_FILE, USERNAMES_5M_FILE


BLOOM_TARGET_FPP = 0.01
BLOOM_BITS_PER_ELEMENT = BloomFilter.bits_per_item(BLOOM_TARGET_FPP)
BLOOM_FILTER_SIZE = int(BLOOM_BITS_PER_ELEMENT * 1_000_000)
BLOOM_HASH_FUNCTIONS_RANGE = [i for i in range(1, 21)]


class TestBloomHashFunctions(BaseTest):
    def __init__(self) -> None:
        self.name = "Bloom Filter - Number of Hash Functions vs FPP"

    def run(self) -> None:
        bloom_filters = [BloomFilter(BLOOM_FILTER_SIZE, k)
                         for k in BLOOM_HASH_FUNCTIONS_RANGE]

        with open(USERNAMES_1M_FILE, "r") as file:
            for line in file:
                username = line.rstrip("\n")

                for f in bloom_filters:
                    f.insert(username)

        false_positives = [0] * len(bloom_filters)

        with open(USERNAMES_5M_FILE, "r") as file:
            for i, line in enumerate(file):
                username = line.rstrip("\n")

                for j, f in enumerate(bloom_filters):
                    if username in f:
                        false_positives[j] += 1

                if i >= 100_000:
                    break

        self.results = [(k, fp / 100_000)
                        for k, fp in enumerate(false_positives, 1)]

    def info(self) -> str:
        info = """The false positive rate of Bloom filters under a different number of hash functions.
For each hash functions value, 1,000,000 usernames were inserted into an empty filter and
100,000 uninserted usernames were checked to calculate the false positive rate.
Each filter used an optimal number of bits per element for a false positive probability of 1%.\n"""

        table = PrettyTable()
        table.field_names = ["Hash Functions", "False Positive Rate"]

        for k, fpp in self.results:
            table.add_row([k, f"{fpp:.4%}"])

        return info + table.get_string()

    def export_csv(self, file: TextIO) -> None:
        writer = csv.writer(file)
        writer.writerow(["k", "fpp"])

        for k, fpp in self.results:
            writer.writerow([k, f"{fpp:f}"])
