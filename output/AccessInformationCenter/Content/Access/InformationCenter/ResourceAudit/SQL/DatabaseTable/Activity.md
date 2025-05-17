---
sidebar_position: 134
title: Activity Report
---

# Activity Report

The Activity report at the database and table levels displays activity on the selected resource logged during the selected date range. The **Include Subfolders** option is active by default until removed. See the [Results Pane](../../Navigate/Overview#Results "Results Pane") topic for information on changing this option.

![Activity report at the database and table levels](../../../../../../../../static/Content/Resources/Images/Access/InformationCenter/ResourceAudit/SQL/DatabaseActivity.png "Activity report at the database and table levels")

This report is comprised of the following columns:

* Access Time – Date and timestamp for when the operation occurred
* Trustee Name – Owner of the trustee account
* Trustee Account – Active Directory account associated with the trustee
* Department – Department to which the trustee account belongs
* Title – Trustee’s title as read from Active Directory
* Mail – Trustee’s email account as read from Active Directory
* EmployeeId – Corporate ID for the employee as read from Active Directory
* Description – Description of the trustee object as read from Active Directory
* DistinguishedName – Distinguished name for the trustee accountt
* ObjectSid – Security ID of the object
* Disabled – True or False if trustee account is disabled
* Deleted – True or False if trustee account is deleted
* Resource – Type of resource
* Operation – Type of operation performed
* Access – Whether the trustee was granted access to execute the operation: **Allowed** or **Denied**
* Path – Database object that was acted upon
* Target Path – Query that triggered the activity event to be stored
* Process Name – Not populated for SQL Server reports

The table data grid functions the same way as other table grids. See the [Data Grid Features](../../../../General/DataGrid "Data Grid Features") topic for additional information.