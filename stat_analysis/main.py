import argparse

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
    return True