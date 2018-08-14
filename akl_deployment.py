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

handle = ucs_logon(ip_addr="192.168.2.23", usr="ucspe", pw="ucspe")
configure_organisation(handle, name="AKL-VI-APP")

configure_mac_pools(handle, "AKL-VI-APP","AKL MAC Pool for Fabric A","AKL_VI_App_MAC-A","00:25:B5:3A:00:00", "00:25:B5:3A:00:FF")
configure_mac_pools(handle, "AKL-VI-APP","AKL MAC Pool for Fabric B","AKL_VI_App_MAC-B","00:25:B5:3B:00:00", "00:25:B5:3B:00:FF")

configure_uuid_pool(handle,'AKL-VI-APP',"AKL-VI-App-UUID","UUID Pool for Auckland Shared Edge Compute","sequential",
                    "0000-000000000256","0000-000000000001")
configure_maint_policy(handle, org="AKL-VI-APP",name="AKL-USER-ACK",reboot_pol="user-ack", descr="User Ack")
configure_host_fw_policy(handle, org="AKL-VI-APP",name="AKL-FW-3.2.3g",descr="3.2.3g")
configure_boot_policy(handle, "AKL-VI-APP","AKL-CDROM","Boot Policy for Auckland Shared Edge Compute")
configure_local_disk_conf_policy(handle, "AKL-VI-APP", "AKL-INT-CARD", "Local Disk Policy for Auckland Shared Edge Compute")
configure_bios_policy(handle, "AKL-VI-APP", "AKL-NO-QUIET", "Local Disk Policy for Auckland Shared Edge Compute")

configure_scrub_policy(handle, "AKL-VI-APP", "AKL-BIOS-Scrub", "Local Disk Policy for Auckland Shared Edge Compute")
configure_ip_pools(handle, "AKL-VI-APP","KVM Management IP Pool for Auckland Shared Edge Compute", "AKL-KVM", "10.233.178.16",
                   "10.233.178.47", "10.233.178.1", "sequential")
configure_qos_policy(handle, "AKL-VI-APP", "Platinum QoS Policy for Auckland Shared Edge Compute Application vNIC", "VI-APP-NET",
                     "platinum", "10240")
configure_qos_policy(handle, "AKL-VI-APP", "Gold QoS Policy for Auckland Shared Edge Compute Recover Point vNIC", "VI-RP",
                     "platinum", "10240")
configure_qos_policy(handle, "AKL-VI-APP", "Silver QoS Policy for Auckland Shared Edge Compute Management vNIC", "VI-MGMT",
                     "silver", "10240")
configure_qos_policy(handle, "AKL-VI-APP", "Bronze QoS Policy for Auckland Shared Edge Compute vMotion vNIC", "VI-VMOTION",
                     "silver", "10240")
configure_qos_policy(handle, "AKL-VI-APP", "FC QoS Policy for Auckland Shared Edge Compute FC vHBAs", "VI-FC",
                     "fc", "10240")
configure_cdp_pol(handle, "AKL-VI-APP","Network Control Policy for Auckland Shared Edge Compute vNICs", "AKL-CDP-EN")
configure_vsans(handle, name='AKL-VSAN-A', vsan_id='1280', fabric='A')
configure_vsans(handle, name='AKL-VSAN-B', vsan_id='1281',fabric='B')
configure_wwnn_pools(handle, org="org-root/org-AKL-VI-APP",wwnn_name="AKL-WWNN-POOL",description="Auckland WWNN Pool",
                     assignment_order="sequential",from_wwnn="20:00:20:25:B5:01:00:00",
                     to_wwnn="20:00:20:25:B5:01:00:FF")

configure_wwpn_pools(handle, org="AKL-VI-APP",description="WWPN Pool for Auckland Shared Edge Compute A Side (VSAN 1280)",
                     name="AKL-WWPN-A", wwpn_from="20:00:2A:25:b5:01:0a:00", wwpn_to="20:00:2A:25:B5:01:0A:FF")
configure_wwpn_pools(handle, org="AKL-VI-APP",description="WWPN Pool for Auckland Shared Edge Compute B Side (VSAN 1281)",
                     name="AKL-WWPN-B", wwpn_from="20:00:2B:25:b5:01:0b:00", wwpn_to="20:00:2B:25:B5:01:0b:FF")
configure_vhba_templates(handle, org="AKL-VI-APP", description="vHBA Template for Auckland Shared Edge Compute SAN Fabric A",
                         name="AKL-HBA-A", wwpn_pool="AKL-WWPN-A",vsan_name="AKL-VSAN-A",fabric="A",qos_pol="VI-FC")
configure_vhba_templates(handle, org="AKL-VI-APP",description="vHBA Template for Auckland Shared Edge Compute SAN Fabric B",
                         name="AKL-HBA-B", wwpn_pool="AKL-WWPN-B",vsan_name="AKL-VSAN-B",fabric="B",qos_pol="VI-FC")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute Management vNIC side A",
                         "AKL-VI-MGMT-A","AKL_VI_App_MAC-A","9000","VI-MGMT","AKL-CDP-EN","VI-MGMT_1112","A")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute Management vNIC side B",
                         "AKL-VI-MGMT-B","AKL_VI_App_MAC-B","9000","VI-MGMT","AKL-CDP-EN","VI-MGMT_1112","B")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                         "AKL-VI-VMOTION-A","AKL_VI_App_MAC-A","9000","VI-VMOTION","AKL-CDP-EN","VI-VMOTION_1111","A")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                         "AKL-VI-VMOTION-B","AKL_VI_App_MAC-B","9000","VI-VMOTION","AKL-CDP-EN","VI-VMOTION_1111","B")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                         "AKL-VI-RP-A","AKL_VI_App_MAC-A","9000","VI-RP","AKL-CDP-EN","VI-RP_1114","A")
configure_vnic_templates(handle, "AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                         "AKL-VI-RP-B","AKL_VI_App_MAC-B","9000","VI-RP","AKL-CDP-EN","VI-RP_1114","B")
for vlan_id in akl_vlan:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_vlans(handle, vlan_id, 'AKL_VI_App_VLAN')
    configure_app_vnic_template(handle, org="AKL-VI-APP",
                                desc="vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                                name="AKL-VI-APP-A",mac_pool="AKL_VI_App_MAC-A",mtu="9000",qos_pol="VI-APP-NET",
                                network_pol="AKL-CDP-EN", vlan_name="AKL_VI_App_VLAN_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="AKL-VI-APP",
                                desc="vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                                name="AKL-VI-APP-B", mac_pool="AKL_VI_App_MAC-B", mtu="9000", qos_pol="VI-APP-NET",
                                network_pol="AKL-CDP-EN", vlan_name="AKL_VI_App_VLAN_{}".format(vlan_id_cleaned),
                                fabric="B")

configure_vlans(handle, "1112", 'VI-MGMT')
configure_vlans(handle, "1111", 'VI-VMOTION')
configure_vlans(handle, "1114", 'VI-RP')
configure_san_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  name="AKL-VI-APP-SCON",
                                  vhba_name="vHBA0",
                                  vhba_template_name="AKL-HBA-A",
                                  vsan_name="AKL-VSAN-A",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="A",
                                  vHBA_order="1",
                                  adapter_profile="VMWare",
                                  wwpn_pool="AKL-WWPN-A",
                                  qos_pol="VI-FC",
                                  wwnn_pool_name="AKL-WWNN-POOL")

configure_san_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  name="AKL-VI-APP-SCON",
                                  vhba_name="vHBA1",
                                  vhba_template_name="AKL-HBA-B",
                                  vsan_name="AKL-VSAN-B",
                                  description="Auckland SAN Connectivity Policy",
                                  switch_side="B",
                                  vHBA_order="2",
                                  adapter_profile="VMWare",
                                  wwpn_pool="AKL-WWPN-B",
                                  qos_pol="VI-FC",
                                  wwnn_pool_name="AKL-WWNN-POOL")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-MGMT-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC1",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="VI-MGMT",
                                  vnic_order="3")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-VMOTION-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC2",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-APP-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC3",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="AKL-VI-APP",
                                  vnic_order="5")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-RP-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC4",
                                  description="AKL VI RP vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="AKL-VI-RP",
                                  vnic_order="6")


configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-MGMT-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC5",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="VI-MGMT",
                                  vnic_order="7")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-VMOTION-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC6",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-APP-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC7",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="AKL-VI-APP",
                                  vnic_order="9")

configure_lan_connectivity_policy(handle, organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-RP-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC8",
                                  description="AKL VI RP vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="AKL-VI-RP",
                                  vnic_order="10")

configure_service_profile_template(handle, name="AKL-VI-APPLICATION_1",
                                   type= "initial-template",
                                   resolve_remote= "yes",
                                   descr="AKL VI APP Descr",
                                   usr_lbl="",src_templ_name="",
                                   ext_ip_state="pooled",
                                   ext_ip_pool_name="AKL-KVM",
                                   ident_pool_name="AKL-VI-App-UUID",
                                   agent_policy_name='',
                                   bios_profile_name="AKL-NO-QUIET",
                                   boot_policy_name="AKL-CDROM",
                                   dynamic_con_policy_name="",
                                   host_fw_policy_name="AKL-FW-3.2.3g",
                                   kvm_mgmt_policy_name="",
                                   lan_conn_policy_name="AKL-VI-APP-CON",
                                   san_conn_policy_name="AKL-VI-APP-SCON",
                                   local_disk_policy_name="AKL-INT-CARD",
                                   maint_policy_name="AKL-USER-ACK",
                                   mgmt_access_policy_name="",
                                   mgmt_fw_policy_name="",
                                   power_policy_name="default",
                                   scrub_policy_name="AKL-BIOS-Scrub",
                                   sol_policy_name="",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="AKL-VI-APP"
                                   )


create_sp_from_template(handle, start_sp_value=611, sp_quantity=12,sp_name_prefix="csvipresx",org="AKL-VI-APP",
                        template_name="AKL-VI-APPLICATION_1")