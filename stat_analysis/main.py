import argparse
from stat_analysis.datasets import csv_dataset
def main(args):
    """
    Main entry point for the program
    :param args: String of command line arguments, excluding program name
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args(args)
    print(args.file)

    d = csv_dataset.CSVDataset(args.file)

    for x in d:
        print(x)

    return True