#!/usr/bin/python3

import os
import subprocess
import time
import socket
import shlex
import re
import requests
from akamai.edgegrid import EdgeGridAuth
import json # library needed for json manipulation

"""
This script was created to test mPulse activation based on user cookie provided by Akamai Edge Servers.
Tests requests are being sent towards the domain to be tested. Responses bodies are being tested for the "BOOMR" string and the mpulse API key.
Note1: The domain needs o be akamaized for this script to work properly.
Note2: The API key needs to be correct for the script to work properly.
"""

def main() -> str:
    hits = 0
    n = int(input ("Provide the number of iterations: "))
    domain=str(input("Provide the domain: "))
    path = str(input("Provide the path: "))
    api_key=str(input("Provide the API key related to " + domain +": "))
    logs = str(input("Enable debugging logs? (yes/no) "))
    for i in range (1,n+1):
        if mpulse_check(domain, path, api_key, logs):
            hits=hits+1
            print("Attempt "+ str(i) + " : HIT")
        else:
            print("Attempt "+ str(i) + " : MISS")    
    percentage = (float(hits)/float(n))*100
    #print(percentage)
    message = "Out of " + str(n) + " request(s), " + str(hits)  +" triggred mPulse, which is " + str(percentage) + "%."
    print(message)

def mpulse_check (domain: str, path: str, api_key: str, logs: bool) -> bool:
    url = "https://" + domain + path
    answer = False

    # creating a http request
    http_request = requests.Session()

    # defining headers
    headers = {}
    headers['Host'] = domain
    headers['Accept'] = "text/html"
    headers['Accept-Encoding'] = "gzip, deflate, br"
    headers['Connection'] = "keep-alive"

    # defining Pragma headers for Akamai debugging
    headers['Pragma'] = "akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-true-cache-key, akamai-x-get-extracted-values, akamai-x-get-request-id, akamai-x-get-client-ip, akamai-x-feo-trace, akamai-x-feo-state, akamai-x-extension-on, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-serial-no, akamai-x-tapioca-trace, akamai-x-flush-log"
    http_request.headers = headers

    # defining http response
    http_response = http_request.get(url)
    response_text = (http_response.text).strip()
    response_headers = (http_response.headers)
    #json_text=json.dumps(response_text)
    #json_headers=json.dumps(response_headers)
    #print(response_headers["X-True-Cache-Key"])
    if logs == "yes":
        print("Log line: " + str(http_response.headers['X-Akamai-Session-Info']))
    if (api_key in response_text) & ("BOOMR" in response_text):
        answer = True
    return answer

if __name__ == '__main__':
    main()
