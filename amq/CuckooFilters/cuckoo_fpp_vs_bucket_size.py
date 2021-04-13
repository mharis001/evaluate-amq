from cuckoo_filters import *

DATASET_PATH = "usernames.txt"
DATA_INSERT = 40000
DATA_TEST = DATA_INSERT * 10


def fpp_vs_bucket_size_cuckoo(size, bucket_size):
    buckets = int(size/bucket_size)
    cuckoo_filter = CuckooFilter(buckets, 1, bucket_size)
    false_positives = 0

    with open(DATASET_PATH, "r") as file:
        for i, line in enumerate(file):
            username = line.rstrip('\n')

            if i < DATA_INSERT:
                cuckoo_filter.insert(username)
            elif i < DATA_TEST:
                if cuckoo_filter.contains(username):
                    false_positives += 1
            else:
                break

    false_positive_rate = false_positives/(DATA_TEST - DATA_INSERT)
    return false_positive_rate


def fpp_vs_bucket_size_cuckoo_test(size, bucket_size_lst):
    results = []
    for i in bucket_size_lst:
        results.append(fpp_vs_bucket_size_cuckoo(size, i))

    return results


def main():
    bucket_size_lst = [1, 2, 3, 4, 5, 6, 7]
    print(fpp_vs_bucket_size_cuckoo_test(100000, bucket_size_lst))


if __name__ == "__main__":
    main()
