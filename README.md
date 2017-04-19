# Signal Sciences Settings export and import
Tools for importing and exporting Signal Sciences settings

## Configuration

The configuration options are pretty straight forward and can be set as JSON parameters in a file or via environment variables.

**JSON Example:**

    {
    "email":"user@domain.com", #Email used for logging into Signal Sciences
    "password":"PASWORD", #Password used for logging into Signal Sciences. This currently needs to be an API users if you if SSO turned on
    "corp":"CORP", #The Corp that your dashboard view sits under
    "siteName":"SITE NAME" #The name of the dashboard view
    }



**Environment Variables:**

**ENV Name** | **Value** | **Description**
SIGSCI_EMAIL | STRING | Email used for logging into Signal Sciences
SIGSCI_PASSWORD | STRING | Password used for logging into Signal Sciences. 
SIGSCI_CORP | STRING | The Corp that your dashboard view sits under
SIGSCI_SITE_NAME | STRING | The name of the dashboard view

## setting-export.py Usage

This script will export the current redactions, alerts, blacklists, whitelists (ip, paths, parameters) for a specific site to both STDOUT and a file redactImportFile.txt with the right format to use for the import.

**Example:**
    
    python settings-export.py -c config.json

**Output:**
    
    {"redactionType": 0, "created": "2017-03-29T19:56:06Z", "field": "datafield", "createdBy": "user@domain.com", "id": "58dc11562e266a7d1eab9956"}
    {"redactionType": 0, "created": "2017-03-29T20:04:11Z", "field": "importedfield", "createdBy": "user@domain.com", "id": "58dc133b3c2b611c3b6fad05"}
    {"redactionType": 1, "created": "2017-03-29T20:04:33Z", "field": "importedfieldnew", "createdBy": "user@domain.com", "id": "58dc13512e266a7d1eab9d10"}
    {"redactionType": 0, "created": "2017-03-29T20:15:37Z", "field": "parameter", "createdBy": "user@domain.com", "id": "58dc15e93c2b611c3b6fb250"}
    {"redactionType": 1, "created": "2017-03-29T20:15:37Z", "field": "requestheader", "createdBy": "user@domain.com", "id": "58dc15e93c2b611c3b6fb253"}
    {"redactionType": 2, "created": "2017-03-29T20:15:38Z", "field": "responseheader", "createdBy": "user@domain.com", "id": "58dc15ea2e266a7d1eaba249"}


## settings-import.py Usage

This script will import the redactions, alerts, blacklists, and whitelists (ip, paths, parameters) for a specific site from the file specified.

**Example:**

    python settings-import.py -c config.json -f importFile.txt