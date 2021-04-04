from cuckoo_filters import *

DATASET_PATH = "usernames.txt"
DATA_INSERT = 100000
DATA_TEST = DATA_INSERT * 10


def fpp_vs_size_cuckoo(size, scale):
    false_positives = 0
    cuckoo_filter = CuckooFilter(int(size*scale), 1)

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

    false_positive_rate = false_positives / (DATA_TEST - DATA_INSERT)
    return false_positive_rate


def fpp_vs_size_cuckoo_test(size, scale_lst):
    results = []
    for i in scale_lst:
        false_positive_rate = fpp_vs_size_cuckoo(size, i)
        results.append((size*i, false_positive_rate))

    return results


def main():
    scale_lst = [0.26, 0.5, 1, 2, 5, 10, 100]
    print(fpp_vs_size_cuckoo_test(100000, scale_lst))


if __name__ == "__main__":
    main()