import argparse
import logging
from stat_analysis.datasets import csv_dataset

logger = logging.getLogger(__name__)
def main(cl_args):
    """
    Main entry point for the program
    :param args: String of command line arguments, excluding program name
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("col_names")
    args = parser.parse_args(cl_args)
    logger.info("Data set file name: {}".format(args.file))

    d = csv_dataset.CSVDataset(args.file,args.col_names)


    return True