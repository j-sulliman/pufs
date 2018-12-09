from ucs_main import configure_organisation, configure_mac_pools,configure_uuid_pool, configure_maint_policy
from ucs_main import configure_host_fw_policy, configure_boot_policy, configure_local_disk_conf_policy
from ucs_main import configure_bios_policy, configure_scrub_policy, configure_ip_pools, configure_qos_policy
from ucs_main import configure_cdp_pol, configure_vsans, configure_wwnn_pools, configure_wwpn_pools
from ucs_main import configure_vhba_templates, configure_vnic_templates, configure_vlans, configure_app_vnic_template
from ucs_main import configure_service_profile_template, configure_lan_connectivity_policy
from ucs_main import configure_san_connectivity_policy, create_sp_from_template, ucs_logon, configure_sol_policy


handle = ucs_logon(ip_addr="192.168.2.114", usr="ucspe", pw="ucspe")

twr_data_vlans = ['114', '116', '118', '119', '216', '218', '306', '307', '400', '401', '402', '404', '405', '406',
                  '408', '420', '430', '431', '450', '451', '454', '460', '461', '462', '464', '470', '471', '474',
                  '512', '513', '514', '515', '516', '520', '521', '522', '601', '602', '603', '604', '605', '606',
                  '607', '608', '609', '610', '818', '819', '821', '900', '901', '902', '903', '904', '950', '951',
                  '952', '953', '954', '970', '971', '990']

configure_organisation(handle, name="ORB4ESX")

configure_mac_pools(handle, "ORB4ESX","PROD TOWER MAC Pool for Fabric A","ORB4PRD_MAC-A","00:25:B5:1A:00:00",
                    "00:25:B5:1A:00:FF")
configure_mac_pools(handle, "ORB4ESX","PROD TOWER MAC Pool for Fabric B","ORB4PRD_MAC-B","00:25:B5:1B:00:00",
                    "00:25:B5:1B:00:FF")

configure_mac_pools(handle, "ORB4ESX","DEV TOWER MAC Pool for Fabric A","ORB4DEV_MAC-A","00:25:B5:2A:00:00",
                    "00:25:B5:2A:00:FF")
configure_mac_pools(handle, "ORB4ESX","DEV TOWER MAC Pool for Fabric B","ORB4DEV_MAC-B","00:25:B5:2B:00:00",
                    "00:25:B5:2B:00:FF")
configure_sol_policy(handle, org="ORB4ESX", name="SOL-POL", descr="Serial Over LAN Policy for Tower c240 Servers",
                     baud_speed="115200")
configure_uuid_pool(handle,'ORB4ESX',"ORB4ESX-UUID","UUID Pool for Tower ESX","sequential",
                    "0000-000000000256","0000-000000000001")
configure_maint_policy(handle, org="ORB4ESX",name="USER-ACK-MAINT",reboot_pol="user-ack", descr="User Ack")

configure_host_fw_policy(handle, org="ORB4ESX",name="FW-3.2.3i",descr="3.2.3i")
configure_boot_policy(handle, "ORB4ESX","CDROM","Boot Policy for Tower ESX")
configure_local_disk_conf_policy(handle, "ORB4ESX", "INT-CARD", "Local Disk Policy for Tower ESX")
configure_bios_policy(handle, "ORB4ESX", "NO-QUIET", "Local Disk Policy for Tower ESX")

configure_scrub_policy(handle, "ORB4ESX", "BIOS-SCRUB", "Local Disk Policy for Tower ESX")
configure_ip_pools(handle, "ORB4ESX","KVM Management IP Pool for Tower Compute", "KVM", "10.48.111.8",
                   "10.48.111.136", "10.48.111.1", "sequential")
configure_qos_policy(handle, "ORB4ESX", "Platinum QoS Policy for Tower Application vNIC", "APP",
                     "platinum", "10240")
configure_qos_policy(handle, "ORB4ESX", "Platinum QoS Policy for Tower Recover NFS vNIC", "NFS",
                     "platinum", "10240")
configure_qos_policy(handle, "ORB4ESX", "Silver QoS Policy for Tower Management vNIC", "MGMT",
                     "silver", "10240")
configure_qos_policy(handle, "ORB4ESX", "Bronze QoS Policy for Tower vMotion vNIC", "VMOTION",
                     "silver", "10240")
configure_qos_policy(handle, "ORB4ESX", "FC QoS Policy for Tower FC vHBAs", "FC",
                     "fc", "10240")
configure_qos_policy(handle, "ORB4ESX", "Best-Effort QoS Policy for Tower Backup vNIC", "BKP",
                     "best-effort", "10240")
configure_cdp_pol(handle, "ORB4ESX","Network Control Policy for Tower vNICs", "CDP-ENA-LNK-DOWN")
configure_vsans(handle, name='ORB4-VSAN-A', vsan_id='1101', fabric='A')
configure_vsans(handle, name='ORB4-VSAN-B', vsan_id='1102',fabric='B')
configure_wwnn_pools(handle, org="org-root/org-ORB4ESX",wwnn_name="ORB4-WWNN",description="Auckland WWNN Pool",
                     assignment_order="sequential",from_wwnn="20:00:20:25:B5:01:00:00",
                     to_wwnn="20:00:20:25:B5:01:00:FF")

configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for PROD Tower ESX A Side (VSAN 1101)",
                     name="ORB4PRD-WWPN-A", wwpn_from="20:00:2A:25:b5:01:0a:00", wwpn_to="20:00:2A:25:B5:01:0A:FF")
configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for PROD Tower ESX B Side (VSAN 1102)",
                     name="ORB4PRD-WWPN-B", wwpn_from="20:00:2B:25:b5:01:0b:00", wwpn_to="20:00:2B:25:B5:01:0b:FF")


configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for DEV Tower ESX A Side (VSAN 1101)",
                     name="ORB4DEV-WWPN-A", wwpn_from="20:00:2A:25:b5:01:1a:00", wwpn_to="20:00:2A:25:B5:01:1A:FF")
configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for DEV Tower ESX B Side (VSAN 1102)",
                     name="ORB4DEV-WWPN-B", wwpn_from="20:00:2B:25:b5:01:1b:00", wwpn_to="20:00:2B:25:B5:01:1b:FF")


configure_vlans(handle, "512", 'MGMT')
configure_vlans(handle, "515", 'VMOTION')
configure_vlans(handle, "524", 'BACKUP')


# Prod vNIC and vHBA Templates
configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4PRD-HBA-A", wwpn_pool="ORB4PRD-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4PRD-HBA-B", wwpn_pool="ORB4PRD-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side A",
                         "PRD-MGMT-A","ORB4PRD_MAC-A","9000","MGMT","CDP-ENA-LNK-DOWN","MGMT_0512","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side B",
                         "PRD-MGMT-B","ORB4PRD_MAC-B","9000","MGMT","CDP-ENA-LNK-DOWN","MGMT_0512","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side A",
                         "PRD-VMOTION-A","ORB4PRD_MAC-A","9000","VMOTION","CDP-ENA-LNK-DOWN","VMOTION_0515","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side B",
                         "PRD-VMOTION-B","ORB4PRD_MAC-B","9000","VMOTION","CDP-ENA-LNK-DOWN","VMOTION_0515","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side A",
                         "PRD-BKP-A","ORB4PRD_MAC-A","9000","BKP","CDP-ENA-LNK-DOWN","BACKUP_0524","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side B",
                         "PRD-BKP-B","ORB4PRD_MAC-B","9000","BKP","CDP-ENA-LNK-DOWN","BACKUP_0524","B")
#configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side A",
#                         "PRD-DATA-A","ORB4_MAC-A","9000","APP","CDP-ENA-LNK-DOWN","DATA_0922","A")
#configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side B",
#                         "PRD-DATA-B","ORB4_MAC-B","9000","APP","CDP-ENA-LNK-DOWN","DATA_0922","B")

for vlan_id in twr_data_vlans:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_vlans(handle, vlan_id, 'DATA_VLANs')
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for PROD Tower ESX Backup vNIC side A",
                                name="PRD-DATA-A",mac_pool="ORB4PRD_MAC-A",mtu="9000",qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="DATA_VLANs_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for PROD Tower ESX Backup vNIC side B",
                                name="PRD-DATA-B", mac_pool="ORB4PRD_MAC-B", mtu="9000", qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="DATA_VLANs_{}".format(vlan_id_cleaned),
                                fabric="B")

    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for DEV Tower ESX Backup vNIC side A",
                                name="DEV-DATA-A", mac_pool="ORB4DEV_MAC-A", mtu="9000", qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="DATA_VLANs_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for DEV Tower ESX Backup vNIC side B",
                                name="DEV-DATA-B", mac_pool="ORB4DEV_MAC-B", mtu="9000", qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="DATA_VLANs_{}".format(vlan_id_cleaned),
                                fabric="B")

configure_san_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  name="ORB4PRD-SCON",
                                  vhba_name="vHBA0",
                                  vhba_template_name="ORB4PRD-HBA-A",
                                  vsan_name="ORB4-VSAN-A",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="A",
                                  vHBA_order="1",
                                  adapter_profile="VMWare",
                                  wwpn_pool="ORB4PRD-WWPN-A",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_san_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  name="ORB4PRD-SCON",
                                  vhba_name="vHBA1",
                                  vhba_template_name="ORB4PRD-HBA-B",
                                  vsan_name="ORB4-VSAN-B",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="B",
                                  vHBA_order="2",
                                  adapter_profile="VMWare",
                                  wwpn_pool="ORB4PRD-WWPN-B",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-MGMT-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC1",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4PRD-MAC-A",
                                  qos_pol="MGMT",
                                  vnic_order="3")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-VMOTION-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC2",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4PRD-MAC-A",
                                  qos_pol="VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-DATA-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC3",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4PRD-MAC-A",
                                  qos_pol="APP",
                                  vnic_order="5")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-BKP-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC4",
                                  description="Production Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4PRD-MAC-A",
                                  qos_pol="NFS",
                                  vnic_order="6")




configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-MGMT-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC5",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4PRD-MAC-B",
                                  qos_pol="MGMT",
                                  vnic_order="7")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-VMOTION-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC6",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4PRD-MAC-B",
                                  qos_pol="VMOTION",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-DATA-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC7",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4PRD-MAC-B",
                                  qos_pol="APP",
                                  vnic_order="9")
configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-BKP-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC8",
                                  description="Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4PRD-MAC-B",
                                  qos_pol="BKP",
                                  vnic_order="10")



configure_service_profile_template(handle, name="ORB4ESX-PRD",
                                   type= "initial-template",
                                   resolve_remote= "yes",
                                   descr="AKL VI APP Descr",
                                   usr_lbl="",src_templ_name="",
                                   ext_ip_state="pooled",
                                   ext_ip_pool_name="KVM",
                                   ident_pool_name="ORB4ESX-UUID",
                                   agent_policy_name='',
                                   bios_profile_name="NO-QUIET",
                                   boot_policy_name="CDROM",
                                   dynamic_con_policy_name="",
                                   host_fw_policy_name="FW-3.2.3i",
                                   kvm_mgmt_policy_name="",
                                   lan_conn_policy_name="ORB4PRD-CON",
                                   san_conn_policy_name="ORB4PRD-SCON",
                                   local_disk_policy_name="INT-CARD",
                                   maint_policy_name="USER-ACK-MAINT",
                                   mgmt_access_policy_name="",
                                   mgmt_fw_policy_name="",
                                   power_policy_name="default",
                                   scrub_policy_name="BIOS-SCRUB",
                                   sol_policy_name="SOL-POL",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="ORB4ESX"
                                   )



# DEV vNIC and vHBA Templates
configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4DEV-HBA-A", wwpn_pool="ORB4DEV-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4DEV-HBA-B", wwpn_pool="ORB4DEV-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4DEV-HBA-A", wwpn_pool="ORB4DEV-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4DEV-HBA-B", wwpn_pool="ORB4DEV-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side A",
                         "DEV-MGMT-A","ORB4DEV_MAC-A","9000","MGMT","CDP-ENA-LNK-DOWN","MGMT_0512","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side B",
                         "DEV-MGMT-B","ORB4DEV_MAC-B","9000","MGMT","CDP-ENA-LNK-DOWN","MGMT_0512","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side A",
                         "DEV-VMOTION-A","ORB4DEV_MAC-A","9000","VMOTION","CDP-ENA-LNK-DOWN","VMOTION_0515","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side B",
                         "DEV-VMOTION-B","ORB4DEV_MAC-B","9000","VMOTION","CDP-ENA-LNK-DOWN","VMOTION_0515","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side A",
                         "DEV-BKP-A","ORB4DEV_MAC-A","9000","BKP","CDP-ENA-LNK-DOWN","BACKUP_0524","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side B",
                         "DEV-BKP-B","ORB4DEV_MAC-B","9000","BKP","CDP-ENA-LNK-DOWN","BACKUP_0524","B")
#configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side A",
#                         "DEV-DATA-A","ORB4_MAC-A","9000","NFS","CDP-ENA-LNK-DOWN","DATA_0922","A")
#configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side B",
#                         "DEV-DATA-B","ORB4_MAC-B","9000","NFS","CDP-ENA-LNK-DOWN","DATA_0922","B")




configure_san_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  name="ORB4DEV-SCON",
                                  vhba_name="vHBA0",
                                  vhba_template_name="ORB4DEV-HBA-A",
                                  vsan_name="ORB4-VSAN-A",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="A",
                                  vHBA_order="1",
                                  adapter_profile="VMWare",
                                  wwpn_pool="ORB4-WWPN-A",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_san_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  name="ORB4DEV-SCON",
                                  vhba_name="vHBA1",
                                  vhba_template_name="ORB4DEV-HBA-B",
                                  vsan_name="ORB4-VSAN-B",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="B",
                                  vHBA_order="2",
                                  adapter_profile="VMWare",
                                  wwpn_pool="ORB4DEV-WWPN-B",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-MGMT-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC1",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4DEV-MAC-A",
                                  qos_pol="MGMT",
                                  vnic_order="3")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-VMOTION-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC2",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4DEV-MAC-A",
                                  qos_pol="VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-DATA-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC3",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4DEV-MAC-A",
                                  qos_pol="APP",
                                  vnic_order="5")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-BKP-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC4",
                                  description="Production Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4DEV-MAC-A",
                                  qos_pol="BKP",
                                  vnic_order="6")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-MGMT-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC5",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4DEV-MAC-B",
                                  qos_pol="MGMT",
                                  vnic_order="7")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-VMOTION-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC6",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4DEV-MAC-B",
                                  qos_pol="VMOTION",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-DATA-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC8",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4DEV-MAC-B",
                                  qos_pol="APP",
                                  vnic_order="10")
configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-BKP-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC9",
                                  description="Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4DEV-MAC-B",
                                  qos_pol="BKP",
                                  vnic_order="11")


configure_service_profile_template(handle, name="ORB4ESX-DEV",
                                   type= "initial-template",
                                   resolve_remote= "yes",
                                   descr="AKL VI APP Descr",
                                   usr_lbl="",src_templ_name="",
                                   ext_ip_state="pooled",
                                   ext_ip_pool_name="KVM",
                                   ident_pool_name="ORB4ESX-UUID",
                                   agent_policy_name='',
                                   bios_profile_name="NO-QUIET",
                                   boot_policy_name="CDROM",
                                   dynamic_con_policy_name="",
                                   host_fw_policy_name="FW-3.2.3i",
                                   kvm_mgmt_policy_name="",
                                   lan_conn_policy_name="ORB4DEV-CON",
                                   san_conn_policy_name="ORB4DEV-SCON",
                                   local_disk_policy_name="INT-CARD",
                                   maint_policy_name="USER-ACK-MAINT",
                                   mgmt_access_policy_name="",
                                   mgmt_fw_policy_name="",
                                   power_policy_name="default",
                                   scrub_policy_name="BIOS-SCRUB",
                                   sol_policy_name="SOL-POL",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="ORB4ESX"
                                   )

create_sp_from_template(handle, start_sp_value=01, sp_quantity=4,sp_name_prefix="ORB4ESX",org="ORB4ESX",
                        template_name="ORB4ESX-PRD")



create_sp_from_template(handle, start_sp_value=05, sp_quantity=2,sp_name_prefix="ORB4ESX",org="ORB4ESX",
                        template_name="ORB4ESX-DEV")