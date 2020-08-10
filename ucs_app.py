from ucs_main import ucs_logon, configure_organisation, configure_uuid_pool
from ucs_main import configure_vlans, configure_vsans, configure_mac_pools
from ucs_main import configure_ip_pools, configure_uuid_pool
from ucs_main import configure_sol_policy, configure_cdp_pol
from ucs_main import configure_vnic_templates, configure_scrub_policy
from ucs_main import configure_san_connectivity_policy, configure_bios_policy
from ucs_main import configure_vhba_templates, configure_local_disk_conf_policy
from ucs_main import configure_wwnn_pools, configure_wwpn_pools
from ucs_main import configure_maint_policy, configure_qos_policy
from ucs_main import configure_host_fw_policy, configure_service_profile_template
from ucs_main import configure_lan_connectivity_policy
from word_doc import create_word_doc_title, create_word_doc_paragraph
from word_doc import create_word_doc_table
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Configure UCS from spreadsheet')
    parser.add_argument('-a', help='UCSM IP (a)ddress (not URL)',type=str,
                        required=True)
    parser.add_argument('-u', help='UCSM (u)ser name',type=str, required=True)
    parser.add_argument('-p', help='UCSM (p)assword',type=str, required=True)
    parser.add_argument('-f', help='Excel Spreadsheet File Name and Path',
                        type=str, required=True)
    args = parser.parse_args()

    handle = ucs_logon(ip_addr=args.a, usr=args.u, pw=args.p)


    orgs = pd.read_excel(open(args.f, 'rb'), sheet_name='Organisations')
    for index, row in orgs.iterrows():
        configure_organisation(handle, name=row['Name'])

    host_fw_pol=pd.read_excel(open(args.f, 'rb'), sheet_name='HostFWPol')
    for index, row in host_fw_pol.iterrows():
        configure_host_fw_policy(handle, org=row['Org'], name=row['Name'],
                            descr=row['Descr'],
                            ignore_comp_check=row['IgnoreCompCheck'],
                            stage_size=str(row['StageSize']),
                            rack_bun_ver=row['RackBundleVersion'],
                            upd_trig=row['UpdateTrigger'],
                            mode=row['Mode'],
                            blade_bun_ver=row['BladeBundleVersion'],
                            override_def_exc=row['OverrideDefaultExclusion'])

    maint_pol=pd.read_excel(open(args.f, 'rb'), sheet_name='MaintenancePol')
    for index, row in maint_pol.iterrows():
        configure_maint_policy(handle, org=row['Org'],
                    ss_timer=row['SoftShutdownTimer'], name=row['Name'],
                    reboot_pol=row['RebootPol'], descr=row['Desc'])

    scrub_pol=pd.read_excel(open(args.f, 'rb'), sheet_name='ScrubPol')
    for index, row in scrub_pol.iterrows():
        configure_scrub_policy(handle, org=row['Org'], name=row['Name'],
                            descr=row['Desc'], bios_scrub=row['BiosSettingScrub'],
                            flex_flash_scrub=row['FlexFlashScrub'],
                            disk_scrub=row['DiskScrub'])

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

    wwnn_pool = pd.read_excel(open(args.f, 'rb'), sheet_name='WwnnPool')
    for index, row in wwnn_pool.iterrows():
        configure_wwnn_pools(handle, org=row['Org'],
                                 wwnn_name=row['Name'],
                                 description=row['Desc'],
                                 assignment_order=row['AssignmentOrder'],
                                 from_wwnn=row['StartWWNN'],
                                 to_wwnn=row['EndWWNN'])


    wwpn_pool = pd.read_excel(open(args.f, 'rb'), sheet_name='WwpnPool')
    for index, row in wwpn_pool.iterrows():
        configure_wwpn_pools(handle, org=row['Org'],
                                 name=row['Name'],
                                 description=row['Desc'],
                                 assignment_ordr=row['AssignmentOrder'],
                                 wwpn_from=row['StartWWPN'],
                                 wwpn_to=row['EndWWPN'])

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

    lan_con_pol = pd.read_excel(open(args.f, 'rb'), sheet_name='LanConnectivityPolicy')
    for index, row in lan_con_pol.iterrows():
        print(row['vNICTemplateName'])
        configure_lan_connectivity_policy(handle,
                        organisation = "org-root/org-{}".format(row['Org']),
                        vnic_template_name=row['vNICTemplateName'],
                          vnic_order=str(row['vNICOrder']),
                          name=row['Name'],
                          vnic_name=row['vNICName'],
                          switch_id=row['SwitchID'],
                          adapter_profile=row['AdapterPol'])

    sp_template = pd.read_excel(open(args.f, 'rb'),
                                sheet_name='CreateServceProfileTemplate')
    for index, row in sp_template.iterrows():
        configure_service_profile_template(handle, name=row["Name"],
                                   type=row["type"],
                                   resolve_remote=row["resolve_remote"],
                                   descr=row["descr"],
                                   usr_lbl='',
                                   src_templ_name='',
                                   ext_ip_state=row["ext_ip_state"],
                                   ext_ip_pool_name=row["ext_ip_pool_name"],
                                   ident_pool_name=row["ident_pool_name"],
                                   agent_policy_name='',
                                   bios_profile_name=row["bios_profile_name"],
                                   boot_policy_name=row["boot_policy_name"],
                                   dynamic_con_policy_name='',
                                   host_fw_policy_name=row["host_fw_policy_name"],
                                   kvm_mgmt_policy_name=row["kvm_mgmt_policy_name"],
                                   lan_conn_policy_name=row["lan_conn_policy_name"],
                                   local_disk_policy_name=row["local_disk_policy_name"],
                                   maint_policy_name=row["maint_policy_name"],
                                   mgmt_access_policy_name='',
                                   mgmt_fw_policy_name='',
                                   power_policy_name='',
                                   san_conn_policy_name=row["san_conn_policy_name"],
                                   scrub_policy_name=row["scrub_policy_name"],
                                   sol_policy_name=row["sol_policy_name"],
                                   stats_policy_name='',
                                   vcon_profile_name='',
                                   vmedia_policy_name='',
                                   server_pool_name='',
                                   org=row["Org"])

    # Create the Design Document
    doc = create_word_doc_title(doc_title = 'Cisco UCS Detailed Design')
    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Organisations',
                paragraph_text='Organisations will be configured as follows:')
    doc = create_word_doc_table(doc, orgs)


    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Server Configuration',
                paragraph_text='This section outlines Service Profiles and Server Policies.')

    doc = create_word_doc_paragraph(doc = doc,
            heading_text = 'Host Firmware Policy',
            heading_level=2,
            paragraph_text='Host Firmware Policies will be configured as follows:')
    doc = create_word_doc_table(doc, host_fw_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Maintenance Policy',
                heading_level=2,
                paragraph_text='Maintenance Policies will be configured as follows:')
    doc = create_word_doc_table(doc, maint_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'UUID Pool',
                heading_level=2,
                paragraph_text='UUID Pool will be defined as follows:')
    doc = create_word_doc_table(doc, uuid_pool)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'BIOS Policies',
                heading_level=2,
                paragraph_text='BIOS Policies will be configured as follows:')
    doc = create_word_doc_table(doc, bios_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Scrub Policies',
                heading_level=2,
                paragraph_text='Scrub Policies will be configured as follows:')
    doc = create_word_doc_table(doc, scrub_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Local Disk Policies',
                heading_level=2,
                paragraph_text='Local Disk Policies will be configured as follows:')
    doc = create_word_doc_table(doc, local_disk_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Serial Over Lan Policies',
                heading_level=2,
                paragraph_text='Serial Over LAN Policies will be configured as follows:')
    doc = create_word_doc_table(doc, sol_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'UCS Networking',
                heading_level=1,
                paragraph_text='The following outlines the networking elements of the UCS design.')
    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Management Addresses',
                heading_level=2,
                paragraph_text='Management Pools will be configured as follows:')
    doc = create_word_doc_table(doc, ip_pool)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'Network Control Policies',
                heading_level=2,
                paragraph_text='Serial Over LAN Policies will be configured as follows:')
    doc = create_word_doc_table(doc, cdp_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'MAC Address Pools',
                heading_level=2,
                paragraph_text='MAC Address Pools will be configured as follows:')
    doc = create_word_doc_table(doc, mac_pool)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'QoS Policies',
                heading_level=2,
                paragraph_text='QoS Policies will be configured as follows:')
    doc = create_word_doc_table(doc, qos_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'VLANs',
                heading_level=2,
                paragraph_text='VLANs will be defined as follows:')
    doc = create_word_doc_table(doc, vlans)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'vNIC Templates',
                heading_level=2,
                paragraph_text='vNIC templates will be defined as follows:')
    doc = create_word_doc_table(doc, vnic_tmpl)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'LAN Connectivity Policy',
                heading_level=2,
                paragraph_text='LAN Connectivity Policy will be defined as follows:')
    doc = create_word_doc_table(doc, lan_con_pol)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'UCS Storage',
                heading_level=1,
                paragraph_text='The following outlines the Storage elements of the UCS design.')

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'VSANs',
                heading_level=2,
                paragraph_text='VSANs will be defined as follows:')
    doc = create_word_doc_table(doc, vsans)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'WWNN Pools',
                heading_level=2,
                paragraph_text='WWNN Pools will be defined as follows:')
    doc = create_word_doc_table(doc, wwnn_pool)

    doc = create_word_doc_paragraph(doc = doc,
                heading_text = 'WWPN Pools',
                heading_level=2,
                paragraph_text='WWPN Pools will be defined as follows:')
    doc = create_word_doc_table(doc, wwpn_pool)



    doc.save('demo.docx')
main()
