import markdown_to_json
import sys

with open("./pr_body", "r") as file:
    text = file.read()
    d = markdown_to_json.dictify(text)
    for key, value in d.items():
        print(d[key], len(d[key]))
        if type(d[key]) is list:
            continue
        if d[key] == "":
            sys.exit("Not all RAP fields have been filled in.")

    print("All fields are filled!")
