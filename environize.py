"""Convert a Spring .properties file to an .env file"""
import re
from argparse import ArgumentParser
from os import getcwd
from pathlib import Path

pattern = re.compile("(.*?)=(.*)")


def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="File to process")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    output = args.output
    if not output:
        output = (Path(getcwd()) / Path(args.file).name).with_suffix(".env")

    with open(args.file, "r", encoding="utf-8") as file_fd:
        with open(output, "w", encoding="utf-8") as env_fd:
            for line in file_fd.readlines():
                search = pattern.search(line)
                key = search.group(1)

                key = key.replace(".", "_").replace("-", "").upper()
                value = search.group(2)
                env_fd.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
