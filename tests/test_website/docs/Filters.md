---
title: "Filters"
sidebar_position: 700
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

# Filters

Review the table below to learn more about filters. The filters correspond to Activity Record fields.

| Filter | Description | Supported Operators |
| --- | --- | --- |
| RID | Activity Record ID. Limits your search to a unique key of the Activity Record.  Max length: 49. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Who | Limits your search to a specific user who made the change (e.g., *Enterprise Administrator*, *administrator@enterprise.onmicrosoft.com*).  Max length: 255. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | | * InGroup | | * NotInGroup | |
| Where | Limits your search to a resource where the change was made (e.g., *Enterprise-SQL*, *FileStorage.enterprise.local*).  The resource name can be a FQDN or NETBIOS server name, Active Directory domain or container, SQL Server instance, SharePoint farm, VMware host, etc.  Max length: 255. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| ObjectType | Limits your search to objects of a specific type only (e.g., *user*).  Max length: 255. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| What | Limits your search to a specific object that was changed (e.g., *NewPolicy*) .  Max length: 1073741822. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| DataSource | Limits your search to the selected data source only (e.g., *Active Directory*).  Max length: 1073741822. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Monitoring Plan | Limits your search to a specific monitoring plan —Netwrix Auditor object that governs data collection.  Max length: 255. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Item | Limits your search to a specific item—object of monitoring—and its type provided in brackets.  The following item types are available:   |  |  | | --- | --- | | * AD container | * NetApp | | * Computer | * Office 365 tenant | | * Domain | * Oracle Database instance | | * EMC Isilon | * SharePoint farm | | * EMC VNX/VNXe | * SQL Server instance | | * Integration | * VMware ESX/ESXi/vCenter | | * IP range | * Windows file share |   Max length: 1073741822. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Workstation | Limits your search to an originating workstation from which the change was made (e.g., *WKSwin12.enterprise.local*).  Max length: 1073741822. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Detail | Limits your search results to entries that contain the specified information in Detail. Normally contains information specific to your data source, e.g., assigned permissions, before and after values, start and end dates.  This filter can be helpful when you are looking for a unique entry.  Max length: 1073741822. | |  | | --- | | * Contains (default) | |  | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Before | Limits your search results to entries that contain the specified before value in Detail.  Max length: 536870911. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| After | Limits your search results to entries that contain the specified after value in the Detail.  Max length: 536870911. | |  | | --- | | * Contains (default) | | * DoesNotContain | | * Equals | | * NotEqualTo | | * StartsWith | | * EndsWith | |
| Action | Limits your search results to certain actions:   |  |  | | --- | --- | | * Added | * Add (Failed Attempt) | | * Removed | * Remove (Failed Attempt) | | * Modified | * Modify (Failed Attempt) | | * Read | * Read (Failed Attempt) | | * Moved | * Move (Failed Attempt) | | * Renamed | * Rename (Failed Attempt) | | * Checked in | * Checked out | | * Discard check out | * Successful Logon | | * Failed Logon | * Logoff | | * Copied | * Sent | | * Session start | * Session end | | * Activated |  | | |  | | --- | | * Equals (default) | | * NotEqualTo | |
| When | Limits your search to a specified time range.  Netwrix Auditor supports the following for the When filter:   * Use Equals (default operator) or NotEqualTo operator * To specify time interval, use Within timeframe with one of the enumerated values (Today, Yesterday, etc.), and/or values in the To and From.   To and From support the following date time formats:   * YYYY-mm-ddTHH:MM:SSZ—Indicates UTC time (zero offset) * YYYY-mm-ddTHH:MM:SS+HH:MM—Indicates time zones ahead of UTC (positive offset) * YYYY-mm-ddTHH:MM:SS-HH:MM—Indicates time zones behind UTC (negative offset) | 1. Equals (default) 2. NotEqualTo 3. Within timeframe:  |  | | --- | | * Today | | * Yesterday | | * LastSevenDays | | * LastThirtyDays | | * Equals (default) | | * NotEqualTo |  2. From..To interval |
| WorkingHours | Limits your search to the specified working hours. You can track activity outside the business hours applying the *NotEqualTo* operator.  To and From support the following date time formats:   * HH:MM:SSZ—Indicates UTC time (zero offset) * HH:MM:SS+HH:MM—Indicates time zones ahead of UTC (positive offset) * HH:MM:SS-HH:MM—Indicates time zones behind UTC (negative offset) | |  | | --- | | * "From..To" interval | | * Equals (default) | | * NotEqualTo | |