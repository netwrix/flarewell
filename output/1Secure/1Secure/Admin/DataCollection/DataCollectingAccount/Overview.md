---
sidebar_position: 70
title: Data Collecting Account
---

Filter: 

* All Files

Submit Search

# Data Collecting Account

The data collecting account is a service account that Netwrix 1Secure uses to collect audit data from the monitored items (domains, OUs, servers, etc.). Netwrix recommends creating a dedicated service account for that purpose. Depending on the data source and connector, the account must meet the corresponding requirements (see the table below).

You can use group Managed Service Account (gMSA) as data collecting account. See the [Using Group Managed Service Account (gMSA)](../GMSA/GMSA)") topic for additional information.

Currently, the following data sources are supported:

| Data source | Provided connectors | Required rights and permissions: |
| --- | --- | --- |
| Active Directory | Active Directory Activity  Active Directory Logons | [Active Directory Auditing](../ActiveDirectory/ActiveDirectoryAuditing "Active Directory Auditing")  [Logon Activity Auditing](../LogonActivity/Overview "Logon Activity Auditing") |
| Azure AD | Azure AD Activity  Azure AD Logons | [Microsoft Entra ID Auditing](../EntraID "Microsoft Entra ID Auditing") |
| Computer | File Server Activity | [Computer Auditing](../Computer/Overview "Computer Auditing") |
| SharePoint Online | SharePoint Online Activity | [SharePoint Online Auditing](../SharePointOnline "SharePoint Online Auditing") |
| Exchange Online | Exchange Online Activity | [Exchange Online Auditing](../ExchangeOnline "Exchange Online Auditing") |