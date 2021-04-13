# CS4411 Project Team 4
# Evaluating the Performance of Approximate Membership Queries

import math
import mmh3

from BitVector import BitVector

from amq.basefilter import BaseFilter
from amq.filteritem import FilterItem


class BloomFilter(BaseFilter):
    """A simple Bloom filter using the MurmurHash3 function."""

    def __init__(self, m: int, k: int) -> None:
        # Exit if invalid m or k values are provided
        if m < 1 or k < 1:
            raise ValueError("ERROR: m and k should be greater than 0.")

        # Number of bits in the array
        self.m = m

        # Number of hash functions
        self.k = k

        # Number of items in the filter
        self.n = 0

        # Initialize a bit array to the size of the filter
        self.bit_array = BitVector(size=self.m)

    def insert(self, item: FilterItem) -> None:
        """Inserts the given item into the Bloom filter."""

        # Set the bits that correspond to this item to 1
        # Using i as the seed for mmh3 ensures independent hash functions
        for i in range(self.k):
            self.bit_array[mmh3.hash(item, i) % self.m] = 1

        self.n += 1

    def delete(self, item: FilterItem) -> None:
        """Unsupported operation. Bloom filter does not support deleting items."""

        pass

    def clear(self) -> None:
        """Clears the Bloom filter by reinitializing the bit array."""

        self.n = 0
        self.bit_array = BitVector(size=self.m)

    def __contains__(self, item: FilterItem) -> bool:
        """Checks if the given item exists in the Bloom filter."""

        # If any bit is not set, then the item is not in the filter
        for i in range(self.k):
            if self.bit_array[mmh3.hash(item, i) % self.m] != 1:
                return False

        # Otherwise, the item might exist in the filter
        return True

    def __len__(self) -> int:
        """Returns the number of elements inserted into the Bloom filter."""

        return self.n

    def __repr__(self) -> str:
        """Returns a string representation of the Bloom filter."""

        return f"<Bloom Filter: m={self.m,}, k={self.k,}, n={self.n,}>"

    @staticmethod
    def bits_per_item(p: float) -> float:
        """Returns the optimal bits per item for the given false positive probability."""

        return -(math.log2(p) / math.log(2))

    @staticmethod
    def k_hash_functions(p: float) -> int:
        """Returns the optimal number of hash functions for the given false positive probability."""

        return -math.log2(p)

    @classmethod
    def from_target_fpp(cls, n: int, p: float):
        return cls(int(n * BloomFilter.bits_per_item(p)), math.ceil(BloomFilter.k_hash_functions(0.01)))
