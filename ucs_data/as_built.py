from ucs_main import query_ucs_class, ucs_logon
import pandas as pd

handle = ucs_logon(ip_addr="192.168.2.114", usr="ucspe", pw="ucspe")

writer = pd.ExcelWriter('Tower_UCS_AS_Built.xlsx')

server_dict = []
rack_servers = query_ucs_class(handle,ucs_class='computeRackUnit')
print('Found {} rack servers... check Servers sheet for detail'.format(len(rack_servers)))
for rack_server in rack_servers:
    temp_dict = {}
    temp_dict["server_serial"] = rack_server.serial
    temp_dict['model'] = rack_server.model
    temp_dict['oper_state'] = rack_server.oper_state
    temp_dict['memory'] = rack_server.total_memory
    temp_dict['cpus'] = rack_server.num_of_cpus
    temp_dict['vnics'] = rack_server.num_of_eth_host_ifs
    temp_dict['svr_id'] = rack_server.rn
    temp_dict['avail_paths'] = rack_server.conn_status
    temp_dict['service_profile'] = rack_server.assigned_to_dn
    temp_dict['association'] = rack_server.association
    server_dict.append(temp_dict)
server_df = pd.DataFrame.from_dict(server_dict)
server_df.to_excel(writer, sheet_name='Servers', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


service_profile_dict = []
service_profiles = query_ucs_class(handle, ucs_class='lsServer')
print('Found {} Service Profiles... check Service Profiles sheet for detail'.format(len(service_profiles)))
for sp in service_profiles:
    temp_dict = {}
    temp_dict["dn"] = sp.dn
    temp_dict['pn_dn'] = sp.pn_dn
    temp_dict['oper_src_templ_name'] = sp.oper_src_templ_name
    temp_dict['oper_state'] = sp.oper_state
    temp_dict['fsm_progr'] = sp.fsm_progr
    temp_dict['oper_scrub_policy_name'] = sp.oper_scrub_policy_name
    temp_dict['oper_bios_profile_name'] = sp.oper_bios_profile_name
    temp_dict['oper_boot_policy_name'] = sp.oper_boot_policy_name
    temp_dict['oper_maint_policy_name'] = sp.oper_maint_policy_name
    temp_dict['oper_host_fw_policy_name'] = sp.oper_host_fw_policy_name
    temp_dict['oper_local_disk_policy_name'] = sp.oper_local_disk_policy_name
    temp_dict['oper_ext_ip_pool_name'] = sp.oper_ext_ip_pool_name
    temp_dict['oper_ident_pool_name'] = sp.oper_ident_pool_name
    temp_dict['assoc_state'] = sp.assoc_state
    service_profile_dict.append(temp_dict)
sp_df = pd.DataFrame.from_dict(service_profile_dict)
sp_df.to_excel(writer, sheet_name='Service Profiles', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


vnics_dict = []
vnics = query_ucs_class(handle, ucs_class='vnicEther')
print('Found {} vNICs... check vNICs sheet for detail'.format(len(vnics)))
for vnic in vnics:
    temp_dict = {}
    temp_dict["dn"] = vnic.dn
    temp_dict['oper_adaptor_profile_name'] = vnic.oper_adaptor_profile_name
    temp_dict['addr'] = vnic.addr
    #temp_dict['equipmentDn'] = vnic.equipmentDn
    temp_dict['oper_ident_pool_name'] = vnic.oper_ident_pool_name
    temp_dict['mtu'] = vnic.mtu
    temp_dict['name'] = vnic.name
    temp_dict['oper_nw_ctrl_policy_name'] = vnic.oper_nw_ctrl_policy_name
    temp_dict['oper_nw_templ_name'] = vnic.oper_nw_templ_name
    temp_dict['oper_order'] = vnic.oper_order
    temp_dict['oper_qos_policy_name'] = vnic.oper_qos_policy_name
    temp_dict['oper_speed'] = vnic.oper_speed
    temp_dict['switch_id'] = vnic.switch_id
    #temp_dict['oper_vnet_name'] = vnic.oper_vnet_name
    vnics_dict.append(temp_dict)
vnic_df = pd.DataFrame.from_dict(vnics_dict)
vnic_df.to_excel(writer, sheet_name='vNICs', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


fi_dict = []
fis = query_ucs_class(handle, ucs_class='networkElement')
print('Found {} FI Management addresses... check Fabric Interconnect Management sheet for detail'.format(len(fis)))
for fi in fis:
    temp_dict = {}
    temp_dict["dn"] = fi.dn
    temp_dict['total_memory'] = fi.total_memory
    temp_dict['serial'] = fi.serial
    temp_dict['operability'] = fi.operability
    temp_dict['oob_if_gw'] = fi.oob_if_gw
    temp_dict['oob_if_ip'] = fi.oob_if_ip
    temp_dict['oob_if_mask'] = fi.oob_if_mask
    fi_dict.append(temp_dict)
fi_df = pd.DataFrame.from_dict(fi_dict)
fi_df.to_excel(writer, sheet_name='Fabric Interconnect Management', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


fw_dict = []
psus = query_ucs_class(handle, ucs_class='equipmentPsu')
print('Found {} Power Supplies... check Power Supply Health sheet for detail'.format(len(psus)))
for psu in psus:
    temp_dict = {}
    temp_dict["type"] = psu.type
    temp_dict['dn'] = psu.dn
    temp_dict['model'] = psu.model
    temp_dict['operability'] = psu.operability
    temp_dict['wattage'] = psu.psu_wattage
    temp_dict['thermal_status'] = psu.thermal
    temp_dict['voltage_statuss'] = psu.voltage
    fw_dict.append(temp_dict)
psu_df = pd.DataFrame.from_dict(fw_dict)
psu_df.to_excel(writer, sheet_name='Power Supply Health', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


sfp_dict = []
sfps = query_ucs_class(handle, ucs_class='equipmentXcvr')
print('Found {} Transceivers... check Interface Transceivers sheet for detail'.format(len(sfps)))
for sfp in sfps:
    temp_dict = {}
    temp_dict["type"] = sfp.type
    temp_dict['dn'] = sfp.dn
    temp_dict['model'] = sfp.model
    temp_dict['operability'] = sfp.serial
    sfp_dict.append(temp_dict)
sfp_df = pd.DataFrame.from_dict(sfp_dict)
sfp_df.to_excel(writer, sheet_name='Interface Transceivers', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)



eth_int_list = []
eth_ints = query_ucs_class(handle, ucs_class='swEthLanEp')
print('Found {} Uplinks... check Uplink Interfaces sheet for detail'.format(len(eth_ints)))
for eth in eth_ints:
    temp_dict = {}
    temp_dict["admin_state"] = eth.admin_state
    temp_dict["admin_speed"] = eth.admin_speed
    temp_dict['pc_id'] = eth.pc_id
    temp_dict['dn'] = eth.dn
    temp_dict['switch_id'] = eth.switch_id
    temp_dict['transport'] = eth.transport
    temp_dict['port_id'] = eth.port_id
    eth_int_list.append(temp_dict)
eth_int_df = pd.DataFrame.from_dict(eth_int_list)
eth_int_df.to_excel(writer, sheet_name='Uplink Interfaces', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


fc_int_list = []
fc_ints = query_ucs_class(handle, ucs_class='swFcSanEp')
print('Found {} FC Uplinks... check FC Interfaces sheet for detail'.format(len(fc_ints)))
for fc in fc_ints:
    temp_dict = {}
    temp_dict["admin_state"] = fc.admin_state
    temp_dict["admin_speed"] = fc.admin_speed
    temp_dict['fill_pattern'] = fc.fill_pattern
    temp_dict['dn'] = fc.dn
    temp_dict['switch_id'] = fc.switch_id
    temp_dict['transport'] = fc.transport
    temp_dict['port_vsan_id'] = fc.port_vsan_id
    fc_int_list.append(temp_dict)
fc_df = pd.DataFrame.from_dict(fc_int_list)
fc_df.to_excel(writer, sheet_name='FC Interfaces', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


vsans_dict = []
vsans = query_ucs_class(handle, ucs_class='fabricVsan')
print('Found {} VSANs... check VSAN Status sheet for detail'.format(len(vsans)))
for vsan in vsans:
    temp_dict = {}
    temp_dict["dn"] = vsan.dn
    temp_dict['fcoe_vlan'] = vsan.fcoe_vlan
    temp_dict['vsan_id'] = vsan.id
    temp_dict['name'] = vsan.name
    temp_dict['switch_id'] = vsan.switch_id
    temp_dict['type'] = vsan.type
    vsans_dict.append(temp_dict)
vsan_df = pd.DataFrame.from_dict(vsans_dict)
vsan_df.to_excel(writer, sheet_name='VSAN Status', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


vlans_dict = []
vlans = query_ucs_class(handle, ucs_class='fabricVlan')
print('Found {} VLANs... check VLAN Status sheet for detail'.format(len(vlans)))
for vlan in vlans:
    temp_dict = {}
    temp_dict["Operating_State"] = vlan.oper_state
    temp_dict['dn'] = vlan.dn
    temp_dict['vlan_id'] = vlan.id
    temp_dict['switch_id'] = vlan.switch_id
    vlans_dict.append(temp_dict)
vlan_df = pd.DataFrame.from_dict(vlans_dict)
vlan_df.to_excel(writer, sheet_name='VLAN Status', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


fw_dict = []
fws = query_ucs_class(handle, ucs_class='firmwareRunning')
print('Found {} Running Firmware ... check Running Firmware sheet for detail'.format(len(fws)))
for fw in fws:
    temp_dict = {}
    temp_dict["type"] = fw.type
    temp_dict['dn'] = fw.dn
    temp_dict['package_version'] = fw.package_version
    temp_dict['version'] = fw.version
    fw_dict.append(temp_dict)
fw_df = pd.DataFrame.from_dict(fw_dict)
fw_df.to_excel(writer, sheet_name='Running Firmware', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


mgmt_ip_list = []
mgt_ips = query_ucs_class(handle, ucs_class='ippoolAddr')
print('Found {} KVM Addresses... check Management IP Addresses sheet for detail'.format(len(mgt_ips)))
for ip in mgt_ips:
    temp_dict = {}
    temp_dict['assigned_to_dn'] = ip.assigned_to_dn
    temp_dict['assigned'] = ip.assigned
    temp_dict['id'] = ip.id
    mgmt_ip_list.append(temp_dict)
mgt_ips_df = pd.DataFrame.from_dict(mgmt_ip_list)
mgt_ips_df.to_excel(writer, sheet_name='Management IP Addresses', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


license_list = []
licenses = query_ucs_class(handle, ucs_class='licenseInstance')
print('Found {} Licenses... check License Status sheet for detail'.format(len(licenses)))
for license in licenses:
    temp_dict = {}
    temp_dict['feature'] = license.feature
    temp_dict['sku'] = license.sku
    temp_dict['peer_status'] = license.peer_status
    temp_dict['scope'] = license.scope
    temp_dict['defined_quantity'] = license.def_quant
    temp_dict['used_quantity'] = license.used_quant
    temp_dict['grace_period_used'] = license.grace_period_used
    license_list.append(temp_dict)
licenses_df = pd.DataFrame.from_dict(license_list)
licenses_df.to_excel(writer, sheet_name='License Status', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


qos_class_list = []
qos_classes = query_ucs_class(handle, ucs_class='qosclassEthClassified')
print('Found {} QoS Classes... check QoS Class Definitions sheet for detail'.format(len(qos_classes)))
for qos_class in qos_classes:
    temp_dict = {}
    temp_dict['bw_percent'] = qos_class.bw_percent
    temp_dict['cos'] = qos_class.cos
    temp_dict['priority'] = qos_class.priority
    temp_dict['mtu'] = qos_class.mtu
    temp_dict['weight'] = qos_class.weight
    qos_class_list.append(temp_dict)
qos_class_df = pd.DataFrame.from_dict(qos_class_list)
qos_class_df.to_excel(writer, sheet_name='QoS Class Definition', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


flex_flash_list = []
ssd_cards = query_ucs_class(handle, ucs_class='storageFlexFlashDrive')
print('Found {} SD Drives... check Local SD Card Status sheet for detail'.format(len(ssd_cards)))
for sd in ssd_cards:
    temp_dict = {}
    temp_dict['dn'] = sd.dn
    temp_dict['drive_state'] = sd.drive_state
    temp_dict['operability'] = sd.operability
    temp_dict['operation_state'] = sd.operation_state
    temp_dict['size'] = sd.size
    flex_flash_list.append(temp_dict)
ssd_cards_df = pd.DataFrame.from_dict(flex_flash_list)
ssd_cards_df.to_excel(writer, sheet_name='Local SD Card Status', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)
writer.save()
