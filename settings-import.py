import sys, requests, os, calendar, json
from datetime import datetime, timedelta
import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Utility for adding blacklist in mass to a Signal Sciences Site')

parser.add_argument("-file", type=str, 
                        help="Specify the file with the redaction to add with a JSON item per new line")
parser.add_argument("-c", type=str, 
                        help="Specify the file with the configuration options")

opts = parser.parse_args()

if not ("file" in opts) or opts.file is None or opts.file == "":
    print("-file parameter must be specified")
    exit(1)

if not ("c" in opts) or opts.c is None or opts.c == "":
    print("-c parameter must be specified")
    exit(1)


# Initial setup

if "c" in opts and not(opts.c is None):
    confFile = open(opts.c, "r")

    confJson = json.load(confFile)
else:
    print("No configuration file")
    exit(1)

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

def checkResponse(code, responseText, url=None, token=None, data=None):
    if code == 400:
        responseJson = json.loads(responseText)
        if "message" in responseJson and (responseJson["message"] == "Parameter exists"\
            or responseJson["message"] == "URL path exists" or responseJson["message"] == "Privacy field with given name exists"):
            print("Entry already exists, going to next")
        else:
            print("Bad API Request (ResponseCode: %s)" % (code))
            print("ResponseError: %s" % responseText.rstrip())
            print('url: %s' % url)
            print('email: %s' % email)
            print('Corp: %s' % corp_name)
            print('SiteName: %s' % site_name)
            print("Token: %s" % token)
            print("Payload: %s" % data)
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

#API Endpoints
urlBlack = api_host + ('/api/v0/corps/%s/sites/%s/blacklist' % (corp_name, site_name))
urlWhite = api_host + ('/api/v0/corps/%s/sites/%s/whitelist' % (corp_name, site_name))
urlParam = api_host + ('/api/v0/corps/%s/sites/%s/paramwhitelist' % (corp_name, site_name))
urlPath = api_host + ('/api/v0/corps/%s/sites/%s/pathwhitelist' % (corp_name, site_name))
urlAlerts = api_host + ('/api/v0/corps/%s/sites/%s/alerts' % (corp_name, site_name))
urlRedact = api_host + ('/api/v0/corps/%s/sites/%s/redactions' % (corp_name, site_name))
multiUrl = {"whitelist": urlWhite, "whitelistPath": urlPath, "whitelistParam": urlParam, "blacklist": urlBlack, "alerts": urlAlerts, "redactions": urlRedact}

jsonFile = open(opts.file, "r") 



for line in jsonFile:

    entryType = json.loads(line)
    
    for info in entryType:
        currentType = entryType[info]
        print("\nImporting %s:" % info)
        payload = entryType[info]
        url = multiUrl[info]

    # print(payload)
    # exit(0)    

    response_raw = requests.post(url, headers=headers, data=payload)
    responseCode = response_raw.status_code
    responseError = response_raw.text

    checkResponse(responseCode, responseError, url, token, payload)
    print(payload)