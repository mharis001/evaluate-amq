import os

# Base path for the data folder
DATA_FILES_BASEPATH = os.path.join(os.path.dirname(__file__), "data/")

USERNAMES_1M_FILE = os.path.join(DATA_FILES_BASEPATH, "usernames-1m.txt")
USERNAMES_5M_FILE = os.path.join(DATA_FILES_BASEPATH, "usernames-5m.txt")
USERNAMES_10M_FILE = os.path.join(DATA_FILES_BASEPATH, "usernames-10m.txt")
USERNAMES_10M_DB = os.path.join(DATA_FILES_BASEPATH, "usernames-10m.db")
