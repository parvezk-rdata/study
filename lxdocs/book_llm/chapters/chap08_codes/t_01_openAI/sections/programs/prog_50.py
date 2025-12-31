from collections import Counter
import re

def remove_page_numbers(text):
    patterns = [ r"^Page\s+\d+$", r"^\d+$" ]
    cleaned_lines = []
    for line in text.splitlines():
        if not any(re.match(p, line.strip()) for p in patterns):
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def remove_repeated_lines(text, min_repeats=2):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    counts = Counter(lines)
    cleaned_lines = [ line for line in lines if counts[line] < min_repeats]
    return "\n".join(cleaned_lines)

def normalize_encoding(text):
    # Remove form-feed characters (common in PDFs)
    text = text.replace("\x0c", "")
    # Replace weird unicode artifacts
    text = text.replace("\uFFFD", "")
    return text

def normalize_whitespace(text):
    # Convert multiple spaces into single space
    text = re.sub(r"[ \t]+", " ", text)
    # Normalize multiple newlines
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    # Strip leading/trailing spaces
    text = text.strip()
    return text

def clean_text(raw_text):
    text = normalize_encoding(raw_text)
    text = remove_page_numbers(text)
    text = remove_repeated_lines(text)
    text = normalize_whitespace(text)
    return text