import json
import re

def load_template(template_name="developer"):
    with open(f"templates/{template_name}_template.json", "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_cv(text, template):
    findings = {
        "missing_sections": [],
        "weak_phrases": [],
        "recommended_keywords": [],
    }

    lower_text = text.lower()

    # 1. Eksik bölümler (eşanlamlı listesi ile)
    for section, synonyms in template.get("required_sections", {}).items():
        found = False
        for syn in synonyms:
            if syn.lower() in lower_text:
                found = True
                break
        if not found:
            findings["missing_sections"].append(section)

    # 2. Zayıf ifadeler (regex ile tam kelime eşleşmesi)
    for phrase in template.get("bad_phrases", []):
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        if re.search(pattern, lower_text):
            findings["weak_phrases"].append(phrase)

    # 3. Anahtar kelimeler
    for keyword in template.get("keywords", []):
        pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
        if not re.search(pattern, lower_text):
            findings["recommended_keywords"].append(keyword)

    return findings
