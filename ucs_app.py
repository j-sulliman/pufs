from ucs_main import ucs_logon, configure_organisation, configure_uuid_pool
from ucs_main import configure_vlans, configure_vsans, configure_mac_pools
from ucs_main import configure_ip_pools, configure_uuid_pool, configure_qos_policy
from ucs_main import configure_sol_policy, configure_cdp_pol
from ucs_main import configure_vnic_templates, configure_scrub_policy
from ucs_main import configure_san_connectivity_policy, configure_bios_policy
from ucs_main import configure_vhba_templates, configure_local_disk_conf_policy
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

bios_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='BiosPol')
for index, row in bios_pol.iterrows():
    configure_bios_policy(handle, org=row['Org'], name=row['Name'],
                        descr=row['Desc'], quiet_boot=row['QuietBoot'],
                        cdn_ctrl=row['CDNControl'],
                        post_err_pause=row['PostErrorPause'],
                        reboot_on_upd=row['RebootOnupdate'])

sol_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='SolPolicy')
for index, row in sol_pol.iterrows():
    configure_sol_policy(handle, org=row['Org'], name=row['Name'],
                        descr=row['Desc'], baud_speed=row['Speed'])

local_disk_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='LocalDiskConfigPol')
for index, row in local_disk_pol.iterrows():
    configure_local_disk_conf_policy(handle, org=row['Org'], name=row['Name'],
                        descr=row['Desc'], mode=row['Mode'],
                        flex_flash=row['FlexFlash'],
                        flex_flash_report=row['FlexFlashReporting'],
                        flex_flash_remove=row['FlexFlashRemovableState'])

cdp_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='NetworkControlPolicy')
for index, row in cdp_pol.iterrows():
    configure_cdp_pol(handle, org=row['Org'], description=row['Desc'],
                        name=row['Name'], cdp=row['CDP'],
                        macreg=row['MACRegisterMode'],
                         actionon=row['ActionOnUplinkFailure'],
                         macsec=row['MACSecurityForge'],
                         lldprx=row['LLDPRx'], lldptx=row['LLDPTx'])

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

vsans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vsans')
for index, row in vsans.iterrows():
    configure_vsans(handle, name=row['VsanName'], vsan_id=row['VsanId'],
                        fabric=row['Fabric'])

vhba_tmpl = pd.read_excel(open(args.f, 'rb'), sheet_name='vHBATemplates')
for index, row in vhba_tmpl.iterrows():
    for index2, row2 in vsans.iterrows():
        if row['Name'] == row2['VHBA-Template-1'] or row['Name'] \
            == row2['VHBA-Template-2']:
            configure_vhba_templates(handle, org=row['Org'],
                description=row['Desc'], name=row['Name'],
                wwpn_pool=row['WwpnPool'],
                vsan_name=row['VsanName'], fabric =row['FabricID'],
                qos_pol=row['QosPolicy'])

vlans = pd.read_excel(open(args.f, 'rb'), sheet_name='Vlans')
for index, row in vlans.iterrows():
    configure_vlans(handle, vlan_id=str(row['VlanId']),
                    vlan_name=row['VlanName'])



vnic_tmpl = pd.read_excel(open(args.f, 'rb'), sheet_name='vNICTemplates')
for index, row in vnic_tmpl.iterrows():
    for index2, row2 in vlans.iterrows():
        if row['Name'] == row2['VNIC-Template-A'] or row['Name'] \
            == row2['VNIC-Template-B']:
            configure_vnic_templates(handle, org=row['Org'],
                                         description=row['Desc'],
                                         name=row['Name'],
                                         mac_pool=row['MacPool'],
                                         mtu=str(row['MTU']),
                                         qos_pol=row['QosPolicy'],
                                         network_ctrl_pol=row['NetworkControlPolicy'],
                                         vlan_name=row2['VlanName'],
                                         switch=row['FabricID'])
