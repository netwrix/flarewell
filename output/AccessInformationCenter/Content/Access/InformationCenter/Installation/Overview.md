---
sidebar_position: 14
title: Installation Overview
---

# Installation Overview

The Netwrix Access Information Center relies on collected and analyzed data that is stored in a Microsoft® SQL® Server database. Netwrix Access Analyzer (formerly Enterprise Auditor) must be installed, and there are specific solutions that are prerequisites for installing and using the Access Information Center.

## Prerequisites

The Access Information Center is typically installed on the same server as Access Analyzer. However, it can be installed on a remote server. See the [Remote AIC Console Sever Requirements](#Remote "Remote AIC Console Sever Requirements") topic for additional information.

### Access Analyzer Solutions

The .Active Directory Inventory Solution must be successfully executed prior to installing the Access Information Center.

***RECOMMENDED:*** Successfully execute other solutions, like File System or SharePoint, which supply the data for Resource Audits.

### Permissions

Permissions are needed to the Access Analyzer database and to Active Directory. This can be one account with sufficient rights to each or two separate accounts. For the purpose of this document, these will be referred to as the Database service account and the Active Directory service account.

* Database service account – Typically, this is the same account used by Access Analyzer for a database service account. This credential is required for installation.

  * If you choose to use a different account, it must have the following permissions:

    * Database Owner
    * Provisioned to use Default Schema of ‘dbo’
  * Database connection via TLS 1.2 (SQL Native Client) is supported.
* Active Directory service account – At a minimum, Access Information Center login authentication and Resource Audits require the Active Directory service account to have rights to read Active Directory. This credential is configured during installation based on the account used for connecting to the database. See the [Active Directory Page](../Admin/Configuration/ActiveDirectory "Active Directory Page") topic for additional information.

Commit Active Directory Changes

If configured and enabled, the Access Information Center can commit group membership changes within Active Directory. This is an optional component of change modeling, resource owner ad hoc changes, and the Entitlement Reviews workflow. It is a requirement for the Self-Service Access Requests workflow.

In order for the Access Information Center to commit changes to Active Directory, Active Directory service account must have additional rights on the OUs that house the security and distribution groups to be managed:

* Allow Read Members
* Allow Write Members

See the [Commit Active Directory Changes](../Admin/AdditionalConfig/CommitChanges "Commit Active Directory Changes") topic for additional information and best practices.

### SSL Certificate

To enable Secure Sockets Layer (SSL) for secure remote connections to the Access Information Center, a password-enabled certificate with a private key is required. This certificate should reside in a local folder for browsing prior to installing the Access Information Center. The certificate can also be in any of the Local Machine certificate stores.

### Remote AIC Console Sever Requirements

If it is necessary to install the Access Information Center on a server separate from the Access Analyzer Console, the following minimal server requirements are needed for Access Reporting:

* Windows Server 2016 through Windows Server 2022

  * US English language installation
  * Domain member

* 2+ CPU Cores
* 4+ GB RAM
* 20+ GB Disk Space
* .NET Framework 4.7.2+

**NOTE:** If utilizing any of the Access Information Center workflows (Resource Reviews or Self-Service Access Requests), additional CPU cores, memory, and disk space may be needed.

## Software Compatibility & Versions

For proper functionality, it is necessary for the version of the Access Information Center to be compatible with the existing Access Analyzer installation. If necessary, [Netwrix Support](https://www.netwrix.com/support.html "Netwrix Support") can confirm whether the two product versions are compatible.

Latest Version Compatibility

| Component | Current Version |
| --- | --- |
| Netwrix Access Analyzer (formerly Enterprise Auditor) | Ver. 12.0\* |
| Netwrix Access Information Center | Ver. v12.0\* |

See the [Upgrade Procedure](Upgrade "Upgrade Procedure") topic for additional information.

## Supported Browsers

Supported browsers for the Netwrix Access Information Center include:

* Google® Chrome®
* Microsoft® Edge®
* Mozilla® Firefox®

## Screen Resolution Requirement

Supported screen resolution of 1368 x 768 or greater.