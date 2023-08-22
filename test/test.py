import re
import json

a = [
    "he",
    "try",
    "sth",
    "django",
]
json_string = json.dumps(a)
print(json_string)
# b = "QuanistryingtouseDjango "
# b = b.strip()
# b_lower = b.lower()
# list_item = b_lower.split(" ")
# print(b_lower)
# for item in a:
#     print(re.search(item, b_lower))
