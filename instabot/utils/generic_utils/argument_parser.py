import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-u", type=str, help="username")
    parser.add_argument("-p", type=str, help="password")
    args = parser.parse_args()
    return args.u, args.p
