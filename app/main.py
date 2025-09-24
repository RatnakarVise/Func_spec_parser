import re
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FDD Dynamic Parser API")

# -------------------------------
# Parser function
# -------------------------------
def parse_fdd_dynamic(fdd_text: str) -> Dict[str, str]:
    """
    Parse FDD text into sections dynamically based on numbered or unnumbered headings.
    Captures headings like:
      1. Purpose
      2. Scope
      Reports & Outputs
    Returns dict {heading: content}
    """
    # Regex: match numbered headings (e.g., "1. Purpose") or lines with title-like text
    pattern = re.compile(r"^(?:\d+\.\s*)?([A-Z][A-Za-z &]+)$", re.MULTILINE)

    # Find all headings with their positions
    matches = list(pattern.finditer(fdd_text))

    result = {}
    for i, match in enumerate(matches):
        header = match.group(1).strip()
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(fdd_text)
        content = fdd_text[start:end].strip()
        result[header] = content

    return result

# -------------------------------
# API Model
# -------------------------------
class FDDInput(BaseModel):
    fdd: str

# -------------------------------
# API Endpoint
# -------------------------------
@app.post("/parse_fdd")
async def parse_fdd_endpoint(input_data: FDDInput):
    parsed = parse_fdd_dynamic(input_data.fdd)
    return parsed
