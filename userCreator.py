#!/usr/bin/python3
import requests
import json
import csv
import logging
from requests.auth import HTTPBasicAuth
from faker import Faker
fake = Faker()

fieldnames = ['username', 'password']

action = "create"

# ElasticSearch login Details
elasticUrl = "https://elastic.url"
adminUser = "elastic"
password = "not-really-a-password"
username_prefix = "user"
csv_file = "./credentials.csv"
headersUpdate = {
    "Content-Type": "application/json"
}

# Add user to Kibana_admin role. 
if action == "create":
    with open(csv_file, 'w', newline='') as csvWrite:
        writer = csv.DictWriter(csvWrite, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,100):
            usernameIterator = "{}-{}".format(username_prefix,str(i).zfill(3))
            request_url = "{}/_security/user/{}".format(elasticUrl, usernameIterator)
            rand_password = str(fake.text(max_nb_chars=20)).lower().replace(' ', '-').replace('.','')
            method = "POST"
            request_body = {
            "password" : rand_password,
            "roles" : [ "security_analyst" ],
            "full_name" : "{}".format(usernameIterator)
            }
            r = requests.post(request_url, headers=headersUpdate, data=json.dumps(request_body), auth = HTTPBasicAuth(adminUser, password))
            if r.status_code == 200:
                writer.writerow({"username": usernameIterator, "password": rand_password})
            else:
                logging.warning('User {} failed to create'.format(usernameIterator)) 


if action == "update":
    for i in range(0,100):
        usernameIterator = "{}-{}".format(username_prefix,str(i).zfill(3))
        request_url = "{}/_security/user/{}".format(elasticUrl, usernameIterator)
        method = "POST"
        request_body = {
        "password" : "j@rV1s{}".format(usernameIterator),
        "roles" : [ "security_analyst" ],
        "full_name" : "{}".format(usernameIterator)
        }
        r = requests.post(request_url, headers=headersUpdate, data=json.dumps(request_body), auth = HTTPBasicAuth(adminUser, password))
        

# Set no role to prevent login.
if action == "disable":
    for i in range(0,100):
        usernameIterator = "{}-{}".format(username_prefix,str(i).zfill(3))
        request_url = "{}/_security/user/user{}".format(elasticUrl, numberIterator)
        method = "POST"
        request_body = {
        "roles" : []}
        requests.post(request_url, headers=headersUpdate, data=json.dumps(request_body), auth = HTTPBasicAuth(adminUser, password))
    
