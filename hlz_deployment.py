from ucs_main import configure_organisation, configure_mac_pools,configure_uuid_pool, configure_maint_policy
from ucs_main import configure_host_fw_policy, configure_boot_policy, configure_local_disk_conf_policy
from ucs_main import configure_bios_policy, configure_scrub_policy, configure_ip_pools, configure_qos_policy
from ucs_main import configure_cdp_pol, configure_vsans, configure_wwnn_pools, configure_wwpn_pools
from ucs_main import configure_vhba_templates, configure_vnic_templates, configure_vlans, configure_app_vnic_template
from ucs_main import configure_service_profile_template, configure_lan_connectivity_policy
from ucs_main import configure_san_connectivity_policy, create_sp_from_template, ucs_logon


hlz_vlans = ["1031","1032","1033","1034","1035","1036","1037","1038","1039","1040","1041","1042","1043","1044","1045",
             "1046","1047","1048","1049","1050","1051","1052","1053","1054","1059","1061","1065","1070","1071","1078",
             "1087", "1088","1090","2063","2064","2067", "2068","2071","2088","2104","2112","3000","3002",
             "3024", "3025", "3030","3031","503","514","537"]

handle = ucs_logon(ip_addr="192.168.2.26", usr="ucspe", pw="ucspe")


configure_organisation(handle, name="HLZ-VI-APP")


configure_mac_pools(handle, org="HLZ-VI-APP", description="AKL MAC Pool for Fabric A", name="HLZ-VI-APP-MAC-A",
                    mac_from="00:25:B5:3A:01:00", mac_to="00:25:B5:3A:01:FF")
configure_mac_pools(handle, org="HLZ-VI-APP", description="AKL MAC Pool for Fabric B", name="HLZ-VI-APP-MAC-B",
                    mac_from="00:25:B5:3B:01:00", mac_to="00:25:B5:3B:01:FF")


configure_uuid_pool(handle, org='HLZ-VI-APP', name="HLZ-VI-APP-UUID",
                    descr="UUID Pool for Hamilton Shared Edge Compute", assgn_order="sequential",
                    uuid_from="0000-000000000001", uuid_to="0000-000000000256")
configure_maint_policy(handle, org="HLZ-VI-APP", name="HLZ-USER-ACK", reboot_pol="user-ack", descr="User Ack")
configure_host_fw_policy(handle, org="HLZ-VI-APP",name="HLZ-FW-3.2.3g",descr="3.2.3g")
configure_boot_policy(handle, org="HLZ-VI-APP", name="HLZ-CDROM", descr="Boot Policy for Hamilton Shared Edge Compute")

configure_local_disk_conf_policy(handle, org="HLZ-VI-APP", name="HLZ-INT-CARD",
                                 descr="Local Disk Policy for Hamilton Shared Edge Compute")

configure_bios_policy(handle, org="HLZ-VI-APP", name="HLZ-NO-QUIET",
                      descr="Local Disk Policy for Hamilton Shared Edge Compute")


configure_scrub_policy(handle, org="HLZ-VI-APP", name="HLZ-BIOS-SCRUB",
                       descr="Local Disk Policy for Hamilton Shared Edge Compute")


configure_ip_pools(handle, org="HLZ-VI-APP", description="KVM Management IP Pool for Hamilton Shared Edge Compute",
                   name="HLZ-KVM", ip_from="10.233.178.76",
                   ip_to="10.233.178.107", ip_gw="10.233.178.1", assignment_ordr="sequential")

configure_qos_policy(handle, org="HLZ-VI-APP",
                     description="Platinum QoS Policy for Hamilton Shared Edge Compute Application vNIC",
                     name="VI-APP-NET", priority="platinum", burst="10240")
configure_qos_policy(handle, org="HLZ-VI-APP",
                     description="Gold QoS Policy for Hamilton Shared Edge Compute Recover Point vNIC", name="VI-RP",
                     priority="platinum", burst="10240")
configure_qos_policy(handle, org="HLZ-VI-APP",
                     description="Silver QoS Policy for Hamilton Shared Edge Compute Management vNIC", name="VI-MGMT",
                     priority="silver", burst="10240")
configure_qos_policy(handle, org="HLZ-VI-APP",
                     description="Bronze QoS Policy for Hamilton Shared Edge Compute vMotion vNIC", name="VI-VMOTION",
                     priority="silver", burst="10240")

configure_qos_policy(handle, org="HLZ-VI-APP",
                     description="FC QoS Policy for Hamilton Shared Edge Compute FC vHBAs", name="VI-FC",
                     priority="fc", burst="10240")
configure_cdp_pol(handle, "HLZ-VI-APP","Network Control Policy for Hamilton Shared Edge Compute vNICs", "HLZ-CDP-EN")
configure_vsans(handle, name='HLZ-VSAN-A', vsan_id='1282', fabric='A')
configure_vsans(handle, name='HLZ-VSAN-B', vsan_id='1283',fabric='B')
configure_wwnn_pools(handle, org="org-root/org-HLZ-VI-APP",wwnn_name="HLZ-WWNN-POOL",description="Hamilton WWNN Pool",
                     assignment_order="sequential",from_wwnn="20:00:30:25:B5:01:00:00",
                     to_wwnn="20:00:30:25:B5:01:00:FF")

configure_wwpn_pools(handle, org="HLZ-VI-APP",description="WWPN Pool for Hamilton Shared Edge Compute A Side (VSAN 1280)",
                     name="HLZ-WWPN-A", wwpn_from="20:00:2A:25:b5:02:0a:00", wwpn_to="20:00:2A:25:B5:02:0A:FF")
configure_wwpn_pools(handle, org="HLZ-VI-APP",description="WWPN Pool for Hamilton Shared Edge Compute B Side (VSAN 1281)",
                     name="HLZ-WWPN-B", wwpn_from="20:00:2B:25:b5:02:0b:00", wwpn_to="20:00:2B:25:B5:02:0b:FF")
configure_vhba_templates(handle, org="HLZ-VI-APP", description="vHBA Template for Hamilton Shared Edge Compute SAN Fabric A",
                         name="HLZ-HBA-A", wwpn_pool="HLZ-WWPN-A",vsan_name="HLZ-VSAN-A",fabric="A",qos_pol="VI-FC")
configure_vhba_templates(handle, org="HLZ-VI-APP",description="vHBA Template for Hamilton Shared Edge Compute SAN Fabric B",
                         name="HLZ-HBA-B", wwpn_pool="HLZ-WWPN-B",vsan_name="HLZ-VSAN-B",fabric="B",qos_pol="VI-FC")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute Management vNIC side A",
                         name="HLZ-VI-MGMT-A", mac_pool="HLZ-VI-APP-MAC-A", mtu="9000", qos_pol="VI-MGMT",
                         network_ctrl_pol="HLZ-CDP-EN", vlan_name="VI-MGMT_1112", switch="A")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute Management vNIC side B",
                         name="HLZ-VI-MGMT-B", mac_pool="HLZ-VI-APP-MAC-B", mtu="9000", qos_pol="VI-MGMT",
                         network_ctrl_pol="HLZ-CDP-EN", vlan_name="VI-MGMT_1112", switch="B")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side A",
                         name="HLZ-VI-VMOTION-A",mac_pool="HLZ-VI-APP-MAC-A",mtu="9000",qos_pol="VI-VMOTION",
                         network_ctrl_pol="HLZ-CDP-EN",vlan_name="VI-VMOTION_1111",switch="A")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side B",
                         name="HLZ-VI-VMOTION-B", mac_pool="HLZ-VI-APP-MAC-B", mtu="9000", qos_pol="VI-VMOTION",
                         network_ctrl_pol="HLZ-CDP-EN", vlan_name="VI-VMOTION_1111", switch="B")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side A",
                         name="HLZ-VI-RP-A", mac_pool="HLZ-VI-APP-MAC-A", mtu="9000", qos_pol="VI-RP",
                         network_ctrl_pol="HLZ-CDP-EN", vlan_name="VI-RP_1114", switch="A")
configure_vnic_templates(handle, org="HLZ-VI-APP",
                         description="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side B",
                         name="HLZ-VI-RP-B", mac_pool="HLZ-VI-APP-MAC-B", mtu="9000", qos_pol="VI-RP",
                         network_ctrl_pol="HLZ-CDP-EN", vlan_name="VI-RP_1114", switch="B")
for vlan_id in hlz_vlans:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_vlans(handle, vlan_id, 'HLZ-VI-APP-VLAN')
    configure_app_vnic_template(handle, org="HLZ-VI-APP",
                                desc="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side A",
                                name="HLZ-VI-APP-A",mac_pool="HLZ-VI-APP-MAC-A",mtu="9000",qos_pol="VI-APP-NET",
                                network_pol="HLZ-CDP-EN", vlan_name="HLZ-VI-APP-VLAN_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(handle, org="HLZ-VI-APP",
                                desc="vNIC Template for Hamilton Shared Edge Compute vMotion vNIC side B",
                                name="HLZ-VI-APP-B", mac_pool="HLZ-VI-APP-MAC-B", mtu="9000", qos_pol="VI-APP-NET",
                                network_pol="HLZ-CDP-EN", vlan_name="HLZ-VI-APP-VLAN_{}".format(vlan_id_cleaned),
                                fabric="B")

configure_vlans(handle, vlan_id="1112", vlan_name='VI-MGMT')
configure_vlans(handle, vlan_id="1111", vlan_name='VI-VMOTION')
configure_vlans(handle, vlan_id="1114", vlan_name='VI-RP')
configure_san_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  name="HLZ-VI-APP-SCON",
                                  vhba_name="vHBA0",
                                  vhba_template_name="HLZ-HBA-A",
                                  vsan_name="HLZ-VSAN-A",
                                  description="Hamilton SAN Connectivity Policy",
                                  switch_side="A",
                                  vHBA_order="1",
                                  adapter_profile="VMWare",
                                  wwpn_pool="HLZ-WWPN-A",
                                  qos_pol="VI-FC",
                                  wwnn_pool_name="HLZ-WWNN-POOL")

configure_san_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  name="HLZ-VI-APP-SCON",
                                  vhba_name="vHBA1",
                                  vhba_template_name="HLZ-HBA-B",
                                  vsan_name="HLZ-VSAN-B",
                                  description="Hamilton SAN Connectivity Policy",
                                  switch_side="B",
                                  vHBA_order="2",
                                  adapter_profile="VMWare",
                                  wwpn_pool="HLZ-WWPN-B",
                                  qos_pol="VI-FC",
                                  wwnn_pool_name="HLZ-WWNN-POOL")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-MGMT-A",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC1",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="A",
                                  mac_pool="HLZ-VI-APP-MAC-A",
                                  qos_pol="VI-MGMT",
                                  vnic_order="3")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-VMOTION-A",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC2",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="A",
                                  mac_pool="HLZ-VI-APP-MAC-A",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-APP-A",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC3",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="A",
                                  mac_pool="HLZ-VI-APP-MAC-A",
                                  qos_pol="HLZ-VI-APP",
                                  vnic_order="5")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-RP-A",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC4",
                                  description="AKL VI RP vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="A",
                                  mac_pool="HLZ-VI-APP-MAC-A",
                                  qos_pol="HLZ-VI-RP",
                                  vnic_order="6")


configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-MGMT-B",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC5",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="B",
                                  mac_pool="HLZ-VI-APP-MAC-B",
                                  qos_pol="VI-MGMT",
                                  vnic_order="7")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-VMOTION-B",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC6",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="B",
                                  mac_pool="HLZ-VI-APP-MAC-B",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="8")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-APP-B",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC7",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="B",
                                  mac_pool="HLZ-VI-APP-MAC-B",
                                  qos_pol="HLZ-VI-APP",
                                  vnic_order="9")

configure_lan_connectivity_policy(handle, organisation="org-root/org-HLZ-VI-APP",
                                  vnic_template_name="HLZ-VI-RP-B",
                                  name="HLZ-VI-APP-LCON",
                                  vnic_name="vNIC8",
                                  description="AKL VI RP vNIC",
                                  nw_control_pol="HLZ-CDP-EN",
                                  switch_side="B",
                                  mac_pool="HLZ-VI-APP-MAC-B",
                                  qos_pol="HLZ-VI-RP",
                                  vnic_order="10")

configure_service_profile_template(handle, name="HLZ-VI-APPLICATION",
                                   type= "initial-template",
                                   resolve_remote= "yes",
                                   descr="AKL VI APP Descr",
                                   usr_lbl="",src_templ_name="",
                                   ext_ip_state="pooled",
                                   ext_ip_pool_name="HLZ-KVM",
                                   ident_pool_name="HLZ-VI-APP-UUID",
                                   agent_policy_name='',
                                   bios_profile_name="HLZ-NO-QUIET",
                                   boot_policy_name="HLZ-CDROM",
                                   dynamic_con_policy_name="",
                                   host_fw_policy_name="HLZ-FW-3.2.3g",
                                   kvm_mgmt_policy_name="",
                                   lan_conn_policy_name="HLZ-VI-APP-LCON",
                                   san_conn_policy_name="HLZ-VI-APP-SCON",
                                   local_disk_policy_name="HLZ-INT-CARD",
                                   maint_policy_name="HLZ-USER-ACK",
                                   mgmt_access_policy_name="",
                                   mgmt_fw_policy_name="",
                                   power_policy_name="default",
                                   scrub_policy_name="HLZ-BIOS-SCRUB",
                                   sol_policy_name="",
                                   stats_policy_name="default",
                                   vmedia_policy_name="",
                                   org="HLZ-VI-APP"
                                   )


create_sp_from_template(handle, start_sp_value=623, sp_quantity=11, sp_name_prefix="csvipresx", org="HLZ-VI-APP",
                        template_name="HLZ-VI-APPLICATION")