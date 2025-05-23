import sys
import argparse
from google import genai

from ._utils import AIChecksConfig

PROMPT = """

You are an expert assistant tasked with reviewing Python source code for grammatical correctness in docstrings, comments, and user-facing strings.

Instructions:
- Review the provided Python source code carefully.
- Identify grammar errors ONLY in comments, docstrings, and strings intended for user interaction or documentation.
- Do NOT suggest code logic or structural improvements; focus solely on English grammar and readability.
- If grammar errors are found, list each error clearly in the following structured format:
  - Line [line_number]: "Original incorrect text"
  - Correction: "Corrected grammatically accurate text"
  - Explanation: Briefly explain the grammatical issue.
- If no grammar errors are found, simply respond with:
  - No grammar errors found.

Begin the review now.
"""


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Grammar pre-commit hook")
    parser.add_argument(
        "files", nargs="*", help="List of files to check (provided by pre-commit)"
    )
    parser.add_argument(
        "--ignore-errors",
        action="store_true",
        help="Ignore errors and continue with the next file",
    )
    parser.add_argument(
        "--diff-only",
        action="store_true",
        help="Only check the diff of the files, not the entire file",
    )
    return parser.parse_args(argv)


def check_grammar(file_path: str, config: AIChecksConfig):
    print(f"Checking grammar for {file_path}")

    client = genai.Client(api_key=config.api_key)
    model = config.ai_model

    with open(file_path, "r") as f:
        contents = f.read()
        contents = f"{PROMPT}\n\n`{contents}`"

        response = client.models.generate_content(model=model, contents=contents)
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
