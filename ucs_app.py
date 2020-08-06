from ucs_main import ucs_logon, configure_organisation, configure_uuid_pool
from ucs_main import configure_vlans, configure_vsans
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Configure UCS from spreadsheet')
parser.add_argument('-a', help='UCSM IP (a)ddress (not URL)',type=str,
                    required=True)
parser.add_argument('-u', help='UCSM (u)ser name',type=str, required=True)
parser.add_argument('-p', help='UCSM (p)assword',type=str, required=True)
parser.add_argument('-f', help='Excel Spreadsheet File Name and Path',type=str,
                    required=True)
args = parser.parse_args()

handle = ucs_logon(ip_addr=args.a, usr=args.u, pw=args.p)


orgs = pd.read_excel(open(args.f, 'rb'), sheet_name='Organisations')
for index, row in orgs.iterrows():
    configure_organisation(handle, name=row['Name'])

vlans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vlans')
for index, row in vlans.iterrows():
    configure_vlans(handle, vlan_id=str(row['VlanId']),
                    vlan_name=row['VlanName'])

vsans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vsans')
for index, row in vsans.iterrows():
    configure_vsans(handle, name=row['VsanName'], vsan_id=row['VsanId'],
                        fabric=row['Fabric'])
