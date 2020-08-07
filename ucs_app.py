from ucs_main import ucs_logon, configure_organisation, configure_uuid_pool
from ucs_main import configure_vlans, configure_vsans, configure_mac_pools
from ucs_main import configure_ip_pools, configure_uuid_pool, configure_qos_policy
from ucs_main import configure_sol_policy, configure_cdp_pol
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

mac_pool = pd.read_excel(open(args.f, 'rb'), sheet_name='MacPools')
for index, row in mac_pool.iterrows():
    configure_mac_pools(handle, org=row['Org'], description=row['Desc'],
                        name=row['Name'], mac_from=row['StartMac'],
                        mac_to=row['EndMac'])

qos_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='QoSPolicy')
for index, row in qos_pol.iterrows():
    configure_qos_policy(handle, org=row['Org'], description=row['Desc'],
                    name=row['Name'], priority=row['Priority'],
                    burst=row['Burst'])

uuid_pool = pd.read_excel(open(args.f, 'rb'), sheet_name='Uuids')
for index, row in uuid_pool.iterrows():
    configure_uuid_pool(handle, org=row['Org'], name=row['Name'],
            descr=row['Desc'], assgn_order='sequential', uuid_to=row['UuidEnd'],
            uuid_from=row['UuidStart'], pref = 'derived')


ip_pool = pd.read_excel(open(args.f, 'rb'), sheet_name='IpPool')
for index, row in ip_pool.iterrows():
    configure_ip_pools(handle, org=row['Org'], description=row['Desc'],
            name=row['Name'], ip_from=row['StartIP'], ip_to=row['EndIP'],
            ip_gw=row['Gateway'], assignment_ordr='sequential',
            ip_subnet=row['SubnetMask'], dns_prim=row['PrimaryDNS'],
            dns_sec=row['SecondaryDNS'])

vlans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vlans')
for index, row in vlans.iterrows():
    configure_vlans(handle, vlan_id=str(row['VlanId']),
                    vlan_name=row['VlanName'])

vsans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vsans')
for index, row in vsans.iterrows():
    configure_vsans(handle, name=row['VsanName'], vsan_id=row['VsanId'],
                        fabric=row['Fabric'])
