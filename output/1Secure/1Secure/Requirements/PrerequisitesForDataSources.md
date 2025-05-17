---
sidebar_position: 24
title: Prerequisites for Data Sources
---

Filter: 

* All Files

Submit Search

# Prerequisites for Data Sources

This section lists platforms and systems that can be monitored with Netwrix 1Secure.

* Active Directory

* Microsoft Entra ID (formerly Azure AD)

* Computer (Windows File Share)
* SharePoint Online
* Exchange Online

| Data source | Supported Versions |
| --- | --- |
| Active Directory  (including Logon Activity) | Domain Controller OS versions:   * Windows Server 2022 * Windows Server 2019 * Windows Server 2016 * Windows Server 2012 R2 |
| Microsoft Entra ID | Microsoft Entra ID version provided within Microsoft Office 365  You may need to take some preparatory steps, depending on the authentication method you want to use for collecting Azure AD and Office 365 data. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information. |
| Computer (Windows File Server) | * Windows Server OS:   * Windows Server 2022   * Windows Server 2019   * Windows Server 2016   * Windows Server 2012 R2 * Windows Desktop OS (32 and 64-bit):   * Windows 10   * Windows 8.1   * Windows 7   Consider the following:   * To collect data from 32-bit operating systems, network traffic compression must be disabled. * To collect data from Windows Failover Cluster, network traffic compression must be enabled. * Scale-Out File Server (SOFS) cluster is not supported. |
| SharePoint Online | Azure Active Directory version provided within Microsoft Office 365  You may need to take some preparatory steps, depending on the authentication method you want to use for collecting SharePoint Online and One Drive for Business. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information. |
| Exchange Online | Azure Active Directory version provided within Microsoft Office 365  You may need to take some preparatory steps, depending on the authentication method you want to use for collecting Exchange Online. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information. |