from ucsmsdk.ucshandle import UcsHandle
from colorama import Fore, Back, Style, init
init(autoreset=True)
'''
def ucs_logon(ip_addr="192.168.2.23", usr="ucspe", pw="ucspe"):
    handle = UcsHandle(ip_addr, usr, pw, port=443, secure=True)
    handle.get_auth_token()
    handle.login(auto_refresh=True)
    return handle

'''
def ucs_logon(ip_addr="192.168.2.23", usr="ucspe", pw="ucspe"):
    handle = UcsHandle(ip_addr, usr, pw)
    handle.login(auto_refresh=True)
    return handle


#handle.process_xml_elem(elem=ucsmethodfactory.config_find_dns_by_class_id(cookie=handle.cookie, class_id="LsServer",
#                                                                          in_filter=None))

#fcpool_filter = '(assigned, "yes", type="eq")'
#data = handle.query_classid(class_id="fcpoolInitiator", filter_str=fcpool_filter)


def configure_organisation(handle, name):
    from ucsmsdk.mometa.org.OrgOrg import OrgOrg
    mo = OrgOrg(parent_mo_or_dn="org-root", name=name)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Organisation {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Organisation {}. '.format(err, name))
        #data = handle.set_dump_xml()
        #print(data)


def configure_uuid_pool(handle, org, name, descr, assgn_order, uuid_to, uuid_from, pref = 'derived'):

    from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
    from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock

    mo = UuidpoolPool(parent_mo_or_dn="org-root/org-{}".format(org), policy_owner="local", prefix=pref,
                      descr=descr, assignment_order=assgn_order,
                      name=name)
    mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to=uuid_to, r_from=uuid_from)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'UUID {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, UUID {}. '.format(err, name))

        #data = handle.set_dump_xml()
        #print(data)


def configure_boot_policy(handle, org, name, descr):
    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
    from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
    from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
    from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
    from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage

    mo = LsbootPolicy(parent_mo_or_dn="org-root/org-{}".format(org), name=name, descr=descr,
                      reboot_on_update="no", policy_owner="local", enforce_vnic_name="yes", boot_mode="legacy")
    mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-local", lun_id="0", mapping_name="", order="1")
    mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="2")
    mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
    mo_2_1_1 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_2_1, order="2")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Boot Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Boot Policy {}. '.format(err, name))

def configure_local_disk_conf_policy(handle, org, name, descr):
    from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy

    mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn="org-root/org-{}".format(org), protect_config="yes", name=name,
                                      descr=descr, flex_flash_raid_reporting_state="enable",
                                      flex_flash_state="disable", policy_owner="local", mode="raid-mirrored")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Local Disk Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Local Disk Policy {}. '.format(err, name))

def configure_bios_policy(handle, org, name, descr, quiet_boot = 'disabled'):
    from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
    from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
    from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
    from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
    from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
    from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss

    mo = BiosVProfile(parent_mo_or_dn="org-root/org-{}".format(org), policy_owner="local", name=name, descr=descr,
                      reboot_on_update="no")
    mo_1 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
    mo_2 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="disabled")
    mo_3 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
    mo_4 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot=quiet_boot)
    mo_5 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'BIOS Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, BIOS Policy {}. '.format(err, name))


def configure_scrub_policy(handle, org, name, descr):
    from ucsmsdk.mometa.compute.ComputeScrubPolicy import ComputeScrubPolicy

    mo = ComputeScrubPolicy(parent_mo_or_dn="org-root/org-{}".format(org), flex_flash_scrub="no", name=name,
                            descr=descr, policy_owner="local", bios_settings_scrub="yes", disk_scrub="no")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Scrub Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Scrub Policy {}. '.format(err, name))


def configure_maint_policy(handle, org, name='', reboot_pol="user-ack", descr=''):
    from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

    mo = LsmaintMaintPolicy(parent_mo_or_dn="org-root/org-{}".format(org), uptime_disr=reboot_pol, name=name,
                            descr=descr, trigger_config="", soft_shutdown_timer="150-secs", sched_name="",
                            policy_owner="local")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Scrub Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Maintenance Policy {}. '.format(err, name))

def create_sp_from_template(handle, start_sp_value=611, sp_quantity=12, sp_name_prefix="csvipresx", org="AKL-VI-APP",
                            template_name="AKL-VI-APPLICATION_1"):
    from ucsmsdk.ucsmethodfactory import ls_instantiate_n_named_template
    from ucsmsdk.ucsbasetype import DnSet, Dn
    start_value = start_sp_value
    for sp in range(sp_quantity):
        dn_set = DnSet()
        dn = Dn()
        dn.attr_set("value", sp_name_prefix+str(start_value))
        dn_set.child_add(dn)
        start_value += 1

        elem = ls_instantiate_n_named_template(cookie=handle.cookie, dn="org-root/org-{}/ls-{}".format(org, template_name),
                                               in_error_on_existing="true", in_name_set=dn_set,
                                               in_target_org="org-root/org-{}".format(org), in_hierarchical="false")
        mo_list = handle.process_xml_elem(elem)


def configure_host_fw_policy(handle, org, name, descr):
    from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import FirmwareComputeHostPack
    from ucsmsdk.mometa.firmware.FirmwareExcludeServerComponent import FirmwareExcludeServerComponent

    mo = FirmwareComputeHostPack(parent_mo_or_dn="org-root/org-{}".format(org), ignore_comp_check="yes", name=name,
                                 descr=descr, stage_size="0", rack_bundle_version="", update_trigger="immediate",
                                 policy_owner="local", mode="staged", blade_bundle_version="",
                                 override_default_exclusion="yes")
    mo_1 = FirmwareExcludeServerComponent(parent_mo_or_dn=mo, server_component="local-disk")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Firmware Policy {} configured'.format(name))
    except Exception, err:
        print(Fore.YELLOW + 'Error: {}, Firmware Policy {}. '.format(err, name))


def configure_vlans(handle, vlan_id, vlan_name):
    from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none", name="{}_{}".format(vlan_name, vlan_id_cleaned),
                    id=vlan_id_cleaned,
                    mcast_policy_name="", policy_owner="local", default_net="no", pub_nw_name="",
                    compression_type="included")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'VLAN {} configured'.format(vlan_id_cleaned))
    except Exception, err:
        if "103" in err:
            print(Fore.YELLOW + 'Error: {}, VLAN {}. '.format(err, vlan_id_cleaned))
        else:
            print(Fore.YELLOW + 'Error: {}, VLAN {}. '.format(err, vlan_id_cleaned))




def configure_mac_pools(handle, org, description, name, mac_from, mac_to):
    from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
    from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

    mo = MacpoolPool(parent_mo_or_dn="org-root/org-{}".format(org), policy_owner="local", descr=description,
                     assignment_order="sequential", name=name)
    mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to=mac_to, r_from=mac_from)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'MAC Pool {} configured'.format(name))
    except Exception, err:
        print(Fore.RED + 'Error: {}, MAC Pool {}. '.format(err, name))


def configure_ip_pools(handle, org, description, name, ip_from, ip_to, ip_gw = "10.233.178.1", assignment_ordr = "sequential"):
    from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
    from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

    mo = IppoolPool(parent_mo_or_dn="org-root/org-{}".format(org), is_net_bios_enabled="disabled", name=name,
                    descr=description, policy_owner="local", ext_managed="internal", supports_dhcp="disabled",
                    assignment_order=assignment_ordr)
    mo_1 = IppoolBlock(parent_mo_or_dn=mo, to=ip_to, r_from=ip_from, def_gw=ip_gw)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'IP Pool {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure IP Pool {}. Does it already exist?'.format(name))
        #data = handle.set_dump_xml()
        #print(data)


def configure_qos_policy(handle, org, description, name, priority, burst):
    from ucsmsdk.mometa.epqos.EpqosDefinition import EpqosDefinition
    from ucsmsdk.mometa.epqos.EpqosEgress import EpqosEgress

    mo = EpqosDefinition(parent_mo_or_dn="org-root/org-{}".format(org), policy_owner="local", name=name,
                         descr=description)
    mo_1 = EpqosEgress(parent_mo_or_dn=mo, rate="line-rate", host_control="none", name="", prio=priority,
                       burst=burst)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'QoS Policy{} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure QoS Policy {}. Does it already exist?'.format(name))
        #data = handle.set_dump_xml()
        #print(data)


def configure_cdp_pol(handle, org, description, name):
    from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
    from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac

    mo = NwctrlDefinition(parent_mo_or_dn="org-root/org-{}".format(org), lldp_transmit="disabled", name=name,
                          lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local",
                          cdp="enabled", uplink_fail_action="link-down", descr=description)
    mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local", name="", descr="")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Network Control Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure CDP Policy {}. Does it already exist?'.format(name))
        #data = handle.set_dump_xml()
        #print(data)



def configure_wwnn_pools(handle, org="org-root/org-AKL-VI-APP",
                         wwnn_name="AKL-WWNN-Pool",
                         description="Auckland WWNN pool",
                         assignment_order="sequential",
                         from_wwnn="20:00:00:25:B5:00:00:00",
                         to_wwnn="20:00:00:25:B5:00:00:7F"):
    from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
    from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock

    mo = FcpoolInitiators(parent_mo_or_dn=org,
                          name=wwnn_name,
                          policy_owner="local",
                          descr=description,
                          assignment_order=assignment_order,
                          purpose="node-wwn-assignment")
    mo_1 = FcpoolBlock(parent_mo_or_dn=mo,
                       to=to_wwnn,
                       r_from=from_wwnn)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'WWNN Pool {} configured'.format(wwnn_name))
    except:
        print(Fore.YELLOW + 'Unable to configure WWNN Pool {}. Does it already exist?'.format(wwnn_name))


def configure_wwpn_pools(handle, org, description, name, wwpn_from, wwpn_to, assignment_ordr = "sequential"):
    from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
    from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock

    mo = FcpoolInitiators(parent_mo_or_dn="org-root/org-{}".format(org), name=name, policy_owner="local",
                          descr=description, assignment_order=assignment_ordr, purpose="port-wwn-assignment")
    mo_1 = FcpoolBlock(parent_mo_or_dn=mo, to=wwpn_to, r_from=wwpn_from)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'WWPN Pool {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure WWPN Pool {}. Does it already exist?'.format(name))
        #data = handle.set_dump_xml()
        #print(data)

def configure_vsans(handle, name='',
                    vsan_id='1280',
                    fabric='A'):
    from ucsmsdk.mometa.fabric.FabricVsan import FabricVsan

    mo = FabricVsan(parent_mo_or_dn="fabric/san/{}".format(fabric),
                    name=name,
                    fcoe_vlan=vsan_id,
                    policy_owner="local",
                    fc_zone_sharing_mode="coalesce",
                    zoning_state="disabled",
                    id=vsan_id)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'VSAN {} configured'.format(name))
    except Exception, err:
        print(Fore.RED + 'Error: {}, VSAN {}. '.format(err, name))


def configure_vhba_templates(handle, org, description, name, wwpn_pool, vsan_name, fabric = 'A', qos_pol='VI-FC'):
    from ucsmsdk.mometa.vnic.VnicSanConnTempl import VnicSanConnTempl
    from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf

    mo = VnicSanConnTempl(parent_mo_or_dn="org-root/org-{}".format(org),
                          redundancy_pair_type="none",
                          name=name,
                          descr=description,
                          stats_policy_name="default",
                          switch_id=fabric,
                          pin_to_group_name="",
                          policy_owner="local",
                          peer_redundancy_templ_name="",
                          templ_type="updating-template",
                          qos_policy_name=qos_pol,
                          ident_pool_name=wwpn_pool,
                          max_data_field_size="2048")

    mo_1 = VnicFcIf(parent_mo_or_dn=mo,
                    name=vsan_name)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'vHBA Template {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure vHBA Template {}. Does it already exist?'.format(name))


def configure_vnic_templates(handle, org,
                             description='',
                             name='',
                             mac_pool='',
                             mtu='',
                             qos_pol='',
                             network_ctrl_pol='',
                             vlan_name='',
                             switch="A"):
    from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
    from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf

    mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-{}".format(org),
                          redundancy_pair_type="none",
                          name=name,
                          descr=description,
                          stats_policy_name="default",
                          admin_cdn_name="",
                          switch_id=switch,
                          pin_to_group_name="",
                          mtu=mtu, policy_owner="local",
                          peer_redundancy_templ_name="",
                          templ_type="updating-template",
                          qos_policy_name=qos_pol,
                          ident_pool_name=mac_pool,
                          cdn_source="vnic-name",
                          nw_ctrl_policy_name=network_ctrl_pol)

    mo_1 = VnicEtherIf(parent_mo_or_dn=mo,
                       default_net="no",
                       name=vlan_name)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'vNIC Template {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure vNIC Template {}. Does it already exist?'.format(name))


def configure_app_vnic_template(handle, org, desc='',
                                name='',
                                mac_pool='',
                                mtu="9000",
                                qos_pol='',
                                network_pol='',
                                vlan_name='',
                                fabric=''):
    from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
    from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf

    mo = VnicLanConnTempl(parent_mo_or_dn="org-root/org-{}".format(org),
                          redundancy_pair_type="none",
                          name=name,
                          descr=desc,
                          stats_policy_name="default",
                          admin_cdn_name="",
                          switch_id=fabric,
                          pin_to_group_name="",
                          mtu=mtu,
                          policy_owner="local",
                          peer_redundancy_templ_name="",
                          templ_type="updating-template",
                          qos_policy_name=qos_pol,
                          ident_pool_name=mac_pool,
                          cdn_source="vnic-name",
                          nw_ctrl_policy_name=network_pol)
    mo_1 = VnicEtherIf(parent_mo_or_dn=mo,
                       default_net="no",
                       name=vlan_name)

    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'vNIC Template {} configured'.format(name))
    except:
        print(Fore.GREEN + 'vNIC Template already detected {}. Modifying'.format(name))
        handle.add_mo(mo, True)

    handle.commit()

def configure_san_connectivity_policy(handle, organisation = "org-root/org-AKL-VI-APP",
                                      name="UCS_Lan",
                                      vhba_name="vHBA0",
                                      vhba_template_name="AKL-SAN-A",
                                      vsan_name = "AKL-VSAN-A",
                                      description="My Description",
                                      switch_side="A",
                                      vHBA_order="1",
                                      adapter_profile ="VMWare",
                                      wwpn_pool="AKL-WWPN-B",
                                      qos_pol="VI-FC",
                                      wwnn_pool_name="AKL-WWNN-POOL"):
    from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
    from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
    from ucsmsdk.mometa.vnic.VnicFc import VnicFc
    from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf

    mo = VnicSanConnPolicy(parent_mo_or_dn=organisation,
                           policy_owner="local",
                           name=name,
                           descr=description)

    mo_1 = VnicFcNode(parent_mo_or_dn=mo,
                      ident_pool_name=wwnn_pool_name,
                      addr="pool-derived")

    mo_2 = VnicFc(parent_mo_or_dn=mo,
                  cdn_prop_in_sync="yes",
                  addr="derived",
                  admin_host_port="ANY",
                  admin_vcon="any",
                  stats_policy_name="default",
                  admin_cdn_name="",
                  switch_id=switch_side,
                  pin_to_group_name="",
                  pers_bind="disabled",
                  order=vHBA_order,
                  pers_bind_clear="no",
                  qos_policy_name=qos_pol,
                  adaptor_profile_name=adapter_profile,
                  ident_pool_name=wwpn_pool,
                  cdn_source="vnic-name",
                  max_data_field_size="2048",
                  nw_templ_name=vhba_template_name,
                  name=vhba_name)
    mo_2_1 = VnicFcIf(parent_mo_or_dn=mo_2,
                      name=vsan_name)
    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'SAN Connectivity Policy {} configured'.format(name))
    except Exception, err:
        handle.add_mo(mo, True)
        handle.commit()
        print(Fore.RED + 'Error: {}, SAN Connectivity Policy {}. '.format(err, name))

def configure_lan_connectivity_policy(handle, organisation = "org-root/org-AKL-VI-APP",
                                      vnic_template_name="AKL-VI-MGMT-A",
                                      vnic_order="1",
                                      name="UCS_Lan",
                                      vnic_name="vNIC1",
                                      description="My Description",
                                      nw_control_pol="AKL-CDP-EN",
                                      switch_side="A",
                                      adapter_profile ="VMWare",
                                      MTU = "9000",
                                      mac_pool="AKL_VI_App_MAC-B",
                                      qos_pol="org-root/org-AKL-VI-APP/ep-qos-VI-RP"):

    from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy
    from ucsmsdk.mometa.vnic.VnicEther import VnicEther

    mo = VnicLanConnPolicy(parent_mo_or_dn=organisation,
                           policy_owner="local",
                           name=name,
                           descr=description)

    mo_1 = VnicEther(parent_mo_or_dn=mo,
                     cdn_prop_in_sync="yes",
                     nw_ctrl_policy_name=nw_control_pol,
                     admin_host_port="ANY",
                     admin_vcon="any",
                     stats_policy_name="default",
                     admin_cdn_name="",
                     switch_id=switch_side,
                     pin_to_group_name="",
                     name=vnic_name,
                     order=vnic_order,
                     qos_policy_name=qos_pol,
                     adaptor_profile_name=adapter_profile,
                     ident_pool_name=mac_pool,
                     cdn_source="vnic-name",
                     mtu=MTU,
                     nw_templ_name=vnic_template_name,
                     addr="derived")


    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'LAN Connectivity Policy {} configured'.format(name))
    except Exception, err:
        handle.add_mo(mo, True)
        handle.commit()
        print(Fore.RED + 'Error: {}, LAN Connectivity Policy {}. '.format(err, name))

def configure_service_profile_template(handle, name, type, resolve_remote, descr="",
                       usr_lbl="", src_templ_name="", ext_ip_state="none",
                       ext_ip_pool_name="", ident_pool_name="",
                       agent_policy_name="",
                       bios_profile_name="",
                       boot_policy_name="",
                       dynamic_con_policy_name="",
                       host_fw_policy_name="",
                       kvm_mgmt_policy_name="",
                       lan_conn_policy_name="",
                       local_disk_policy_name="",
                       maint_policy_name="",
                       mgmt_access_policy_name="",
                       mgmt_fw_policy_name="",
                       power_policy_name="",
                       san_conn_policy_name="",
                       scrub_policy_name="",
                       sol_policy_name="",
                       stats_policy_name="",
                       vcon_profile_name="",
                       vmedia_policy_name="",
                       server_pool_name="",
                       org="org-root"):

    from ucsmsdk.mometa.ls.LsServer import LsServer
    from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef
    from ucsmsdk.mometa.ls.LsRequirement import LsRequirement

    #obj = handle.query_dn(parent_dn)
    #if not obj:
    #    raise ValueError("org '%s' does not exist." % parent_dn)
    dn = "org-root/org-{}".format(org)
    mo = LsServer(parent_mo_or_dn="org-root/org-{}".format(org),
                  name=name,
                  type=type,
                  resolve_remote=resolve_remote,
                  descr=descr,
                  usr_lbl=usr_lbl,
                  src_templ_name=src_templ_name,
                  ext_ip_state=ext_ip_state,
                  ext_ip_pool_name=ext_ip_pool_name,
                  ident_pool_name=ident_pool_name,
                  vcon_profile_name=vcon_profile_name,
                  agent_policy_name=agent_policy_name,
                  bios_profile_name=bios_profile_name,
                  boot_policy_name=boot_policy_name,
                  dynamic_con_policy_name=dynamic_con_policy_name,
                  host_fw_policy_name=host_fw_policy_name,
                  kvm_mgmt_policy_name=kvm_mgmt_policy_name,
                  local_disk_policy_name=local_disk_policy_name,
                  maint_policy_name=maint_policy_name,
                  mgmt_access_policy_name=mgmt_access_policy_name,
                  mgmt_fw_policy_name=mgmt_fw_policy_name,
                  power_policy_name=power_policy_name,
                  scrub_policy_name=scrub_policy_name,
                  sol_policy_name=sol_policy_name,
                  stats_policy_name=stats_policy_name,
                  vmedia_policy_name=vmedia_policy_name
                  )

    # Add vNIC Connection Policy to template
    VnicConnDef(parent_mo_or_dn=mo,
                lan_conn_policy_name=lan_conn_policy_name,
                san_conn_policy_name=san_conn_policy_name)

    # Add Server Pool to template
    LsRequirement(parent_mo_or_dn=mo, name=server_pool_name)


    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'Service Profile Template {} configured'.format(name))
    except Exception, err:
        handle.add_mo(mo, True)
        handle.commit()
        print(Fore.YELLOW + 'Error: {}, Service Profile Template {}.  Modifying object '.format(err, name))
'''
akl_vlan = ['1030','1031','1032','1033','1034','1035','1036','1037','1038','1039','1040','1041','1042','1043','1044',
            '1045','1046','1047','1048','1049','1050','1051','1052','1053','1054','1055','1056','1057','1058','1059',
            '1061','1065','1070', '1071', '1072','1078','1087','1088','1090','2068','2104','2820','2821','2822',
            '2824','2825','2826','2827','2828','2828','2830','3002','3010','3030','503','505','513','537','544','549',
            '554']

hlz_vlans = ["1031","1032","1033","1034","1035","1036","1037","1038","1039","1040","1041","1042","1043","1044","1045",
             "1046","1047","1048","1049","1050","1051","1052","1053","1054","1059","1061","1065","1070","1071","1078",
             "1087", "1088","1090","2063","2064","2067", "2068","2071","2088","2104","2112","3000","3002",
             "3024", "3025", "3030","3031","503","514","537"]

configure_organisation(name="AKL-VI-APP")

configure_mac_pools("AKL-VI-APP","AKL MAC Pool for Fabric A","AKL_VI_App_MAC-A","00:25:B5:3A:00:00", "00:25:B5:3A:00:FF")
configure_mac_pools("AKL-VI-APP","AKL MAC Pool for Fabric B","AKL_VI_App_MAC-B","00:25:B5:3B:00:00", "00:25:B5:3B:00:FF")

configure_uuid_pool('AKL-VI-APP',"AKL-VI-App-UUID","UUID Pool for Auckland Shared Edge Compute","sequential",
                    "0000-000000000256","0000-000000000001")
configure_maint_policy(org="AKL-VI-APP",name="AKL-USER-ACK",reboot_pol="user-ack", descr="User Ack")
configure_host_fw_policy(org="AKL-VI-APP",name="AKL-FW-3.2.3g",descr="3.2.3g")
configure_boot_policy("AKL-VI-APP","AKL-CDROM","Boot Policy for Auckland Shared Edge Compute")
configure_local_disk_conf_policy("AKL-VI-APP", "AKL-INT-CARD", "Local Disk Policy for Auckland Shared Edge Compute")
configure_bios_policy("AKL-VI-APP", "AKL-NO-QUIET", "Local Disk Policy for Auckland Shared Edge Compute")

configure_scrub_policy("AKL-VI-APP", "AKL-BIOS-Scrub", "Local Disk Policy for Auckland Shared Edge Compute")
configure_ip_pools("AKL-VI-APP","KVM Management IP Pool for Auckland Shared Edge Compute", "AKL-KVM", "10.233.178.16",
                   "10.233.178.47", "10.233.178.1", "sequential")
configure_qos_policy("AKL-VI-APP", "Platinum QoS Policy for Auckland Shared Edge Compute Application vNIC", "VI-APP-NET",
                     "platinum", "10240")
configure_qos_policy("AKL-VI-APP", "Gold QoS Policy for Auckland Shared Edge Compute Recover Point vNIC", "VI-RP",
                     "platinum", "10240")
configure_qos_policy("AKL-VI-APP", "Silver QoS Policy for Auckland Shared Edge Compute Management vNIC", "VI-MGMT",
                     "silver", "10240")
configure_qos_policy("AKL-VI-APP", "Bronze QoS Policy for Auckland Shared Edge Compute vMotion vNIC", "VI-VMOTION",
                     "silver", "10240")
configure_qos_policy("AKL-VI-APP", "FC QoS Policy for Auckland Shared Edge Compute FC vHBAs", "VI-FC",
                     "fc", "10240")
configure_cdp_pol("AKL-VI-APP","Network Control Policy for Auckland Shared Edge Compute vNICs", "AKL-CDP-EN")
configure_vsans(name='AKL-VSAN-A', vsan_id='1280', fabric='A')
configure_vsans(name='AKL-VSAN-B', vsan_id='1281',fabric='B')
configure_wwnn_pools(org="org-root/org-AKL-VI-APP",wwnn_name="AKL-WWNN-POOL",description="Auckland WWNN Pool",
                     assignment_order="sequential",from_wwnn="20:00:20:25:B5:01:00:00",
                     to_wwnn="20:00:20:25:B5:01:00:FF")

configure_wwpn_pools(org="AKL-VI-APP",description="WWPN Pool for Auckland Shared Edge Compute A Side (VSAN 1280)",
                     name="AKL-WWPN-A", wwpn_from="20:00:2A:25:b5:01:0a:00", wwpn_to="20:00:2A:25:B5:01:0A:FF")
configure_wwpn_pools(org="AKL-VI-APP",description="WWPN Pool for Auckland Shared Edge Compute B Side (VSAN 1281)",
                     name="AKL-WWPN-B", wwpn_from="20:00:2B:25:b5:01:0b:00", wwpn_to="20:00:2B:25:B5:01:0b:FF")
configure_vhba_templates(org="AKL-VI-APP", description="vHBA Template for Auckland Shared Edge Compute SAN Fabric A",
                         name="AKL-HBA-A", wwpn_pool="AKL-WWPN-A",vsan_name="AKL-VSAN-A",fabric="A",qos_pol="VI-FC")
configure_vhba_templates(org="AKL-VI-APP",description="vHBA Template for Auckland Shared Edge Compute SAN Fabric B",
                         name="AKL-HBA-B", wwpn_pool="AKL-WWPN-B",vsan_name="AKL-VSAN-B",fabric="B",qos_pol="VI-FC")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute Management vNIC side A",
                         "AKL-VI-MGMT-A","AKL_VI_App_MAC-A","9000","VI-MGMT","AKL-CDP-EN","VI-MGMT_1112","A")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute Management vNIC side B",
                         "AKL-VI-MGMT-B","AKL_VI_App_MAC-B","9000","VI-MGMT","AKL-CDP-EN","VI-MGMT_1112","B")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                         "AKL-VI-VMOTION-A","AKL_VI_App_MAC-A","9000","VI-VMOTION","AKL-CDP-EN","VI-VMOTION_1111","A")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                         "AKL-VI-VMOTION-B","AKL_VI_App_MAC-B","9000","VI-VMOTION","AKL-CDP-EN","VI-VMOTION_1111","B")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                         "AKL-VI-RP-A","AKL_VI_App_MAC-A","9000","VI-RP","AKL-CDP-EN","VI-RP_1114","A")
configure_vnic_templates("AKL-VI-APP","vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                         "AKL-VI-RP-B","AKL_VI_App_MAC-B","9000","VI-RP","AKL-CDP-EN","VI-RP_1114","B")
for vlan_id in akl_vlan:
    if len(vlan_id) == 3:
        vlan_id_cleaned = "0" + vlan_id
    elif len(vlan_id) == 2:
        vlan_id_cleaned = "00" + vlan_id
    else:
        vlan_id_cleaned = vlan_id
    configure_vlans(vlan_id, 'AKL_VI_App_VLAN')
    configure_app_vnic_template(org="AKL-VI-APP",
                                desc="vNIC Template for Auckland Shared Edge Compute vMotion vNIC side A",
                                name="AKL-VI-APP-A",mac_pool="AKL_VI_App_MAC-A",mtu="9000",qos_pol="VI-APP-NET",
                                network_pol="AKL-CDP-EN", vlan_name="AKL_VI_App_VLAN_{}".format(vlan_id_cleaned),
                                fabric="A")
    configure_app_vnic_template(org="AKL-VI-APP",
                                desc="vNIC Template for Auckland Shared Edge Compute vMotion vNIC side B",
                                name="AKL-VI-APP-B", mac_pool="AKL_VI_App_MAC-B", mtu="9000", qos_pol="VI-APP-NET",
                                network_pol="AKL-CDP-EN", vlan_name="AKL_VI_App_VLAN_{}".format(vlan_id_cleaned),
                                fabric="B")

configure_vlans("1112", 'VI-MGMT')
configure_vlans("1111", 'VI-VMOTION')
configure_vlans("1114", 'VI-RP')
configure_san_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
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

configure_san_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
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

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-MGMT-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC1",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="VI-MGMT",
                                  vnic_order="3")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-VMOTION-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC2",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="4")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-APP-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC3",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="AKL-VI-APP",
                                  vnic_order="5")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-RP-A",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC4",
                                  description="AKL VI RP vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="A",
                                  mac_pool="AKL-VI-APP-MAC-A",
                                  qos_pol="AKL-VI-RP",
                                  vnic_order="6")


configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-MGMT-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC5",
                                  description="AKL VI MGMT vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="VI-MGMT",
                                  vnic_order="7")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-VMOTION-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC6",
                                  description="AKL VI vMotion vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="VI-VMOTION",
                                  vnic_order="8")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
                                  vnic_template_name="AKL-VI-APP-B",
                                  name="AKL-VI-APP-CON",
                                  vnic_name="vNIC7",
                                  description="AKL VI App vNIC",
                                  nw_control_pol="AKL-CDP-EN",
                                  switch_side="B",
                                  mac_pool="AKL-VI-APP-MAC-B",
                                  qos_pol="AKL-VI-APP",
                                  vnic_order="9")

configure_lan_connectivity_policy(organisation="org-root/org-AKL-VI-APP",
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


create_sp_from_template(start_sp_value=611, sp_quantity=12,sp_name_prefix="csvipresx",org="AKL-VI-APP",
                        template_name="AKL-VI-APPLICATION_1")
'''