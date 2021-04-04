from bloom_filters import *

DATASET_PATH = "usernames.txt"
DATA_INSERT = 100000
DATA_TEST = DATA_INSERT * 2


def fpp_vs_hash_bloom(size, filter_size_ratio, hash_number):
    bloom_filter = BloomFilter(size*filter_size_ratio, hash_number)
    false_positives = 0

    with open(DATASET_PATH, "r") as file:
        for i, line in enumerate(file):
            username = line.rstrip('\n')

            if i < DATA_INSERT:
                bloom_filter.add(username)
            elif i < DATA_TEST:
                if bloom_filter.contains(username):
                    false_positives += 1
            else:
                break
    false_positive_rate = false_positives/(DATA_TEST - DATA_INSERT)
    return false_positive_rate


def fpp_vs_hash_bloom_test(data_size, filter_size_ratio, hash_number):
    fp_rate_list = []

    for i in range(1, hash_number+1):
        fp_rate = fpp_vs_hash_bloom(data_size, filter_size_ratio, i)
        fp_rate_list.append((i, fp_rate))

    return fp_rate_list


def main():
    lst = [1, 5, 10]
    for i in lst:
        print(fpp_vs_hash_bloom_test(100000, i, 10))


if __name__ == "__main__":
    main()
