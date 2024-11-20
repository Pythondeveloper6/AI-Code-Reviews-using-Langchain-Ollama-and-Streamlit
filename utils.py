import re

def extract_code_quality_score(result):
    # Use regex to match "Code Quality Score: X/10"
    match = re.search(r"Code Quality Score:\s*(\d+)/10", result)
    if match:
        # Extract the score as an integer
        return int(match.group(1))
    return None