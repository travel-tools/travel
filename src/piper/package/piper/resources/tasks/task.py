import argparse


def main(context, task):

    print(f"{task} is OK! Running in {context}")


if __name__ == '__main__':

    # Parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--context")
    parser.add_argument("--task")
    args = parser.parse_args()

    main(args.context, args.task)
