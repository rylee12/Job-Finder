from urllib.parse import urlencode

"""Testing the feasibility of allowing user input"""

#val = input("Which city?: ")
#val2 = input("Hi: ")
val = 0
val2 = 0

test_dict = {
    "p": val,
    "radius": val2
}

test_d2 = {}
test_d2["p"] = val
test_d2["rad"] = val2

# geoId: I or L?
query_param = {
    "geoId": "",
    "keywords": "computer science internship",
    "location": "San Francisco, CA"
}

encoded_query = urlencode(query_param)
print("encoded")
print(encoded_query)
linked_query = f"https://www.linkedin.com/jobs/search/?{encoded_query}"

print(linked_query)

#print(test_dict)
#print(test_d2)
#print(query_param)
