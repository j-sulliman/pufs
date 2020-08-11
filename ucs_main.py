from ucsmsdk.ucshandle import UcsHandle
from colorama import Fore, Back, Style, init
from ucsmsdk.ucsexception import UcsException
import argparse
import sys
init(autoreset=True)

parser = argparse.ArgumentParser(description='Configure UCS from spreadsheet')
parser.add_argument('-a', help='UCSM IP (a)ddress (not URL)',type=str,
                    required=True)
parser.add_argument('-u', help='UCSM (u)ser name',type=str, required=True)
parser.add_argument('-p', help='UCSM (p)assword',type=str, required=True)
parser.add_argument('-f', help='Excel Spreadsheet File Name and Path',type=str,
                    required=False)
args = parser.parse_args()

def ucs_logon(ip_addr=args.a, usr=args.u, pw=args.p):
    handle = UcsHandle(ip_addr, usr, pw, port=443, secure=True)
    handle.get_auth_token()
    handle.login(auto_refresh=True)
    print('Connecting to {}')
    return handle


def configure_organisation(handle, name):
    from ucsmsdk.mometa.org.OrgOrg import OrgOrg
    mo = OrgOrg(parent_mo_or_dn="org-root", name=name)
    handle.add_mo(mo)
    try:
        handle.commit()
        print(Fore.GREEN + 'Organisation {} configured'.format(name))
    except UcsException:
        print(Fore.YELLOW + 'Error: {}  Organisation {}, not configured. '.format(UcsException, name))



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
    except:
        print(Fore.YELLOW + 'Error: UUID {}, {}. '.format(name,
                sys.exc_info()[1]))



def configure_boot_policy(handle, org, name, descr, reboot_on_upd,
        enforce_vnic_name, boot_mode):
    from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
    from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
    from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
    from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
    from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage

    mo = LsbootPolicy(parent_mo_or_dn="org-root/org-{}".format(org), name=name,
                        descr=descr,reboot_on_update=reboot_on_upd,
                        policy_owner="local",
                        enforce_vnic_name=enforce_vnic_name,
                        boot_mode=boot_mode)
    mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote", lun_id="0", mapping_name="", order="1")
    mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="2")
    mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
    mo_2_1_1 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_2_1, order="2")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Boot Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: Boot Policy {}, {}. '.format(name,
                sys.exc_info()[1]))

def configure_local_disk_conf_policy(handle, org, name, descr, mode, flex_flash,
                                    flex_flash_report, flex_flash_remove):
    from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy

    mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn="org-root/org-{}".format(
            org), protect_config="yes", name=name, descr=descr,
            flex_flash_raid_reporting_state=flex_flash_report,
            flex_flash_state=flex_flash, policy_owner="local", mode=mode)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Local Disk Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: Local Disk Policy {}, {}. '.format(name,
                sys.exc_info()[1]))

def configure_bios_policy(handle, org, name, descr, quiet_boot, cdn_ctrl,
                            post_err_pause, reboot_on_upd):
    ##### Start-Of-PythonScript #####

    from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile

    mo = BiosVProfile(parent_mo_or_dn="org-root/org-{}".format(org), descr=descr,
                      name=name, reboot_on_update=reboot_on_upd)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'BIOS Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: BIOS Policy {}, {}. '.format(name,
                sys.exc_info()[1]))


    from ucsmsdk.mometa.bios.BiosTokenSettings import BiosTokenSettings


    from ucsmsdk.mometa.bios.BiosTokenSettings import BiosTokenSettings

    mo = BiosTokenSettings(parent_mo_or_dn="org-root/org-{}/bios-prof-{}/tokn-featr-Quiet Boot/tokn-param-QuietBoot".format(org, name),
        is_assigned="yes", settings_mo_rn=quiet_boot)
    handle.add_mo(mo, True)

    from ucsmsdk.mometa.bios.BiosTokenSettings import BiosTokenSettings

    mo = BiosTokenSettings(parent_mo_or_dn="org-root/org-{}/bios-prof-{}/tokn-featr-POST error pause/tokn-param-POSTErrorPause".format(org, name),
        is_assigned="yes", settings_mo_rn=post_err_pause)
    handle.add_mo(mo, True)


    from ucsmsdk.mometa.bios.BiosTokenSettings import BiosTokenSettings

    mo = BiosTokenSettings(parent_mo_or_dn="org-root/org-{}/bios-prof-{}/tokn-featr-Consistent Device Name Control/tokn-param-cdnEnable".format(org, name),
        is_assigned="yes", settings_mo_rn=cdn_ctrl)
    handle.add_mo(mo, True)


    try:
        handle.commit()
        print(Fore.GREEN + 'BIOS Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: BIOS Policy {}, {}. '.format(name, sys.exc_info()[1]))


def configure_sol_policy(handle, org, name, descr, baud_speed='115200'):
    from ucsmsdk.mometa.sol.SolPolicy import SolPolicy

    mo = SolPolicy(admin_state='enable',
                   descr=descr,
                   parent_mo_or_dn="org-root/org-{}".format(org),
                   name=name,
                   speed=str(baud_speed))
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'SoL Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: SoL Policy {}, {}. '.format(name, sys.exc_info()[1]))


def configure_scrub_policy(handle, org, name, descr, bios_scrub,
                            flex_flash_scrub, disk_scrub):
    from ucsmsdk.mometa.compute.ComputeScrubPolicy import ComputeScrubPolicy

    mo = ComputeScrubPolicy(parent_mo_or_dn="org-root/org-{}".format(org),
                            flex_flash_scrub=flex_flash_scrub, name=name,
                            descr=descr, policy_owner="local",
                            bios_settings_scrub=bios_scrub,
                            disk_scrub=disk_scrub)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Scrub Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: Scrub Policy {}, {}. '.format(name,
                sys.exc_info()[1]))


def configure_maint_policy(handle, org, ss_timer, name='', reboot_pol="user-ack",
        descr=''):
    from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy

    mo = LsmaintMaintPolicy(parent_mo_or_dn="org-root/org-{}".format(org), uptime_disr=reboot_pol, name=name,
                            descr=descr, trigger_config="", soft_shutdown_timer=ss_timer, sched_name="",
                            policy_owner="local")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Maintenance Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: Maintenance Policy {}, {}. '.format(name,
                sys.exc_info()[1]))

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


def configure_host_fw_policy(handle, org, name, descr, ignore_comp_check,
                        stage_size, upd_trig, mode,
                        override_def_exc, rack_bun_ver='', blade_bun_ver=''):
    from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import FirmwareComputeHostPack
    from ucsmsdk.mometa.firmware.FirmwareExcludeServerComponent import FirmwareExcludeServerComponent

    mo = FirmwareComputeHostPack(parent_mo_or_dn="org-root/org-{}".format(org),
                                 ignore_comp_check=ignore_comp_check, name=name,
                                 descr=descr, stage_size=stage_size,
                                 rack_bundle_version=rack_bun_ver,
                                 update_trigger=upd_trig,
                                 policy_owner="local", mode=mode,
                                 blade_bundle_version=blade_bun_ver,
                                 override_default_exclusion=override_def_exc)
    mo_1 = FirmwareExcludeServerComponent(parent_mo_or_dn=mo,
                                        server_component="local-disk")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Host Firmware Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: Host Firmware Policy {}, {}. '.format(name,
                sys.exc_info()[1]))


def configure_vlans(handle, vlan_id, vlan_name):
    from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
    mo = FabricVlan(parent_mo_or_dn="fabric/lan", sharing="none",
                    name=vlan_name,
                    id=vlan_id,
                    mcast_policy_name="", policy_owner="local",
                    default_net="no", pub_nw_name="",
                    compression_type="included")
    handle.add_mo(mo)
    #handle.commit()
    #print(Fore.GREEN + 'VLAN {} configured'.format(vlan_id_cleaned))

    try:
        handle.commit()
        print(Fore.GREEN + 'VLAN {} configured'.format(vlan_id))
    except:
        print(Fore.YELLOW + 'Error: VLAN {}, {}. '.format(vlan_id,
            sys.exc_info()[1]))



def configure_mac_pools(handle, org, description, name, mac_from, mac_to):
    from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
    from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock

    mo = MacpoolPool(parent_mo_or_dn="org-root/org-{}".format(org),
                        policy_owner="local", descr=description,
                        assignment_order="sequential", name=name)
    mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to=mac_to, r_from=mac_from)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'MAC Pool {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: MAC Pool {}, {}. '.format(name,
                sys.exc_info()[1]))


def configure_ip_pools(handle, org, description, name, ip_from, ip_to, ip_gw = "10.233.178.1",
                       assignment_ordr = "sequential", ip_subnet="255.255.255.0", dns_prim='10.46.116.13',
                       dns_sec="10.50.116.14"):
    from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
    from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock

    mo = IppoolPool(parent_mo_or_dn="org-root/org-{}".format(org), is_net_bios_enabled="disabled", name=name,
                    descr=description, policy_owner="local", ext_managed="internal", supports_dhcp="disabled",
                    assignment_order=assignment_ordr)
    mo_1 = IppoolBlock(parent_mo_or_dn=mo, to=ip_to, r_from=ip_from, def_gw=ip_gw, subnet=ip_subnet, prim_dns=dns_prim,
                       sec_dns=dns_sec)
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

    mo = EpqosDefinition(parent_mo_or_dn="org-root/org-{}".format(org),
                        policy_owner="local", name=name, descr=description)
    mo_1 = EpqosEgress(parent_mo_or_dn=mo, rate="line-rate",
                        host_control="none", name="", prio=priority,
                       burst=str(burst))
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'QoS Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: QoS Policy {}, {}. '.format(name,
                sys.exc_info()[1]))
        #data = handle.set_dump_xml()
        #print(data)


def configure_cdp_pol(handle, org, description, name, cdp, macreg, actionon,
                        macsec, lldprx, lldptx):
    from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
    from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac

    mo = NwctrlDefinition(parent_mo_or_dn="org-root/org-{}".format(org),
                          lldp_transmit=lldptx, name=name,
                          lldp_receive=lldprx,
                          mac_register_mode=macreg,
                          policy_owner="local",
                          cdp=cdp, uplink_fail_action=actionon, descr=description)
    mo_1 = DpsecMac(parent_mo_or_dn=mo, forge=macsec, policy_owner="local", name="", descr="")
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'Network Control Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Unable to configure CDP Policy {}. Does it already exist?'.format(name))
        #data = handle.set_dump_xml()
        #print(data)



def configure_wwnn_pools(handle, org,
                         wwnn_name="AKL-WWNN-Pool",
                         description="Auckland WWNN pool",
                         assignment_order="sequential",
                         from_wwnn="20:00:00:25:B5:00:00:00",
                         to_wwnn="20:00:00:25:B5:00:00:7F"):
    from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
    from ucsmsdk.mometa.fcpool.FcpoolBlock import FcpoolBlock
    mo = FcpoolInitiators(parent_mo_or_dn='org-root/org-{}'.format(org),
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
        print(Fore.YELLOW + 'Error: WWNN Pool {}, {}. '.format(wwnn_name,
                sys.exc_info()[1]))

def configure_kvm_policy(handle, org, description, name, vmedia_encrypt,
                        kvm_port):
    from ucsmsdk.mometa.compute.ComputeKvmMgmtPolicy import ComputeKvmMgmtPolicy

    mo = ComputeKvmMgmtPolicy(parent_mo_or_dn="org-root/org-{}".format(org),
                            descr=description, name=name,
                            vmedia_encryption=vmedia_encrypt)
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'KVM Policy {} configured'.format(name))
    except:
        print(Fore.YELLOW + 'Error: KVM Policy {}, {}. '.format(name,
                sys.exc_info()[1]))



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
                    name=str(name),
                    fcoe_vlan=str(vsan_id),
                    policy_owner="local",
                    fc_zone_sharing_mode="coalesce",
                    zoning_state="disabled",
                    id=str(vsan_id))
    handle.add_mo(mo)

    try:
        handle.commit()
        print(Fore.GREEN + 'VSAN {} configured'.format(vsan_id))
    except:
        print(Fore.YELLOW + 'Error: VSAN {}, {}. '.format(vsan_id, sys.exc_info()[1]))


def configure_vhba_templates(handle, org, description, name, wwpn_pool,
    vsan_name, fabric = 'A', qos_pol='VI-FC'):
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
        print(Fore.YELLOW + 'Error: vHBA Template {}, {}. '.format(name,
                sys.exc_info()[1]))


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


    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'vNIC Template {} configured'.format(name))
    except:
        handle.add_mo(mo, modify_present=True)
        handle.commit()
        print(Fore.YELLOW + 'Error: vNIC Template {}, {}. '.format(name,
                sys.exc_info()[1]))


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

def configure_san_connectivity_policy(handle, org, name, wwnn_pool_name,
                    adaptor_prof_name, vhba_name, vhba_tmpl_name ):
    from ucsmsdk.mometa.vnic.VnicSanConnPolicy import VnicSanConnPolicy
    from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
    from ucsmsdk.mometa.vnic.VnicFc import VnicFc
    from ucsmsdk.mometa.vnic.VnicFcIf import VnicFcIf

    mo = VnicSanConnPolicy(parent_mo_or_dn="org-root/org-{}".format(org), name=name)
    mo_1 = VnicFcNode(parent_mo_or_dn=mo, addr="pool-derived",
                        ident_pool_name=wwnn_pool_name)
    mo_2 = VnicFc(parent_mo_or_dn=mo, adaptor_profile_name=adaptor_prof_name,
                name=vhba_name, nw_templ_name=vhba_tmpl_name, order="1")
    mo_2_1 = VnicFcIf(parent_mo_or_dn=mo_2, name="default")

    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'SAN Connectivity Policy {} configured'.format(
            name))
    except:
        handle.add_mo(mo, modify_present=True)
        handle.commit()
        print(Fore.YELLOW + 'Error: SAN Connectivity Policy {}, {}. '.format(
                name, sys.exc_info()[1]))

def configure_lan_connectivity_policy(handle, organisation = "org-root/org-AKL-VI-APP",
                                      vnic_template_name="AKL-VI-MGMT-A",
                                      vnic_order="1",
                                      name="UCS_Lan",
                                      vnic_name="vNIC1",
                                      switch_id="A",
                                      adapter_profile ="VMWare"
                                     ):

    from ucsmsdk.mometa.vnic.VnicLanConnPolicy import VnicLanConnPolicy
    from ucsmsdk.mometa.vnic.VnicEther import VnicEther

    mo = VnicLanConnPolicy(parent_mo_or_dn=organisation,
                           name=name)

    if switch_id == 'A':
        mo_1 = VnicEther(parent_mo_or_dn=mo,
                        adaptor_profile_name=adapter_profile,
                        name=vnic_name, nw_templ_name=vnic_template_name,
                        order=vnic_order)
    elif switch_id == 'B':
        mo_1 = VnicEther(parent_mo_or_dn=mo,
                        adaptor_profile_name=adapter_profile,
                        name=vnic_name, nw_templ_name=vnic_template_name,
                        order=vnic_order, switch_id=switch_id)


    try:
        handle.add_mo(mo)
        handle.commit()
        print(Fore.GREEN + 'LAN Connectivity Policy {} configured'.format(
            name))
    except:
        handle.add_mo(mo, modify_present=True)
        handle.commit()
        print(Fore.YELLOW + 'Error: LAN Connectivity Policy {}, {}. '.format(
                name, sys.exc_info()[1]))
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
        print(Fore.GREEN + 'Service Profile Template {} configured'.format(
            name))
    except:
        handle.add_mo(mo, modify_present=True)
        handle.commit()
        print(Fore.YELLOW + 'Error: Service Profile Template {}, {}. '.format(
                name, sys.exc_info()[1]))


def query_ucs_class(handle, ucs_class='computeRackUnit', children='False'):
    if children == 'True':
        object_array = handle.query_classid(ucs_class, hierarchy=True)
    elif children == 'False':
        object_array = handle.query_classid(ucs_class, hierarchy=False)
    return object_array
