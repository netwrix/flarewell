---
title: "Manage Data Sources"
sidebar_position: 877
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

# Manage Data Sources

You can fine-tune data collection for each data source. Settings that you configure for the data source will be applied to all items belonging to that data source. Using data source settings, you can, for example:

* Enable state-in-time data collection (currently supported for several data sources)
* Depending on the data source, customize the monitoring scope (e.g., enable read access auditing, monitoring of failed attempts)

To add, modify and remove data sources, enable or disable monitoring, you must be assigned the Global administrator role in the product or the Configurator role on the plan. See the [Role-Based Access and Delegation](Delegation.htm "Role-based access and delegation") topic for additional information.

## Modify Data Source Settings

Follow the steps to modify data source settings.

**Step 1 –** Select the monitoring plan you need and click **Edit**.

**Step 2 –** Within the monitoring plan window, highlight the data source (the first one is the row right under the blue table header) and click Edit data source on the right:

[![Data source settings](../static/img/Auditor/Images/Auditor/MonitoringPlans/MP_edit_data_source_thumb_0_0.png "Data source settings")](../../../Resources/Images/Auditor/MonitoringPlans/MP_edit_data_source.png)

**Step 3 –** Modify data source settings as you need.

**Step 4 –** When finished, click **Save**.

Review the following for additional information:

* [Active Directory](ActiveDirectory/Overview.htm "Active Directory")
* [Active Directory Federation Services](ADFS.htm "Active Directory Federation Services")
* [Microsoft Entra ID](MicrosoftEntraID/Overview.htm "Microsoft Entra ID")
* [Exchange](Exchange/Overview.htm "Exchange")
* [Exchange Online](ExchangeOnline/Overview.htm "Exchange Online")
* [File Servers](FileServers/Overview.htm "File Servers")
* [Group Policy](GroupPolicy/Overview.htm "Group Policy")
* [Logon Activity](LogonActivity/Overview.htm "Logon Activity")
* [MS Teams](MSTeams.htm "MS Teams")
* [Network Devices](NetworkDevices.htm "Network Devices")
* [Oracle Database](Oracle/Overview.htm "Oracle Database")
* [SharePoint](SharePoint/Overview.htm "SharePoint")
* [SharePoint Online](SharePointOnline/Overview.htm "SharePoint Online")
* [SQL Server](SQLServer/Overview.htm "SQL Server")
* [User Activity](UserActivity/Overview.htm "User Activity")
* [VMware](VMware/Overview.htm "VMware")
* [Windows File Share](FileServers/Scope.htm#Windows "Windows File Share")

Also, you can add a data source to the monitoring plan, or remove a data source that is no longer needed.

## Add a Data Source to an Existing Plan

Follow the steps to add a data source to existing plan.

**Step 1 –** Select the monitoring plan you need and click Edit.

**Step 2 –** In the right pane, select Add data source.

**Step 3 –** Specify a data source.

**Step 4 –** Configure settings specific to your data source.

**Step 5 –** When finished, click the **Add** button to save the settings.

## Add Items for Monitoring

Once you completed monitoring plan wizard and specified data sources, add items for monitoring. You can add as many items for a data source as you want. In this case, all items will share settings you specified for this data source.

Each data source has a dedicated item type. Netwrix Auditor automatically suggests item types associated with your data source.

| Data Source | Item |
| --- | --- |
| Active Directory  Group Policy  Exchange  Logon Activity | [Domain](ActiveDirectory/Overview.htm#Domain "Domain") |
| Active Directory Federation Services | [Federation Server](ADFS.htm#Federati "Federation Server") |
| Microsoft Entra ID  Exchange Online  SharePoint Online  Microsoft Teams | [Microsoft Entra ID](MicrosoftEntraID/Overview.htm#Office "Office 365 Tenant") |
| File Servers  (including Windows file server, Dell, NetApp, Nutanix File server, Synology, and Qumulo) | [AD Container](ActiveDirectory/Overview.htm#AD "AD Container")  [File Servers](FileServers/Overview.htm#Computer "Computer")  [Dell Isilon](FileServers/Overview.htm#Dell "Dell Isilon")  [Dell VNX VNXe](FileServers/Overview.htm#Dell2 "Dell VNX VNXe")  [File Servers](FileServers/Overview.htm#IP "IP Range")  [NetApp](FileServers/Overview.htm#NetApp "NetApp")  [Windows File Share](FileServers/Scope.htm#Windows "Windows File Share")  [Nutanix SMB Shares](FileServers/Overview.htm#Nutanix "Nutanix SMB Shares")  [Qumulo](FileServers/Overview.htm#Qumulo "Qumulo")  [Synology](FileServers/Overview.htm#Synology "Synology")  By default, Auditor will monitor all shares stored in the specified location, except for hidden shares (both default and user-defined). If you want to monitor user-defined hidden shares, select the related option in the monitored item settings.  Remember that administrative hidden shares like default system root or Windows directory (ADMIN$), default drive shares (D$, E$), etc. will not be monitored. See the topics on the monitored items for details. |
| Network Devices | [Syslog Device](NetworkDevices.htm#Syslog "Syslog Device")  [Cisco Meraki Dashboard](NetworkDevices.htm#top "Cisco Meraki Dashboard") |
| Oracle Database | [Oracle Database Instance](Oracle/Overview.htm#Oracle "Oracle Database Instance") |
| SharePoint | [SharePoint Farm](SharePoint/Overview.htm#SharePoi "SharePoint Farm") |
| SQL Server | [SQL Server Instance](SQLServer/Items.htm#SQL "SQL Server Instance")  [SQL Server Availability Group](SQLServer/Items.htm#SQL2 "SQL Server Availability Group") |
| VMware | [VMware ESX/ESXi/vCenter](VMware/Overview.htm#VMware "VMware ESX/ESXi/vCenter") |
| Windows Server  User Activity | [File Servers](FileServers/Overview.htm#Computer "Computer")  [AD Container](ActiveDirectory/Overview.htm#AD "Container")  [File Servers](FileServers/Overview.htm#IP "IP Range") |
| Netwrix API | [Integration API](../../API/Overview.htm "Integration API") |

To add, modify and remove items, you must be assigned the Global administrator role in the product or the **Configurator** role on the plan. See the [Role-Based Access and Delegation](Delegation.htm "Role-based access and delegation")topic for additional information.

Follow the steps to add a new item to a data source:

**Step 6 –** Navigate to your plan settings.

**Step 7 –** Click Add item under the data source.

**Step 8 –** Provide the object name and configure item settings.

You can fine-tune data collection for each item individually. To do it, select an item within your monitoring plan and click Edit item. For each item, you can:

* Specify a custom account for data collection
* Customize settings specific your item (e.g., specify SharePoint site collections)

## Configure Monitoring Scope

In some environments, it may not be necessary to monitor the entire IT infrastructure. Netwrix monitoring scope can be configured on the Data Source and/or Item levels. the section below contains examples on how to use omit functionality in Auditor.

In addition to the restrictions for a monitoring plan, you can use the \*.txt files to collect more granular audit data. Note that the new monitoring scope restrictions apply together with previous exclusion settings configured in the \*.txt files. See the [Monitoring Plans](Overview.htm "Monitoring Plans")topic for additional information.

| Use case | Related documentation |
| --- | --- |
| **Active Directory** | |
| I want to omit all activity by a specific service account or service accounts with specific naming pattern. | [Active Directory](ActiveDirectory/Overview.htm "Active Directory") |
| If Netwrix user is responsible just for a limited scope within corporate AD, s/he needs to omit everything else. | [Active Directory](ActiveDirectory/Overview.htm "Active Directory")   * Always both activity and state in time data are omitted. * In group/Not in group filters don’t not process groups from omitted OUs. |
| **Logon Activity** | |
| I want to omit domain logons by a specific service account or service accounts with specific naming pattern. | [Logon Activity](LogonActivity/Overview.htm "Logon Activity") |
| **File Servers**  (including Windows file server, Dell, NetApp, Nutanix File server) | |
| I have a server named *StationWin16* where I can't install .Net 4.5 in OU where I keep all member servers. I want to suppress errors from this server by excluding it from the Netwrix auditing scope. | [AD Container](ActiveDirectory/Overview.htm#AD "AD Container") |
| A Security Officer wants to monitor a file share but s/he does not have access to a certain folder on this share. Then, s/he does not want the product to monitor this folder at all. | [File Servers](FileServers/Overview.htm#Computer "Computer")  [Dell Isilon](FileServers/Overview.htm#Dell "Dell Isilon")  [Dell VNX VNXe](FileServers/Overview.htm#Dell2 "Dell VNX VNXe")  [NetApp](FileServers/Overview.htm#NetApp "NetApp")  [Windows File Share](FileServers/Scope.htm#Windows "Windows File Share")  [Nutanix SMB Shares](FileServers/Overview.htm#Nutanix "Nutanix SMB Shares") |
| A Security Officer wants to monitor a file share but s/he does not have access to a certain folder on this share. Then, s/he does not want the product to monitor this folder at all. | [File Servers](FileServers/Overview.htm#Computer "Computer")  [Dell Isilon](FileServers/Overview.htm#Dell "Dell Isilon")  [Dell VNX VNXe](FileServers/Overview.htm#Dell2 "Dell VNX VNXe")  [NetApp](FileServers/Overview.htm#NetApp "NetApp")  [Windows File Share](FileServers/Scope.htm#Windows "Windows File Share")  [Nutanix SMB Shares](FileServers/Overview.htm#Nutanix "Nutanix SMB Shares") |
| A Security Officer wants to monitor a file share, but it contains a folder with a huge amount of objects, so s/he does not want Netwrix Auditor to collect State-in-Time data for this folder. | [File Servers](FileServers/Overview.htm#Computer "Computer")  [Dell Isilon](FileServers/Overview.htm#Dell "Dell Isilon")  [Dell VNX VNXe](FileServers/Overview.htm#Dell2 "Dell VNX VNXe")  [NetApp](FileServers/Overview.htm#NetApp "NetApp")  [Windows File Share](FileServers/Scope.htm#Windows "Windows File Share")  [Nutanix SMB Shares](FileServers/Overview.htm#Nutanix "Nutanix SMB Shares") |
| I want to exclude specific computers within an IP range from the Netwrix auditing scope. | [File Servers](FileServers/Overview.htm#IP "IP Range") |
| **SQL Server** | |
| I want to know if *corp\administrator* user is messing with SQL data. | [SQL Server Instance](SQLServer/Items.htm#SQL "SQL Server Instance") |
| As a Auditor administrator I want to exclude the *domain\nwxserviceaccount* service account activity from SQL server audit so that I get reports without changes made by automatic systems. | [SQL Server Instance](SQLServer/Items.htm#SQL "SQL Server Instance") |
| As a Auditor administrator I want to exclude all changes performed by *MyCustomTool*. | [SQL Server Instance](SQLServer/Items.htm#SQL "SQL Server Instance") |
| **SharePoint** | |
| I want to exclude the *domain\nwxserviceaccount* account from data collection as it produces standard activity that doesn't require monitoring. | [SharePoint Farm](SharePoint/Overview.htm#SharePoi "SharePoint Farm") |
| As a Auditor Administrator I want to exclude shared *PublicList* from read audit. | [[SharePoint Farm](SharePoint/Overview.htm#SharePoi "SharePoint Farm")](../../Solutions/Items/SharePointFarm) |
| Windows Server | |
| I have a server named StationWin16 where I can't install .Net 4.5 in OU where I keep all member servers. I want to suppress errors from this server by excluding it from the Netwrix auditing scope. | [AD Container](ActiveDirectory/Overview.htm#AD "AD Container") |
| I want to exclude specific computers within an IP range from the Netwrix auditing scope. | [File Servers](FileServers/Overview.htm#IP "IP Range") |
| VMware | |
| I have a virtual machine named "testvm" I use for testing purposes, so I want to exclude it from being monitored. | [VMware ESX/ESXi/vCenter](VMware/Overview.htm#VMware "VMware ESX/ESXi/vCenter") |