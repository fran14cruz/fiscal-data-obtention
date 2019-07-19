"""
This script makes a POST request to verify a receipt in ОФД and storage to database.
"""
import requests

# API-endpoint
url_post = "https://localhost:8000"

# Data to be sent
data = {
    'fn': fn,
    'fd': fd,
    'fpd': fpd,
    'total_sum': total_sum,
    'ope_type': ope_type
}

# Send post request and save response as responde object
r = requests.post(url = url_post, data = data)

# Extract response text
pastebin_url = r.text
print("Pastebin url: {}".format(pastebin_url))