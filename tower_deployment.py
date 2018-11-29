from ucs_main import configure_organisation, configure_mac_pools,configure_uuid_pool, configure_maint_policy
from ucs_main import configure_host_fw_policy, configure_boot_policy, configure_local_disk_conf_policy
from ucs_main import configure_bios_policy, configure_scrub_policy, configure_ip_pools, configure_qos_policy
from ucs_main import configure_cdp_pol, configure_vsans, configure_wwnn_pools, configure_wwpn_pools
from ucs_main import configure_vhba_templates, configure_vnic_templates, configure_vlans, configure_app_vnic_template
from ucs_main import configure_service_profile_template, configure_lan_connectivity_policy
from ucs_main import configure_san_connectivity_policy, create_sp_from_template, ucs_logon


akl_vlan = ['1030','1031','1032','1033','1034','1035','1036','1037','1038','1039','1040','1041','1042','1043','1044',
            '1045','1046','1047','1048','1049','1050','1051','1052','1053','1054','1055','1056','1057','1058','1059',
            '1061','1065','1070', '1071', '1072','1078','1087','1088','1090','2068','2104','2820','2821','2822',
            '2824','2825','2826','2827','2828','2828','2830','3002','3010','3030','503','505','513','537','544','549',
            '554']

handle = ucs_logon(ip_addr="192.168.2.114", usr="ucspe", pw="ucspe")
configure_organisation(handle, name="ORB4ESX")

configure_mac_pools(handle, "ORB4ESX","TOWER MAC Pool for Fabric A","ORB4_MAC-A","00:25:B5:1A:00:00", "00:25:B5:1A:00:FF")
configure_mac_pools(handle, "ORB4ESX","TOWER MAC Pool for Fabric B","ORB4_MAC-B","00:25:B5:1B:00:00", "00:25:B5:1B:00:FF")

configure_uuid_pool(handle,'ORB4ESX',"ORB4ESX-UUID","UUID Pool for Tower ESX","sequential",
                    "0000-000000000256","0000-000000000001")
configure_maint_policy(handle, org="ORB4ESX",name="USER-ACK-MAINT",reboot_pol="user-ack", descr="User Ack")
configure_host_fw_policy(handle, org="ORB4ESX",name="FW-3.2.3i",descr="3.2.3i")
configure_boot_policy(handle, "ORB4ESX","CDROM","Boot Policy for Tower ESX")
configure_local_disk_conf_policy(handle, "ORB4ESX", "INT-CARD", "Local Disk Policy for Tower ESX")
configure_bios_policy(handle, "ORB4ESX", "NO-QUIET", "Local Disk Policy for Tower ESX")

configure_scrub_policy(handle, "ORB4ESX", "BIOS-SCRUB", "Local Disk Policy for Tower ESX")
configure_ip_pools(handle, "ORB4ESX","KVM Management IP Pool for Tower Compute", "KVM", "10.233.178.16",
                   "10.233.178.47", "10.233.178.1", "sequential")
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

configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for Tower ESX A Side (VSAN 1101)",
                     name="ORB4-WWPN-A", wwpn_from="20:00:2A:25:b5:01:0a:00", wwpn_to="20:00:2A:25:B5:01:0A:FF")
configure_wwpn_pools(handle, org="ORB4ESX",description="WWPN Pool for Tower ESX B Side (VSAN 1102)",
                     name="ORB4-WWPN-B", wwpn_from="20:00:2B:25:b5:01:0b:00", wwpn_to="20:00:2B:25:B5:01:0b:FF")



# Prod vNIC and vHBA Templates
configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4PRD-HBA-A", wwpn_pool="ORB4-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4PRD-HBA-B", wwpn_pool="ORB4-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4DEV-HBA-A", wwpn_pool="ORB4-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4DEV-HBA-B", wwpn_pool="ORB4-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side A",
                         "PRD-MGMT-A","ORB4_MAC-A","9000","MGMT","CDP-ENA-LNK-DOWN","ORB4ESX-MGMT_1001","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side B",
                         "PRD-MGMT-B","ORB4_MAC-B","9000","MGMT","CDP-ENA-LNK-DOWN","ORB4ESX-MGMT_1001","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side A",
                         "PRD-VMT-A","ORB4_MAC-A","9000","VMOTION","CDP-ENA-LNK-DOWN","ORB4ESX-VMOTION_1002","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side B",
                         "PRD-VMT-B","ORB4_MAC-B","9000","VMOTION","CDP-ENA-LNK-DOWN","ORB4ESX-VMOTION_1002","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side A",
                         "PRD-BKP-A","ORB4_MAC-A","9000","BKP","CDP-ENA-LNK-DOWN","ORB4ESX-BACKUP_1003","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side B",
                         "PRD-BKP-B","ORB4_MAC-B","9000","BKP","CDP-ENA-LNK-DOWN","ORB4ESX-BACKUP_1003","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side A",
                         "PRD-NFS-A","ORB4_MAC-A","9000","NFS","CDP-ENA-LNK-DOWN","ORB4ESX-NFS_1004","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side B",
                         "PRD-NFS-B","ORB4_MAC-B","9000","NFS","CDP-ENA-LNK-DOWN","ORB4ESX-NFS_1004","B")


for vlan_id in akl_vlan:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_vlans(handle, vlan_id, 'ORB4ESX_VLAN')
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for Tower ESX vMotion vNIC side A",
                                name="PRD-APP-A",mac_pool="ORB4_MAC-A",mtu="9000",qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="ORB4ESX_VLAN_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for Tower ESX vMotion vNIC side B",
                                name="PRD-APP-B", mac_pool="ORB4_MAC-B", mtu="9000", qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="ORB4ESX_VLAN_{}".format(vlan_id_cleaned),
                                fabric="B")

configure_vlans(handle, "1001", 'ORB4ESX-MGMT')
configure_vlans(handle, "1002", 'ORB4ESX-VMOTION')
configure_vlans(handle, "1003", 'ORB4ESX-BACKUP')
configure_vlans(handle, "1004", 'ORB4ESX-NFS')
configure_san_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  name="ORB4PRD-SCON",
                                  vhba_name="vHBA0",
                                  vhba_template_name="ORB4PRD-HBA-A",
                                  vsan_name="ORB4-VSAN-A",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="A",
                                  vHBA_order="1",
                                  adapter_profile="VMWare",
                                  wwpn_pool="ORB4-WWPN-A",
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
                                  wwpn_pool="ORB4-WWPN-B",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-MGMT-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC1",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="MGMT",
                                  vnic_order="3")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-VMT-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC2",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-APP-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC3",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="APP",
                                  vnic_order="5")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-BKP-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC4",
                                  description="Production Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="NFS",
                                  vnic_order="6")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-NFS-A",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC5",
                                  description="NFS vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="NFS",
                                  vnic_order="7")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-MGMT-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC6",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="MGMT",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-VMT-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC7",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="VMOTION",
                                  vnic_order="9")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-APP-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC8",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="APP",
                                  vnic_order="10")
configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-BKP-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC9",
                                  description="Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="BKP",
                                  vnic_order="11")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="PRD-NFS-B",
                                  name="ORB4PRD-CON",
                                  vnic_name="vNIC10",
                                  description="NFS vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="NFS",
                                  vnic_order="12")

configure_service_profile_template(handle, name="ORB4PRD",
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
                                   sol_policy_name="",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="ORB4ESX"
                                   )



# DEV vNIC and vHBA Templates
configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4DEV-HBA-A", wwpn_pool="ORB4-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4DEV-HBA-B", wwpn_pool="ORB4-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vhba_templates(handle, org="ORB4ESX", description="vHBA Template for Tower ESX SAN Fabric A",
                         name="ORB4DEV-HBA-A", wwpn_pool="ORB4-WWPN-A",vsan_name="ORB4-VSAN-A",fabric="A",qos_pol="FC")
configure_vhba_templates(handle, org="ORB4ESX",description="vHBA Template for Tower ESX SAN Fabric B",
                         name="ORB4DEV-HBA-B", wwpn_pool="ORB4-WWPN-B",vsan_name="ORB4-VSAN-B",fabric="B",qos_pol="FC")


configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side A",
                         "DEV-MGMT-A","ORB4_MAC-A","9000","MGMT","CDP-ENA-LNK-DOWN","ORB4ESX-MGMT_1001","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Management vNIC side B",
                         "DEV-MGMT-B","ORB4_MAC-B","9000","MGMT","CDP-ENA-LNK-DOWN","ORB4ESX-MGMT_1001","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side A",
                         "DEV-VMT-A","ORB4_MAC-A","9000","VMOTION","CDP-ENA-LNK-DOWN","ORB4ESX-VMOTION_1002","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX vMotion vNIC side B",
                         "DEV-VMT-B","ORB4_MAC-B","9000","VMOTION","CDP-ENA-LNK-DOWN","ORB4ESX-VMOTION_1002","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side A",
                         "DEV-BKP-A","ORB4_MAC-A","9000","BKP","CDP-ENA-LNK-DOWN","ORB4ESX-BACKUP_1003","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX Backup vNIC side B",
                         "DEV-BKP-B","ORB4_MAC-B","9000","BKP","CDP-ENA-LNK-DOWN","ORB4ESX-BACKUP_1003","B")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side A",
                         "DEV-NFS-A","ORB4_MAC-A","9000","NFS","CDP-ENA-LNK-DOWN","ORB4ESX-NFS_1004","A")
configure_vnic_templates(handle, "ORB4ESX","vNIC Template for PROD Tower ESX NFS vNIC side B",
                         "DEV-NFS-B","ORB4_MAC-B","9000","NFS","CDP-ENA-LNK-DOWN","ORB4ESX-NFS_1004","B")


for vlan_id in akl_vlan:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for Tower ESX vMotion vNIC side A",
                                name="DEV-APP-A",mac_pool="ORB4_MAC-A",mtu="9000",qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="ORB4ESX_VLAN_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="ORB4ESX",
                                desc="vNIC Template for Tower ESX vMotion vNIC side B",
                                name="DEV-APP-B", mac_pool="ORB4_MAC-B", mtu="9000", qos_pol="APP",
                                network_pol="CDP-ENA-LNK-DOWN", vlan_name="ORB4ESX_VLAN_{}".format(vlan_id_cleaned),
                                fabric="B")

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
                                  wwpn_pool="ORB4-WWPN-B",
                                  qos_pol="FC",
                                  wwnn_pool_name="ORB4-WWNN")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-MGMT-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC1",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="MGMT",
                                  vnic_order="3")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-VMT-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC2",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-APP-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC3",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="APP",
                                  vnic_order="5")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-BKP-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC4",
                                  description="Production Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="NFS",
                                  vnic_order="6")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-NFS-A",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC5",
                                  description="NFS vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="A",
                                  mac_pool="ORB4ESX-MAC-A",
                                  qos_pol="NFS",
                                  vnic_order="7")


configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-MGMT-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC6",
                                  description="MGMT vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="MGMT",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-VMT-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC7",
                                  description="vMotion vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="VMOTION",
                                  vnic_order="9")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-APP-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC8",
                                  description="App vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="APP",
                                  vnic_order="10")
configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-BKP-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC9",
                                  description="Backup vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="BKP",
                                  vnic_order="11")

configure_lan_connectivity_policy(handle, organisation="org-root/org-ORB4ESX",
                                  vnic_template_name="DEV-NFS-B",
                                  name="ORB4DEV-CON",
                                  vnic_name="vNIC10",
                                  description="NFS vNIC",
                                  nw_control_pol="CDP-ENA-LNK-DOWN",
                                  switch_side="B",
                                  mac_pool="ORB4ESX-MAC-B",
                                  qos_pol="NFS",
                                  vnic_order="12")

configure_service_profile_template(handle, name="ORB4DEV",
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
                                   sol_policy_name="",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="ORB4ESX"
                                   )

create_sp_from_template(handle, start_sp_value=001, sp_quantity=4,sp_name_prefix="ORB4PRDESX",org="ORB4ESX",
                        template_name="ORB4PRD")



create_sp_from_template(handle, start_sp_value=001, sp_quantity=2,sp_name_prefix="ORB4DEVESX",org="ORB4ESX",
                        template_name="ORB4DEV")