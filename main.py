#!/usr/bin/env python3
"""Entry for u-xvader-the-most-boring-object-reviewed-in-one-line-bd3117c3.

A single line (<= 200 characters) reviewing the most boring everyday
object. The joke must come from how the object really behaves.

Chosen object: a rubber band. Its real behaviour is the joke: it sits
unused in a drawer for years, then snaps the one time it is needed.
"""

from __future__ import annotations

import sys

# The entry text. One line, 122 characters, well under the 200 limit.
ENTRY_TEXT = (
    "My rubber band snapped the one time I actually needed it, "
    "after spending three years doing absolutely nothing in a drawer."
)

# Competition limits from the brief.
MAX_CHARS = 200
MIN_CHARS = 1

# The boring everyday object this review is about.
OBJECT_KEYWORDS = ("rubber band",)

# Fallback text, used only if the primary text ever fails validation.
# It is itself a valid one-line review of the same object, so the
# program can still produce a compliant entry instead of crashing.
FALLBACK_TEXT = (
    "My rubber band spent three years in a drawer doing nothing, "
    "then snapped the moment I finally needed it."
)


def count_characters(text: str) -> int:
    """Return the character count of *text*, exactly as the brief counts it."""
    return len(text)


def is_single_line(text: str) -> bool:
    """True when *text* contains no line breaks of any kind."""
    return "\n" not in text and "\r" not in text


def mentions_object(text: str) -> bool:
    """True when *text* names the boring object being reviewed."""
    lowered = text.lower()
    return any(keyword in lowered for keyword in OBJECT_KEYWORDS)


def has_clean_spacing(text: str) -> bool:
    """True when *text* has no doubled spaces or stray tab characters."""
    return "  " not in text and "\t" not in text


def has_real_behaviour_joke(text: str) -> bool:
    """Check the joke is grounded in how the object really behaves.

    A rubber band really does sit idle for years and really does snap
    under tension when finally stretched. The entry must mention both
    the idle waiting and the snapping, otherwise the joke is generic.
    """
    lowered = text.lower()
    idle = any(word in lowered for word in ("drawer", "doing nothing", "years"))
    snaps = "snapped" in lowered
    needed = "needed it" in lowered
    return idle and snaps and needed


def validate_entry(text: str) -> list[str]:
    """Validate *text* against every rule in the brief.

    Returns a list of problems; an empty list means the text is valid.
    """
    problems: list[str] = []

    if not isinstance(text, str):
        problems.append("entry must be a string")
        return problems

    if not text.strip():
        problems.append("entry must not be empty")
        return problems

    if text != text.strip():
        problems.append("entry must not have leading or trailing whitespace")

    if not is_single_line(text):
        problems.append("entry must be a single line")

    if not has_clean_spacing(text):
        problems.append("entry must not contain doubled spaces or tabs")

    length = count_characters(text)
    if length < MIN_CHARS:
        problems.append("entry is empty")
    if length > MAX_CHARS:
        problems.append(
            f"entry is {length} characters, over the {MAX_CHARS} limit"
        )

    if not mentions_object(text):
        problems.append("entry must name the boring object it reviews")

    if not has_real_behaviour_joke(text):
        problems.append(
            "joke must come from how the object really behaves"
        )

    return problems


def choose_entry() -> str:
    """Return the entry text, falling back if the primary text is invalid."""
    problems = validate_entry(ENTRY_TEXT)
    if not problems:
        return ENTRY_TEXT
    fallback_problems = validate_entry(FALLBACK_TEXT)
    if not fallback_problems:
        return FALLBACK_TEXT
    # Both texts failed: report every problem and refuse to emit
    # a non-compliant entry rather than printing something invalid.
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    raise SystemExit(1)


def verify_output(output: str) -> None:
    """Verify the exact bytes that will go to stdout before printing."""
    # print() adds one trailing newline; strip exactly that one back
    # so the check compares the entry text itself, not the newline.
    body = output[:-1] if output.endswith("\n") else output
    problems = validate_entry(body)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    """Print exactly the entry text to stdout and nothing else."""
    entry = choose_entry()
    # Final guard: never emit more than the entry plus one newline.
    if len(entry) > MAX_CHARS:
        print("error: entry exceeds the character limit", file=sys.stderr)
        return 1
    output = entry + "\n"
    verify_output(output)
    sys.stdout.write(output)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
