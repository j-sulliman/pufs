from ucs_main import query_ucs_class, ucs_logon
import pandas as pd

handle = ucs_logon(ip_addr="192.168.2.114", usr="ucspe", pw="ucspe")

writer = pd.ExcelWriter('Tower_UCS_AS_Built.xlsx')

server_dict = []
rack_servers = query_ucs_class(handle,ucs_class='computeRackUnit')
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
for vnic in vnics:
    print(vnic)
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
for fi in fis:
    print(fi)
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
fi_df.to_excel(writer, sheet_name='Fabric Interconnects', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


fw_dict = []
psus = query_ucs_class(handle, ucs_class='equipmentPsu')
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



fc_int_list = []
fc_ints = query_ucs_class(handle, ucs_class='fabricFcVsanPortEp')
for fc in fc_ints:
    temp_dict = {}
    temp_dict["admin_state"] = fc.admin_state
    temp_dict['oper_state'] = fc.oper_state
    temp_dict['dn'] = fc.ep_dn
    temp_dict['switch_id'] = fc.switch_id
    temp_dict['transport'] = fc.transport
    fc_int_list.append(temp_dict)
fc_df = pd.DataFrame.from_dict(fc_int_list)
fc_df.to_excel(writer, sheet_name='FC Interfaces', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)


vsans_dict = []
vsans = query_ucs_class(handle, ucs_class='fabricVsan')
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
for fw in fws:
    temp_dict = {}
    temp_dict["type"] = fw.type
    temp_dict['dn'] = fw.dn
    temp_dict['package_version'] = fw.package_version
    temp_dict['version'] = fw.version
    vlans_dict.append(temp_dict)
fw_df = pd.DataFrame.from_dict(fw_dict)
fw_df.to_excel(writer, sheet_name='Running Firmware', header=True,
                   index=True, index_label=None, startrow=0, startcol=0, freeze_panes=None)

writer.save()
