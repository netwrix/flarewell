---
sidebar_position: 219
title: Activity Details Report for Entra ID User
---

# Activity Details Report for Entra ID User

The Activity Details report for an Entra ID (formerly Azure Active Directory) user object provides details on every activity event logged by the audited user during the selected date range. This report includes a Permission Changes table.

![Activity Details report for an Entra ID user](../../../../../Resources/Images/Access/InformationCenter/ResourceAudit/User/ActivityDetailsEntraID.PNG "Activity Details report for an Entra ID user")

This report is comprised of the following columns:

* Collector – Refers to the collection source for the permission (for example, **FileSystem** for the Access Analyzer File System Solution, **SharePoint** for the Access Analyzer SharePoint Solution, and so on)
* Server Name – Name of the file system server or SharePoint farm/instance where the activity event occurred
* Access Time – Date and timestamp for when the operation occurred
* Resource – Resource type being accessed
* Operation – Name of operation logged
* Access – Whether the trustee was granted access to execute the operation: **Allowed** or **Denied**
* Path – Original location where the operation occurred