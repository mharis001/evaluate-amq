from cuckoo_filters import CuckooFilter

###### GLOBALS ######
DATA_INSERT = 100000
DATA_TEST = DATA_INSERT * 10
#####################


def fpp_vs_fingerprint_cuckoo (filter_size, fingerprint_size):
    cuckoo_filter = CuckooFilter(filter_size, fingerprint_size)
    false_positives = 0

    with open("usernames.txt", "r") as file:
        for j, line in enumerate(file):
            username = line.rstrip('\n')

            if j < DATA_INSERT:
                cuckoo_filter.insert(username)
            elif j < DATA_TEST:
                if cuckoo_filter.contains(username):
                    false_positives += 1
            else:
                break

    false_positive_rate = float(false_positives/(DATA_TEST - DATA_INSERT))
    return false_positive_rate


def fpp_vs_fingerprint_cuckoo_test(filter_size, fingerprint_size_lst):
    results = []
    for i in fingerprint_size_lst:
        results.append(fpp_vs_fingerprint_cuckoo(filter_size, i))

    return results


def main():
    fingerprint_size_lst = [1, 2, 3, 4, 5]
    print(fpp_vs_fingerprint_cuckoo_test(26000, fingerprint_size_lst))


if __name__ == "__main__":
    main()
