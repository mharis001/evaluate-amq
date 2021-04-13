from cuckoo_filters import *

DATASET_PATH = "usernames.txt"
DATA_TEST = 10000


def fpp_vs_load_cuckoo(size, load):
    test_counter = 0
    false_positives = 0
    cuckoo_filter = CuckooFilter(size, 1)

    with open(DATASET_PATH, "r") as file:
        for i, line in enumerate(file):
            username = line.rstrip('\n')

            if cuckoo_filter.load_factor() <= load:
                cuckoo_filter.insert(username)

            elif test_counter < DATA_TEST:
                test_counter += 1
                if cuckoo_filter.contains(username):
                    false_positives += 1
            else:
                break

    false_positive_rate = false_positives / DATA_TEST
    return false_positive_rate


def fpp_vs_load_cuckoo_test(size, load_lst):
    results = []
    for i in load_lst:
        false_positive_rate = fpp_vs_load_cuckoo(size, i)
        results.append((i, false_positive_rate))

    return results


def main():
    load_lst = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.96]
    results = fpp_vs_load_cuckoo_test(100000, load_lst)
    print(results)


if __name__ == "__main__":
    main()

