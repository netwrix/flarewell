---
title: "CIM Data Model Mapping"
sidebar_position: 815
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

# CIM Data Model Mapping

The Splunk Common Information Model (CIM) is installed with an add-on and adds a set of data models that allow data normalization to simplify search.

The CIM contains a number of standard data models that can be used for search. Each of them has predefined set of standard fields common for different data sources.

Netwrix Auditor Add-on for Splunk will map some of the Activity Records that match certain scenario to the respective CIM data models.

| Criteria | Data model | Description |
| --- | --- | --- |
| DataSource IN ("Microsoft Entra ID", "Logon Activity", "SQL Server", "VMware") Action="Successful Logon" | Authentication \> Authentication \> Successful_Authentication | Successful login events |
| DataSource IN ("Microsoft Entra ID", "Logon Activity", "SQL Server", "VMware") Action="Failed Logon" | Authentication \> Authentication \> Failed_ Authentication | Failed login events |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*") Action="Added" ObjectType IN ("user", "computer", "inetorgperson", "service principal", "mail contact", "mail user") | Change \> All_Changes \> Account Management \> Created Accounts | Account creation events |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*") Action IN ("Modified", "Moved") ObjectType IN ("user", "computer", "inetorgperson", "service principal", "mail contact", "mail user") | Change \> All_Changes \> Account Management \> Updated Accounts | Account update events |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*") Action="Removed" ObjectType IN ("user", "computer", "inetorgperson", "service principal", "mail contact", "mail user") | Change \> All_Changes \> Account Management \> Deleted Accounts | Account deletion events |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*", "File Servers") Action IN ("Added", "Modified", "Moved", "Removed") NOT ObjectType IN ("user", "computer", "inetorgperson", "service principal", "mail contact", "mail user") | Change \> All_Changes | All other – not related to accounts – changes |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*") ObjectType IN ("user", "computer", "inetorgperson", "service principal", "mail contact", "mail user") is_ lockout=1 | Change \> All_Changes \> Account Management \> Locked Accounts | Account lockout events |
| DataSource IN ("Active Directory", "Microsoft Entra ID", "Exchange\*") Action IN ("Added", "Modified", "Removed") is_audit=1 | Change \> All_Changes \> Auditing Changes | Changes to audit settings or policies |
| DataSource="Exchange\*" ObjectType="Mailbox Item" Action IN ("Sent", "Removed") | Email \> All Email | Information related to sent or received emails |
| DataSource="File Server" Action IN ("Added". "Modified", "Moved", "Removed", "Renamed") ObjectType IN ("file", "folder") | Endpoint \> Filesystem | Changes to file shares |