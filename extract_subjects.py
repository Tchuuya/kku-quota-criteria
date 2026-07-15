import json

def main():
    try:
        with open("kku_quota_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("kku_quota_data.json not found")
        return

    subjects = {}
    for item in data:
        criteria = item.get("criteria", [])
        for c in criteria:
            code = c.get("code")
            name = c.get("name")
            if code and name:
                subjects[code] = name

    # Sort by code
    sorted_subjects = {k: subjects[k] for k in sorted(subjects.keys())}

    with open("subjects.json", "w", encoding="utf-8") as f:
        json.dump(sorted_subjects, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(sorted_subjects)} unique subjects to subjects.json")
    for code, name in sorted_subjects.items():
        print(f"{code}: {name}")

if __name__ == "__main__":
    main()
