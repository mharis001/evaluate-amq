import os
import sys

from PyInquirer import prompt
from yaspin import yaspin

from tests.bloom import TestBloomBitsPerElement, TestBloomHashFunctions, TestBloomHashPerformance, TestBloomMembershipEMQ


def main():
    # Print title message
    print(
        "Evaluating the Performance of Approximate Membership Queries\n"
        "------------------------------------------------------------"
    )

    # Add available tests here
    tests = [
        TestBloomBitsPerElement(),
        TestBloomHashFunctions(),
        TestBloomHashPerformance(),
        TestBloomMembershipEMQ()
    ]

    # Prompt the user for the test to run and file to save results to
    questions = [
        {
            "type": "list",
            "name": "test",
            "message": "Which test would you like to run?",
            "choices": [{"name": t.name, "value": t} for t in tests]
        },
        {
            "type": "input",
            "name": "csv",
            "message": "Would you like to save the results to a .csv file? (enter file name)",
            "filter": lambda v: v if not v or v.endswith(".csv") else f"{v}.csv"
        }
    ]

    answers = prompt(questions)

    if not answers:
        return

    # Get the user's answers
    test = answers["test"]
    csv_filename = answers["csv"]

    # Create a spinner with a timer and run the test
    with yaspin(text="Running test...", color="yellow", timer=True) as spinner:
        try:
            test.run()
            spinner.ok()
        except:
            spinner.fail()
            raise

    # Print the results
    print("------------------------------------------------------------")
    print(test.info())

    # Export to a csv file if needed
    if csv_filename:
        csv_filepath = os.path.join("export/", csv_filename)

        os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)

        with open(csv_filepath, "w", newline="") as csv_file:
            test.export_csv(csv_file)

        print(f"Exported results to {csv_filepath}")


if __name__ == "__main__":
    sys.exit(main())
