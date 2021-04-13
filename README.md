# evaluate-amq

CS4411 Project: Evaluating the Performance of Approximate Membership Queries

## Requirements

- Python 3.6+

## Usage

1. Create and activate a virtual environment using [`virtualenv`](https://pypi.org/project/virtualenv/).
2. Install the necessary requirements using `pip install -r requirements.txt`.
3. Run the using `python main.py`.
    - Some tests are not provided in this command line interface due to special requirements. They are included in the `amq` package and must be run manually.

The following commands will perform all of the above:

```sh
# Create environments directory
mkdir venv

# Create virtual environment
virtualenv venv/

# Activate virtual environment (may differ for Windows)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the test CLI (some tests are not included in this tool)
python main.py
```

## Data Files

Several data files are included in `tests/data/`:

- 5x 1M, 1x 5M, 1x 10 Reddit Username in text files (one per line)
- `sqlite` database containing 10M Reddit usernames in table `users` with clustered index on undername field

## Credits

- CS4411 Project Team 4
