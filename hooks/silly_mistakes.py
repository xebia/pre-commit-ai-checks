import sys
import argparse


def main(argv=None):
    print("Running silly-mistakes hook")
    print(f"argv: {argv}")

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Custom pre-commit hook")
    parser.add_argument(
        "files", nargs="*", help="List of files to check (provided by pre-commit)"
    )
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Exit with non-zero status if any warnings are emitted",
    )
    args = parser.parse_args(argv)

    if not args.files:
        print("No files to check.")
        return 0

    print(f"args: {args}")

    print(f"Running custom logic on {len(args.files)} file(s):")
    for f in args.files:
        print(f" - {f}")

    # TODO: insert actual check logic here
    # Example: for each file, open and analyze contents

    # Always succeed by default
    return 0


if __name__ == "__main__":
    sys.exit(main())
