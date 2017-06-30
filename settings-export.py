import sys, requests, os, calendar, json
from datetime import datetime, timedelta
import os
import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Utility for adding redactions in mass to a Signal Sciences Site')

parser.add_argument("-c", metavar="CONFIG", type=str, 
                        help="Specify the file with the configuration options")

opts = parser.parse_args()


# Initial setup

if "c" in opts and not(opts.c is None):
    confFile = open(opts.c, "r")

    confJson = json.load(confFile)
else:
    confJson = ""




api_host = 'https://dashboard.signalsciences.net'
if "email" in confJson and not(confJson["email"] is None):
    email = confJson["email"]
else:
    email = os.environ.get('SIGSCI_EMAIL') 

if "password" in confJson and not(confJson["password"] is None):
    password = confJson["password"]
else:
    password = os.environ.get('SIGSCI_PASSWORD') 

if "corp" in confJson and not(confJson["corp"] is None):
    corp_name = confJson["corp"]
else:
    corp_name = os.environ.get('SIGSCI_CORP')

if "siteName" in confJson and not(confJson["siteName"] is None):
    site_name = confJson["siteName"]
else:
    site_name = corp_name = os.environ.get('SIGSCI_SITE_NAME')

showPassword = False


#Definition for error handling on the response code

def checkResponse(code, responseText, url=None, token=None):
    if code == 400:
        print("Bad API Request (ResponseCode: %s)" % (code))
        print("ResponseError: %s" % responseText.rstrip())
        print('url: %s' % url)
        print('email: %s' % email)
        print('Corp: %s' % corp_name)
        print('SiteName: %s' % site_name)
        print("Token: %s" % token)
        if showPassword is True:
            print('password: %s' % password)
        exit(code)
    elif code == 500:
        print("Caused an Internal Server error (ResponseCode: %s)" % (code))
        print("ResponseError: %s" % responseText.rstrip())
        print('url: %s' % url)
        print('email: %s' % email)
        print('Corp: %s' % corp_name)
        print('SiteName: %s' % site_name)
        print("Token: %s" % token)
        if showPassword is True:
            print('password: %s' % password)
        exit(code)
    elif code == 401:
        print("Unauthorized, likely bad credentials or site configuration, or lack of permissions (ResponseCode: %s)" % (code))
        print("ResponseError: %s" % responseText.rstrip())
        print('email: %s' % email)
        print('Corp: %s' % corp_name)
        print('SiteName: %s' % site_name)
        if showPassword is True:
            print('password: %s' % password)
        exit(code)
    elif code >= 402 and code <= 599 and code != 500:
        print("ResponseCode: %s" % code)
        print("ResponseError: %s" % responseText.rstrip())
        print('url: %s' % url)
        print('email: %s' % email)
        print('Corp: %s' % corp_name)
        print('SiteName: %s' % site_name)
        print("Token: %s" % token)
        if showPassword is True:
            print('password: %s' % password)
        exit(code)
    else:
        print("\nSuccess")
        print("ResponseCode: %s" % code)
        #print("Response: %s" % responseText.rstrip())
        print('url: %s' % url)
        # print('email: %s' % email)
        # print('Corp: %s' % corp_name)
        # print('SiteName: %s' % site_name)
        # print("Token: %s" % token)
        # if showPassword is True:
        #     print('password: %s' % password)


# Authenticate
authEndpoint = api_host + '/api/v0/auth'
auth = requests.post(
    authEndpoint,
    data = {"email": email, "password": password}
)

authCode = auth.status_code
authError = auth.text

checkResponse(authCode, authError, authEndpoint)

parsed_response = auth.json()
token = parsed_response['token']

headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer %s' % token
}

urlBlack = api_host + ('/api/v0/corps/%s/sites/%s/blacklist' % (corp_name, site_name))
urlWhite = api_host + ('/api/v0/corps/%s/sites/%s/whitelist' % (corp_name, site_name))
urlParam = api_host + ('/api/v0/corps/%s/sites/%s/paramwhitelist' % (corp_name, site_name))
urlPath = api_host + ('/api/v0/corps/%s/sites/%s/pathwhitelist' % (corp_name, site_name))
urlAlerts = api_host + ('/api/v0/corps/%s/sites/%s/alerts' % (corp_name, site_name))
urlRedact = api_host + ('/api/v0/corps/%s/sites/%s/redactions' % (corp_name, site_name))
multiUrl = {"whitelist": urlWhite, "whitelistPath": urlPath, "whitelistParam": urlParam, "blacklist": urlBlack, "alerts": urlAlerts, "redactions": urlRedact}

importFile = "ImportFile.txt"

if os.path.isfile(importFile):
    try:
        os.remove(importFile)
    except OSError as e: 
        if e.errno != errno.ENOENT: 
            raise


for listType in multiUrl:
    url = multiUrl[listType]
    file = open(importFile, "a")
    response_raw = requests.get(url, headers=headers)
    responseCode = response_raw.status_code
    responseError = response_raw.text

    checkResponse(responseCode, responseError, url)


    response = json.loads(response_raw.text)

    print("\nExporting %s: " % listType)


    for request in response['data']:
        output = json.dumps(request)
        if listType == "blacklist" or listType == "whitelist" or listType == "whitelistPath" or listType == "whitelistParam":
            note = request["note"]

        if listType == "blacklist":
            source = request["source"]
            expires = request["expires"]
            exportJson = ("{\"blacklist\": \"{\\\"source\\\": \\\"%s\\\", \\\"expires\\\": \\\"%s\\\", \\\"note\\\":\\\"%s\\\"}\"}") % (source, expires, note)
        elif listType == "whitelist":
            source = request["source"]
            expires = request["expires"]
            exportJson = ("{\"whitelist\": \"{\\\"source\\\": \\\"%s\\\", \\\"expires\\\": \\\"%s\\\", \\\"note\\\":\\\"%s\\\"}\"}") % (source, expires, note)
        elif listType == "whitelistPath":
            path = request["path"] 
            exportJson = ("{\"whitelistPath\": \"{\\\"path\\\": \\\"%s\\\", \\\"note\\\":\\\"%s\\\"}\"}") % (path, note)
        elif listType == "whitelistParam":
            name = request["name"] 
            wlType = request["type"] 
            exportJson = ("{\"whitelistParam\": \"{\\\"name\\\": \\\"%s\\\",\\\"type\\\": \\\"%s\\\", \\\"note\\\":\\\"%s\\\"}\"}") % (name, wlType, note)
        elif listType == "alerts":
            enabled = request["enabled"]
            if enabled == True:
            	enabled = "true"
            else:
            	enabled = "false"
            interval = request["interval"]
            longName = request["longName"]
            fieldName = request["fieldName"]
            action = request["action"]
            tagName = request["tagName"]
            threshold = request["threshold"]
            exportJson = ("{\"alerts\": \"{\\\"enabled\\\": %s,\\\"interval\\\": %s, \\\"longName\\\":\\\"%s\\\", \\\"action\\\":\\\"%s\\\", \\\"tagName\\\":\\\"%s\\\", \\\"threshold\\\":%s}\"}") % \
            (enabled, interval, longName, action, tagName, threshold)
        elif listType == "redactions":
            redactField = request["field"]
            redactTpe = request["redactionType"]
            exportJson = ("{\"redactions\": \"{\\\"field\\\": \\\"%s\\\", \\\"redactionType\\\": %s}\"}") % (redactField, redactTpe)
        else:
            print("Unknown type \"%s\"" % listType)
        print("\n%s" % output)
        file.write("%s\n" % exportJson)
