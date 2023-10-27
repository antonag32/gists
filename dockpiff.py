"""Obtain a unified diff of the pip packages between two docker images"""

from argparse import ArgumentParser, BooleanOptionalAction
from difflib import unified_diff
from subprocess import run
from sys import stdout

DOCKER_EXEC = ["docker", "run", "--rm", "--entrypoint", "pip"]


def get_pkgs(img_id: str) -> list[str]:
    return (
        run(DOCKER_EXEC + [img_id, "freeze"], capture_output=True, check=True).stdout.decode("utf-8").splitlines(True)
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("image1", type=str)
    parser.add_argument("image2", type=str)
    parser.add_argument("-v", "--verbose", help="Display containers' packages", action=BooleanOptionalAction)
    args = parser.parse_args()

    pkgs1 = get_pkgs(args.image1)
    if args.verbose:
        print(f"Packages for {args.image1}")
        stdout.writelines(pkgs1)

    pkgs2 = get_pkgs(args.image2)
    if args.verbose:
        print(f"Packages for {args.image2}")
        stdout.writelines(pkgs2)

    print("pip package diff")
    stdout.writelines(unified_diff(pkgs1, pkgs2, args.image1, args.image2))


if __name__ == "__main__":
    main()
