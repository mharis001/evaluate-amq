import csv
import sqlite3
import time
from typing import TextIO

from prettytable import PrettyTable

from amq import BloomFilter

from tests.basetest import BaseTest
from tests.testdata import USERNAMES_10M_FILE, USERNAMES_10M_DB


BLOOM_TARGET_FPP = 0.01
TEST_ENTRIES_RANGE = [int(100_000 * i) for i in range(1, 11)]


class TestBloomMembershipEMQ(BaseTest):
    def __init__(self) -> None:
        self.name = "Bloom Filter - Membership Test vs EMQ (sqlite query)"

    def run(self) -> None:
        # Prepare bloom filter
        bloom_filter = BloomFilter.from_target_fpp(
            10_000_000, BLOOM_TARGET_FPP)

        with open(USERNAMES_10M_FILE, "r") as file:
            for line in file:
                username = line.rstrip("\n")
                bloom_filter.insert(username)

        # Measure performance of sqlite database
        query_results = []

        with open(USERNAMES_10M_FILE, "r") as file:
            for n in TEST_ENTRIES_RANGE:
                connection = sqlite3.connect(USERNAMES_10M_DB)

                start = time.process_time()

                for i, line in enumerate(file):
                    username = line.rstrip("\n")

                    connection.execute(
                        "SELECT EXISTS(SELECT 1 FROM users WHERE username=?)", (username,))

                    if i >= n:
                        break

                query_results.append(time.process_time() - start)

                connection.commit()
                connection.close()

        # Measure performance of bloom filter
        bloom_results = []

        with open(USERNAMES_10M_FILE, "r") as file:
            for n in TEST_ENTRIES_RANGE:
                start = time.process_time()

                for i, line in enumerate(file):
                    username = line.rstrip("\n")

                    username in bloom_filter

                    if i >= n:
                        break

                bloom_results.append(time.process_time() - start)

        self.results = list(
            zip(TEST_ENTRIES_RANGE, bloom_results, query_results))

    def info(self) -> str:
        info = """The time (in seconds) to look up usernames using a Bloom filter and a sqlite database
that both contain 10,000,000 usernames. The Bloom filter was set up for a target false positive
probability of 0.01 and the sqlite database used a clustered index."""

        table = PrettyTable()
        table.field_names = ["Number of Lookups",
                             "Bloom Filter Time (s)", "Sqlite Query Time (s)"]

        for n, tb, ts in self.results:
            table.add_row([n, f"{tb:f}", f"{ts:f}"])

        return info + table.get_string()

    def export_csv(self, file: TextIO) -> None:
        writer = csv.writer(file)
        writer.writerow(["n", "bloom", "query"])

        for n, tb, ts in self.results:
            writer.writerow([n, f"{tb:f}", f"{ts:f}"])
