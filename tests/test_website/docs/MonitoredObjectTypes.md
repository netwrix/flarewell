---
title: "Monitored Object Types, Actions, and Attributes"
sidebar_position: 685
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

# Monitored Object Types, Actions, and Attributes

Netwrix Auditor monitored object types, actions, attributes and components for each data source are located in the following topics:

* [Active Directory](../Configuration/ActiveDirectory/Overview)
* [AD FS](../Configuration/ActiveDirectoryFederatedServices/Overview)
* [Exchange](../Configuration/Exchange/Overview)
* [File Servers](../Configuration/FileServers/Overview)

  + [Dell Data Storage](../Configuration/FileServers/DellDataStorage/Overview)
  + [Dell Isilon/PowerScale](../Configuration/FileServers/DellIsilon/Overview)
  + [NetApp Data ONTAP](../Configuration/FileServers/NetAppCMode/Overview)
  + [Nutanix](../Configuration/FileServers/Nutanix/Overview)
  + [Qumulo](../Configuration/FileServers/Qumulo/Overview)
  + [Synology](../Configuration/FileServers/Synology/Overview)
  + [Windows File Servers](../Configuration/FileServers/Windows/Overview)
* [Group Policy](../Configuration/GroupPolicy/Overview)
* [Logon Activity](../Configuration/LogonActivity/Overview)
* [Microsoft 365](../Configuration/Microsoft365/Overview)

  + [Exchange Online](../Configuration/Microsoft365/ExchangeOnline/Overview)
  + [Microsoft Entra ID](../Configuration/Microsoft365/MicrosoftEntraID/Overview)
  + [SharePoint Online](../Configuration/Microsoft365/SharePointOnline/Overview)
  + [MS Teams](../Configuration/Microsoft365/Teams/Overview)
* [Network Devices](../Configuration/NetworkDevices/Overview)
* [Oracle Database](../Configuration/Oracle/Overview)
* [SharePoint](../Configuration/SharePoint/Overview)
* [SQL Server](../Configuration/SQLServer/Overview)
* [User Activity](../Configuration/UserActivity/Overview)
* [VMware](../Configuration/VMware/Overview)
* [Windows Server](../Configuration/WindowsServer/Overview)

Review the list of actions audited and reported by Netwrix Auditor. Actions vary depending on the data source and the object type.

| Action | Active Directory | Active Directory Federation Services | Exchange  Exchange Online | File Servers | Group Policy | Logon Activity | Microsoft Entra ID (formerly Azure AD) | Oracle database | SharePoint  SharePoint Online | SQL Server | User Activity | VMware Servers | Windows Server |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Added | + | - | +\* | + | + | – | + | + | + | + | – | + | + |
| Removed | + | - | +\* | + | + | – | + | + | + | + | – | + | + |
| Modified | + | – | +\* | + | + | – | + | + | + | + | – | + | + |
| Add (failed attempt) | – | – | – | + | – | – | – | + | – | – | – | – | – |
| Remove (failed attempt) | – | – | – | + | – | – | – | + | – | – | – | – | – |
| Modify (failed attempt) | – | – | – | + | – | – | – | + | – | – | – | – | + |
| Read | – | – | +\* | + | – | – | – | + | + | – | – | – | – |
| Read (failed attempt) | – | – | – | + | – | – | – | + | – | – | – | – | – |
| Renamed | – | – | – | + | – | – | – | + | +\*\* | – | – | – | – |
| Moved | – | – | +\* | + | – | – | – | – | + | – | – | – | – |
| Rename (failed attempt) | – | – | – | + | – | – | – | + | – | – | – | – | – |
| Move (failed attempt) | – | – | – | + | – | – | – | – | – | – | – | – | – |
| Checked in | – | – | – | – | – | – | – | – | + | – | – | – | – |
| Checked out | – | – | – | – | – | – | – | – | + | – | – | – | – |
| Discard check out | – | – | – | – | – | – | – | – | + | – | – | – | – |
| Successful logon | – | + | – | – | – | + | + | + | – | + | – | + | – |
| Failed logon | – | + | – | – | – | + | + | + | – | + | – | +\*\*\* | – |
| Logoff | – | – | – | – | – | – | – | + | – | – | – | – | – |
| Copied | – | – | +\* | + | – | – | – | – | +\*\* | – | – | – | – |
| Sent | – | – | +\* | – | – | – | – | – | – | – | – | – | – |
| Activated | – | – | – | – | – | – | – | – | – | – | + | – | – |
| Support for state-in-time data collection | + | – | + | + | + | - | + | - | + | - | - | + | + |

\* —these actions are reported when auditing non-owner mailbox access for Exchange or Exchange Online.

\*\* — these actions are reported for SharePoint Online only.

\*\*\* — Auditor will not collect data on *Failed Logon* event for VMware in case of incorrect logon attempt through VMware vCenter Single Sign-On; also, it will not collect logons using SSH.