import sys
import argparse
from google import genai

from ._utils import AIChecksConfig


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Grammar pre-commit hook")
    parser.add_argument(
        "files", nargs="*", help="List of files to check (provided by pre-commit)"
    )
    parser.add_argument(
        "--ignore-errors",
        action="store_false",
        help="Ignore errors and continue with the next file",
    )
    return parser.parse_args(argv)


def check_grammar(file_path: str, config: AIChecksConfig):
    print(f"Checking grammar for {file_path}")

    client = genai.Client(api_key=config.api_key)
    model = config.ai_model

    response = client.models.generate_content(
        model=model, contents="Explain how AI works in a few words"
    )
    print(response.text)


def main(argv=None):
    print("Running grammar hook")
    print(f"argv: {argv}")

    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)
    config = AIChecksConfig()

    if not args.files:
        print("No files to check.")
        return 0

    print(f"args: {args}")
    print(f"config: {config}")

    print(f"Running custom logic on {len(args.files)} file(s):")
    for f in args.files:
        print(f" - {f}")
        check_grammar(f, config)

    # TODO: insert actual check logic here
    # Example: for each file, open and analyze contents

    # Always succeed by default
    return 0


if __name__ == "__main__":
    sys.exit(main())
