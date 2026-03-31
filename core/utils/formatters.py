def parse_response(text):
    sections = {}
    current_key = None

    for line in text.split("\n"):
        if line.startswith("##"):
            current_key = line.replace("##", "").strip()
            sections[current_key] = ""
        elif current_key:
            sections[current_key] += line + "\n"

    return sections