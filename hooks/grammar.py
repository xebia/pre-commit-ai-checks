import sys
import argparse
import subprocess
from google import genai

from ._utils import AIChecksConfig

PROMPT = """

You are an expert assistant tasked with reviewing Python source code for grammatical correctness in docstrings, comments, and user-facing strings.

Instructions:
- Review the provided Python source code carefully.
- Identify grammar errors ONLY in comments, docstrings, and strings intended for user interaction or documentation.
- Do NOT suggest code logic or structural improvements; focus solely on English grammar and readability.
- Ignore grammatical correctness of ending dots.
- The result MUST be ONLY a list of errors if there are any, or an empty list if there are no errors.
- If grammar errors are found, list each error clearly in the following structured format:
  - Line [line_number]: "Original incorrect text"
  - Correction: "Corrected grammatically accurate text"
  - Explanation: Briefly explain the grammatical issue.
- If no grammar errors are found, simply respond with:
  - No grammar errors found.
- If an empty file is given, simply respond with `No grammar errors found`.
- DO NOT include any other text or example in the response!

FOLLOW THE INSTRUCTIONS STRICTLY!
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


def get_git_diff(file_path: str):
    try:
        diff = subprocess.check_output(
            ["git", "diff", "--staged", file_path],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        return diff
    except subprocess.CalledProcessError:
        return None


def check_grammar(file_path: str, config: AIChecksConfig, diff_only: bool = False):
    print(f"🔍 Checking grammar for {file_path}")

    client = genai.Client(api_key=config.api_key)
    model = config.ai_model

    if diff_only:
        diff = get_git_diff(file_path)
        if not diff:
            return "No grammar errors found"

        request = f"{PROMPT}\n\n`{diff}`"
    else:
        with open(file_path, "r") as f:
            content = f.read()
            if not content:
                return "No grammar errors found"

            request = f"{PROMPT}\n\n`{content}`"
    response = client.models.generate_content(model=model, contents=request)
    return response.text


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)
    config = AIChecksConfig()

    if not args.files:
        print("📝 No files to check.")
        return 0

    print(f"config: {config}")
    errors_found = 0
    for f in args.files:
        response = check_grammar(f, config, args.diff_only)
        if response and response.startswith("No grammar errors found"):
            print(f"  ✅ No grammar errors found in {f}")
        else:
            print(f"  ❌ Grammar errors found in {f}")
            print(response)
            errors_found += 1

    if args.ignore_errors:
        return 0
    return errors_found


if __name__ == "__main__":
    sys.exit(main())
