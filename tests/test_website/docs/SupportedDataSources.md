---
title: "Supported Data Sources"
sidebar_position: 686
---

[Skip To Main Content](#)

Account

Settings

---

Logout

* placeholder

Account

Settings

---

Logout

Filter: 

* All Files

Submit Search

Filter: 

* All Files

Submit Search

You are here:

# Supported Data Sources

This section lists platforms and systems that can be monitored with Netwrix Auditor.

## Active Directory

Auditor supports monitoring the following domain controller operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

See the [Active Directory](../Configuration/ActiveDirectory/Overview.htm "Active Directory") topic for additional information.

## Active Directory Federation Services (AD FS)

Auditor supports monitoring the following AD FS operating system versions:

* AD FS 5.0 – Windows Server 2019
* AD FS 4.0 – Windows Server 2016
* AD FS 3.0 – Windows Server 2012 R2

See the [AD FS](../Configuration/ActiveDirectoryFederatedServices/Overview.htm "AD FS Servers") topic for additional information.

## Exchange

Auditor supports monitoring the following Exchange Server versions:

* Microsoft Exchange Server 2019
* Microsoft Exchange Server 2016
* Microsoft Exchange Server 2013

See the [Exchange](../Configuration/Exchange/Overview.htm "Exchange") topic for additional information.

## File Servers

Dell Data Storage

Auditor supports monitoring the following device versions:

* Dell Data Storage (Unity XT, UnityVSA) running any of the following operating environment versions:

  + 5.4.x
  + 5.2.x
  + 5.0.x
  + 4.5.x
  + 4.4.x
* Dell VNX/VNXe/Celerra families
* Dell PowerStore family

**NOTE:** Only CIFS configuration is supported.

See the [Dell Data Storage](../Configuration/FileServers/DellDataStorage/Overview.htm "Dell Data Storage") topic for additional information.

Dell Isilon/PowerScale

Auditor supports monitoring the following device versions:

* Dell Isilon/PowerScale versions 7.2 – 9.10

**NOTE:** Only CIFS configuration is supported.

Auditing of *System* zone is not supported. As stated by Dell, this zone should be reserved for configuration access only. Current data should be stored in other access zones. See the [Isilon OneFS 8.2.1 CLI Administration Guide](`https://www.dellemc.com/en-us/collaterals/unauth/technical-guides-support-information/2019/09/docu95372.pdf` "Isilon OneFS 8.2.1 CLI Administration Guide") for additional information.

See the [Dell Isilon/PowerScale](../Configuration/FileServers/DellIsilon/Overview.htm "Dell Isilon/PowerScale") topic for additional information.

NetApp Data ONTAP

Auditor supports monitoring the following device versions:

* Clustered-Mode

  + 9.0 – 9.16
  + 8.3

**NOTE:** Only CIFS configuration is supported.

See the [NetApp Data ONTAP](../Configuration/FileServers/NetAppCMode/Overview.htm "NetApp Data ONTAP") topic for additional information.

Nutanix

Auditor supports monitoring the following device versions:

* Files 3.6 - 4.3.0

See the [Nutanix](../Configuration/FileServers/Nutanix/Overview.htm "Nutanix") topic for additional information.

Qumulo

Auditor supports monitoring the following device versions:

* Core 3.3.5 - 6.x.x

See the [Qumulo](../Configuration/FileServers/Qumulo/Overview.htm "Qumulo") topic for additional information.

Synology

Auditor supports monitoring the following device versions:

* DSM 7.2
* DSM 7.1
* DSM 7.0
* DSM 6.2.3

See the [Synology](../Configuration/FileServers/Synology/Overview.htm "Synology") topic for additional information.

Windows File Servers

Auditor supports monitoring the following operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

* Windows 11
* Windows 10 (32 and 64-bit)
* Windows 8.1 (32 and 64-bit)
* Windows 7 (32 and 64-bit)

See the [Windows File Servers](../Configuration/FileServers/Windows/Overview.htm "Windows File Servers") topic for additional information.

## Group Policy

Auditor supports monitoring the following domain controller operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

See the [Group Policy](../Configuration/GroupPolicy/Overview.htm "Group Policy") topic for additional information.

## Logon Activity

Auditor supports monitoring the following domain controller operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

See the [Logon Activity](../Configuration/LogonActivity/Overview.htm "Logon Activity") topic for additional information.

## Microsoft 365

Exchange Online

Auditor supports monitoring the following versions:

* Exchange Online version provided within Microsoft Office 365
* Microsoft GCC (government community cloud) and GCC High

  **NOTE:** DoD tenant types are not supported.

See the [Exchange Online](../Configuration/Microsoft365/ExchangeOnline/Overview.htm "Exchange Online") topic for additional information.

Microsoft Entra ID (formerly Azure AD)

Auditor supports monitoring the following versions:

* Microsoft Entra ID version provided within Microsoft Office 365
* Microsoft GCC (government community cloud) and GCC High

  **NOTE:** DoD tenant types are not supported.

See the [Microsoft Entra ID (formerly Azure AD)](Microsoft365/AzureActiveDirectory/Overview.htm "Microsoft Entra ID (formerly Azure AD)") topic for additional information.

Microsoft Teams (MS Teams)

Auditor supports monitoring the following versions:

* Microsoft Entra ID version provided within Microsoft Office 365
* Microsoft GCC (government community cloud) and GCC High

  **NOTE:** DoD tenant types are not supported.

See the [MS Teams](../Configuration/Microsoft365/Teams/Overview.htm "MS Teams") topic for additional information.

SharePoint Online

Auditor supports monitoring the following versions:

* SharePoint Online version provided within Microsoft Office 365
* Microsoft GCC (government community cloud) and GCC High

  **NOTE:** DoD tenant types are not supported.

See the [SharePoint Online](../Configuration/Microsoft365/SharePointOnline/Overview.htm "SharePoint Online") topic for additional information.

## Network Devices

Cisco ASA Devices

Auditor supports monitoring the following device versions:

* ASA (Adaptive Security Appliance) 8 and above

See the [Configure Cisco ASA Devices](../Configuration/NetworkDevices/CiscoASA.htm "Configure Cisco ASA Devices") topic for additional information.

Cisco IOS Devices

Auditor supports monitoring the following device versions:

* IOS (Internetwork Operating System) 12, 15, 16, and 17

See the [Configure Cisco IOS Devices](../Configuration/NetworkDevices/CiscoIOS.htm "Configure Cisco IOS Devices") topic for additional information.

Cisco Meraki Dashboard

Auditor supports monitoring the following device versions:

* Netwrix recommends the latest version of the Meraki Dashboard

See the [Cisco Meraki Dashboard](../Configuration/NetworkDevices/CiscoMerakiDashboard.htm "Cisco Meraki Dashboard")  topic for additional information.

Cisco FTD

Auditor supports monitoring the following device versions:

* FTD (Firepower Threat Defense) 6.5

Fortinet FortiGate Devices

Auditor supports monitoring the following device versions:

* FortiOS 5.6 and above

See the [Configure Fortinet FortiGate Devices](../Configuration/NetworkDevices/FortinetFortiGate.htm "Configure Fortinet FortiGate Devices") topic for additional information.

HPE Aruba Devices

Auditor supports monitoring the following device versions:

* Aruba OS 6.46.4.x – 8.6.0.x (Mobility Master, Mobility Controller)

See the [Configure Pulse Secure Devices](../Configuration/NetworkDevices/PulseSecure.htm "Configure Pulse Secure Devices") topic for additional information.

Juniper Devices

Auditor supports monitoring the following device versions:

* vSRX with Junos OS 12.1, Junos OS 18.1, Junos OS 20.4R2
* vMX with Junos OS 17.1

See the [Configure Juniper Devices](../Configuration/NetworkDevices/Juniper.htm "Configure Juniper Devices") topic for additional information.

PaloAlto Devices

Auditor supports monitoring the following device versions:

* PAN-OS 7.0, 8.0, 9.0, 10.0

See the [Configure PaloAlto Devices](../Configuration/NetworkDevices/PaloAlto.htm "Configure PaloAlto Devices") topic for additional information.

Pulse Secure Devices

Auditor supports monitoring the following device versions:

* 9.1R3 and above

See the [Configure Pulse Secure Devices](../Configuration/NetworkDevices/PulseSecure.htm "Configure Pulse Secure Devices") topic for additional information.

SonicWall Devices

Auditor supports monitoring the following device versions:

* WAF 2.0.0.x / SMA v9.x & v10.x
* NS 6.5.х.х with SonicOS 6.5.х and 7.0.x
* SMA 12.2

See the [Configure SonicWall Devices](../Configuration/NetworkDevices/SonicWall.htm "Configure SonicWall Devices") topic for additional information.

## Oracle

Auditor supports monitoring the following versions:

* Database 23c On-Premise
* Database 21c On-Premise
* Database 19c On-Premise
* Database 18c On-Premise
* Database 12c On-Premise (12.1, 12.2)
* Database 11g, limited support

  **NOTE:**  See the [Considerations for Oracle Database 11g](../Configuration/Oracle/Overview.htm#Consider "Considerations for Oracle Database 11g") topic for additional information.
* Oracle Database Cloud Service (Enterprise Edition)

See the [Oracle Database](../Configuration/Oracle/Overview.htm "Oracle Database") topic for additional information.

## SharePoint

Auditor supports monitoring the following versions:

* Microsoft SharePoint Server Subscription Edition
* Microsoft SharePoint Server 2019
* Microsoft SharePoint Server 2016
* Microsoft SharePoint Foundation 2013 and SharePoint Server 2013
* Microsoft SharePoint Foundation 2010 and SharePoint Server 2010

See the [SharePoint](../Configuration/SharePoint/Overview.htm "SharePoint") topic for additional information.

## SQL Server

Auditor supports monitoring the following versions:

* Microsoft SQL Server 2022
* Microsoft SQL Server 2019
* Microsoft SQL Server 2017
* Microsoft SQL Server 2016
* Microsoft SQL Server 2014
* Microsoft SQL Server 2012

**NOTE:** Linux-based versions are not supported.

See the [SQL Server](../Configuration/SQLServer/Overview.htm "SQL Server") topic for additional information.

## User Activity

Auditor supports monitoring the following versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

* Windows 11
* Windows 10 (32 and 64-bit)
* Windows 8.1 (32 and 64-bit)
* Windows 7 (32 and 64-bit)

User Activity data source can support around 300 targets with one user session per target without scalability issues:

* Depending on how dense is the actual user activity, the number can be more for servers but less for workstations.
* 50-100 concurrent sessions per terminal server.

Netwrix recommends using the User Activity auditing only for those infrastructure areas that require more attention due to their sensitivity or criticality. Applicable usage scenarios include, for example:

* Terminal servers where users can log in from external locations
* Areas accessible by contractor personnel
* Servers with sensitive information
* Sessions with elevated privileges

See the [User Activity](../Configuration/UserActivity/Overview.htm "User Activity") topic for additional information.

## VMware Servers

Auditor supports monitoring the following versions:

* VMware ESX/ESXi: 6.0 – 6.7, 7.0, 8.0
* VMware vCenter Server: 6.0 – 6.7, 7.0, 8.0

See the [VMware](../Configuration/VMware/Overview.htm "VMware Servers") topic for additional information.

## Windows Servers

Windows Servers & Desktops

Auditor supports monitoring the following operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

* Windows 11
* Windows 10 (32 and 64-bit)
* Windows 8.1 (32 and 64-bit)
* Windows 7 (32 and 64-bit)

DNS & DHCP

Auditor supports monitoring the following operating system versions:

* Windows Server 2025
* Windows Server 2022
* Windows Server 2019
* Windows Server 2016
* Windows Server 2012 R2
* Windows Server 2012

**NOTE:** DNS support is limited on Windows Server 2008 to Windows Server 2008 SP2 (32 and 64-bit). DHCP is not supported on Windows Server 2008.

Internet Information Services (IIS)

Auditor supports monitoring the following operating system versions:

* IIS 7.0 and above.

See the [Windows Server](../Configuration/WindowsServer/Overview.htm "Windows Server") topic for additional information.

## Netwrix Integration API

In addition to data sources monitored within the product, Auditor supports technology integrations leveraging its API. Download free add-ons from [Netwrix Auditor Add-on Store](`https://www.netwrix.com/netwrix_addons.html` "Netwrix Auditor Add-on Store") to enrich your audit trails with activity from the following systems and applications.

Also, there are even add-ons that can export data collected by Auditor to other systems (e.g., ArcSight and ServiceNow).

See the [Integration API](../API/Overview.htm "Integration API") topic for additional information.