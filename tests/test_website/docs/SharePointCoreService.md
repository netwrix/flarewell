---
title: "Install for SharePoint Core Service"
sidebar_position: 674
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

# Install for SharePoint Core Service

This section contains instructions on how to install Netwrix Auditor for SharePoint Core Service.

During the Netwrix Auditor for SharePoint Core Service installation / uninstallation your SharePoint sites may be unavailable.

Prior to the Netwrix Auditor for SharePoint Core Service installation, review the following prerequisites and make sure that:

* Netwrix Auditor for SharePoint Core Service is going to be installed on the computer that hosts SharePoint Central Administration in the audited SharePoint farm.
* [.Net Framework 3.5 SP1](`http://www.microsoft.com/en-us/download/details.aspx?id=22`) is installed on the computer that hosts SharePoint Central Administration in the audited SharePoint farm.
* The SharePoint Administration (SPAdminV4) service is started on the target computer. See [SharePoint](../Configuration/SharePoint/Overview.htm "SharePoint") for more information.
* The user that is going to run the Core Service installation:
  + Is a member of the local Administrators group on SharePoint server, where the Core Service will be deployed.
  + Is granted the SharePoint_Shell_Access role on SharePoint SQL Server configuration database. See [Permissions for SharePoint Auditing](../Configuration/SharePoint/Permissions.htm "Permissions for SharePoint Auditing") topic for more information.

Follow the steps to install Netwrix Auditor for SharePoint Core Service manually.

**Step 1 –** On the computer where Auditor Server resides,navigate to *%Netwrix Auditor installation folder%\SharePoint Auditing**\SharePointPackage* and copy SpaPackage_\.msi to the computer where Central Administration is installed.

**Step 2 –** Run the installation package.

**Step 3 –** Follow the instructions of the setup wizard. When prompted, accept the license agreement and specify the installation folder.