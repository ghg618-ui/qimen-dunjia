import fitz # PyMuPDF
import glob
import json

res = {}
for filename in glob.glob("/Users/gonghg/Downloads/奇门遁甲 project/奇门象意-*.pdf"):
    try:
        doc = fitz.open(filename)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        res[filename.split('/')[-1]] = text
    except Exception as e:
        res[filename.split('/')[-1]] = f"Error: {str(e)}"

with open('pdf_content.json', 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
