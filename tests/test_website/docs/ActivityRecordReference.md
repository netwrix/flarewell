---
title: "Reference for Creating Activity Records"
sidebar_position: 698
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

# Reference for Creating Activity Records

The table below describes Activity Record elements.

Netwrix recommends limiting the input Activity Records file to 50MB and maximum 1,000 Activity Records.

| Element | Mandatory | Datatype | Description |
| --- | --- | --- | --- |
| Activity Record main elements | | | |
| RID | No | string | RID is a unique key of the Activity Record.  The identifier is created automatically when you write an Activity Record to the Audit Database. RID is included in output Activity Records only. |
| Who | Yes | nvarchar 255 | A specific user who made the change (e.g., *Enterprise Administrator*, *Admin@enterprise.onmicrosoft.com*). |
| Action | Yes | — | Activity captured by Auditor (varies depending on the data source): |
| What | Yes | nvarchar  max | A specific object that was changed (e.g., *NewPolicy*). |
| When | Yes | dateTime | The moment when the change occurred. When supports the following datetime formats: |
| Where | Yes | nvarchar 255 | A resource where the change was made (e.g., *Enterprise-SQL*, *FileStorage.enterprise.local*). The resource name can be a FQDN or NETBIOS server name, Active Directory domain or container, SQL Server instance, SharePoint farm, VMware host, etc. |
| ObjectType | Yes | nvarchar 255 | An type of affected object or its class (e.g., *user, mailbox*). |
| Monitoring Plan | No | nvarchar 255 | The Auditor object that responsible for monitoring of a given data source and item.  Sub-elements: Name and ID.  If you provide a monitoring plan name for input Activity Records, make sure the plan is created in Auditor, the Netwrix API data source is added to the plan and enabled for monitoring. In this case, data will be written to the database associated with this plan. |
| DataSource | No | nvarchar  max | IT infrastructure monitored with Auditor (e.g., *Active Directory*).  For input Activity Records, the data source is automatically set to Netwrix API. |
| Item | No | nvarchar  max | The exact object that is monitored (e.g., a domain name, SharePoint farm name) or integration name.  Sub-element: Name.  The item type is added inside the name value in brackets (e.g., *enterprise.local (Domain)*). For input Activity Records, the type is automatically set to Integration, you do not need to provide it. The output Activity Records may contain the following item types depending on the monitoring plan configuration:   |  |  | | --- | --- | | * AD container | * NetApp | | * Computer | * Office 365 tenant | | * Domain | * Oracle Database instance | | * EMC Isilon | * SharePoint farm | | * Dell VNX/VNXe | * SQL Server instance | | * Integration | * VMware ESX/ESXi/vCenter | | * IP range | * Windows file share |   If you provide an item name for input Activity Records, make sure this item is included in the monitoring plan within the Netwrix API data source. If you specify an item that does not exist, data will be written to the plan's database anyway but will not be available for search using the Item filter. |
| Workstation | No | nvarchar  max | An originating workstation from which the change was made (e.g., *WKSwin12.enterprise.local*). |
| IsArchiveOnly | No | — | IsArchiveOnly allows to save Activity Record to the Long-Term Archive only. In this case, these Activity Records will not be available for search in the Auditor client. |
| DetailList | No | — | Information specific to the data source, e.g., assigned permissions, before and after values, start and end dates. References details. |
| Detail sub-elements (provided that DetailList exists) | | | |
| PropertyName | Yes | nvarchar 255 | The name of a modified property. |
| Message | No | string | Object-specific details about the change.  Message is included in output Activity Records only. |
| Before | No | ntext | The previous value of the modified property. |
| After | No | ntext | The new value of the modified property. |