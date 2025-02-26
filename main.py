import markdown_to_json
from jira import JIRA
import sys
import os
import re

# Replace with your Jira URL, email, and API token
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_TOKEN")

def check_list(l):
    list_item_chosen = False
    marked_choices = []
    for item in l:
        m = re.search("\[x\]\\s*([a-zA-Z ]*)", item)
        if m:
            list_item_chosen = True
            marked_choices.append(m.group(1))
    return list_item_chosen, list(map(lambda c: {"value": c}, marked_choices))

file = open("./pr_body", "r")
text = file.read()
file.close()

d = markdown_to_json.dictify(text)
for key, value in d.items():
    print(key, value)
    if type(d[key]) is list:
        marked, value = check_list(d[key])
        value = value[0] if len(value) == 1 else value
        if marked:
            d[key] = value
        else:
            sys.exit(f"Field '{key}' not marked")
    if d[key] == "":
        sys.exit("Not all RAP fields have been filled in.")

rap_field_ids_by_names = {
    'Target Release Date': 'customfield_13622',
#    'Release Type': 'customfield_13231',
    'Business Justification': 'customfield_12731', 
    'Description of Resolution': 'customfield_13725', 
    'What testing did you do? Provide a link to results.': 'customfield_13626',
    'What could this change break outside your team?': 'customfield_13628',
    'What is the risk and complexity of this change?': 'customfield_13629',
    'Is your change backwardly compatible? If not, please ensure you have aligned with your Eng VP and provide rollback/reversion strategy below': 'customfield_15398',
    'What is the roll back and/or reversion strategy for this change?': 'customfield_13630',
    'Do you have Engineering, Product and QA lead sign off that all changes are verified?': 'customfield_13640',
    'Is the team prepared to verify the deployment when it goes live?': 'customfield_13631'
}

# Create a Jira instance
jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, API_TOKEN))

ticket_fields = {
    "project": {
        "key": "RAP"
    },
    "summary": "TEST",
    "issuetype": {
        "name": "Hotfix Request"
    }
}

custom_fields_dict = {rap_field_ids_by_names[key]: d[key] for key, _ in rap_field_ids_by_names.items()}
ticket_fields.update(custom_fields_dict)

print(ticket_fields)

# Get the issue
issue = jira.create_issue(fields=ticket_fields)
