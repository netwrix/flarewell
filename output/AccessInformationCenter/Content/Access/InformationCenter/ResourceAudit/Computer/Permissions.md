---
sidebar_position: 104
title: Permissions Report
---

# Permissions Report

The Permissions report for a computer object provides a list of all resources where the audited computer has been assigned permissions. The **Include Inherited** filter option is active by default, which means the report displays both direct and inherited permissions unless modified by the Access Information Center user. See the [Results Pane](../Navigate/Overview#Results "Results Pane") topic for information on filter options.

![Permissions report](../../../../../../../static/Content/Resources/Images/Access/InformationCenter/ResourceAudit/Computer/Permissions.png "Permissions report")

This report is comprised of the following columns:

* Collector – Refers to the collection source for the permission (for example, **FileSystem** for the Access Analyzer File System Solution, **SharePoint** for the Access Analyzer SharePoint Solution, and so on)
* Server Name – Name of the file system server or SharePoint farm/instance where the permission is set
* Type – Type of resource where the permission is set
* Source – Direct or Inherited permission type
* Path – Location of the resource where the permission is set
* Allow Mask – Bitmask corresponding to Windows ACE permission bits for combined direct and inherited allow rights
* Deny Mask – Bitmask corresponding to Windows ACE permission bits for combined direct inherited deny rights

The following rights are a normalized representation of the permissions granted to the trustee:

* List – Right to view list of resources
* Read – Right to view/read resources
* Write – Right to add or modify resources
* Delete – Right to delete resources
* Manage – Equivalent to full control over resources

The table data grid functions the same way as other table grids. See the [Data Grid Features](../../../General/DataGrid "Data Grid Features") topic for additional information.