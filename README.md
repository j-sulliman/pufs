# PUFS - Provision UCS from Spreadsheet
Get a headstart on UCS design and deployment
Reduce implementation time from days to minutes
Reduce configuration errors by testing deployment against pre-prod in minutes
Auto generate design documentation

# Suggested Workflow
Gather requirements and design inputs for UCS implementation
Enter into spreadsheet (ucs-implementation-data.xlsx) - this spreadsheet would be the source of truth for UCS design and implementation detail
Pre production implementation - Push the configuration parameters / inputs to UCS Platform Emulator and validate and adjust as needed

A Design Document in word format will be automatically generated - this can be used as a starting point for Detailed Design or As Builts
Once satisified with pre-prod (UCSPE) configuration push to production


![alt text](https://github.com/j-sulliman/pufs/blob/master/UCS%20Design%20Document.png)

# Demo
https://youtu.be/nKs3KvOY_Tw

# Setup
```
$ python3 -m venv venv

$ source venv/bin/activate

$ git init

$ git pull https://github.com/j-sulliman/pufs.git

Install the required dependencies:

$ pip3 install -r requirements.txt
```

# Running the Script
Run ucs_app.py with UCSM IP, Username, Password and input spreadsheet arguements as below
```
$ python ucs_app.py -a <192.168.100.132> -u <ucspe> -p <ucspe> -f <ucs-implementation-data.xlsx>

```

# Validate the configuration in UCSM and Review the generated word document

