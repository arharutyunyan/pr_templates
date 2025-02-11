import markdown_to_json

with open("./pr_body", "r") as file:
    text = file.read()
    d = markdown_to_json.dictify(text)
    print(d["Business Justification"])
    print(d["What testing did you do? Provide a link to results."])
    print(d["Does this have model changes?"])
