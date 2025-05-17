---
sidebar_position: 30
title: Resource Audit Overview
---

# Resource Audit Overview

The Resource Audit interface is where Netwrix Access Information Center users view reports on resources that Access Analyzer has collected data for. For the purposes of the Access Information Center, a resource refers to file system servers, SharePoint farms, shared folders, and so on. Reports include permissions, effective access, membership, user activity, changes, and sensitive criteria matches. Most Access Analyzer solutions can send data to the Access Information Center. Additionally, the Access Information Center Flexible Imports feature and Access Analyzer's AnyID Connectors solution can be used to introduce data from target environments not available with the default solutions. See the All Solutions topic of the [Netwrix Access Analyzer Documentation](https://helpcenter.netwrix.com/category/accessanalyzer "Netwrix Access Analyzer Documentation") for additional information on the data collection options.

The Access Information Center search features, found on the home page, can be used to open the other audit interfaces. These other interfaces show reports on users, groups, computers, and sensitive content.

The Access Information Center can also be used to model changes to file system permissions, allowing the Access Information Center user to understand what changes in group membership are needed to modify access to a specific resource, as well as the impact such a change would have across the organization's other resources.

## Resource Reports

The Resource reports provide insight into:

* The permissions applied to a particular resource
* The effective access to a particular resource
* What users and groups doing with their access
* What potentially sensitive data exists across the targeted environment

See the following topics for additional information on specific resource reports:

* [File System Reports](FileSystem/Overview "File System Reports")
* [SharePoint Reports](SharePoint/Overview "SharePoint Reports")
* [Active Directory Reports](ActiveDirectory/Overview "Active Directory Reports")
* [Amazon (AWS) Reports](AWS/Overview) Reports")
* [Dropbox Reports](Dropbox/Overview "Dropbox Reports")
* [Exchange Reports](Exchange/Overview "Exchange Reports")
* [MongoDB Reports](MongoDB/Overview "MongoDB Reports")
* [MySQL Reports](MySQL/Overview "MySQL Reports")
* [Oracle Reports](Oracle/Overview "Oracle Reports")
* [PostgreSQL Reports](PostgreSQL/Overview "PostgreSQL Reports")
* [SQL Server Reports](SQL/Overview "SQL Server Reports")
* [Flexible Imports Feature](FlexibleImports/Overview "Flexible Imports Feature")

## User Reports

The User reports provide insight into:

* The resources a particular user has access to
* What a user is doing with their access

See the [User Reports](User/Overview "User Reports") topic for additional information.

## Group Reports

The Group reports provide insight into:

* The resources a particular group has access to
* The members of the group
* What group membership changes have occurred

See the [Group Reports](Group/Overview "Group Reports") topic for additional information.

## Computer Reports

The Computer reports provide insight into:

* Everywhere a particular computer has access
* What a computer is doing with it's access
* What Active Directory permissions are applied to the computer object

See the [Computer Reports](Computer/Overview "Computer Reports") topic for additional information.

## Sensitive Content Reports

The Sensitive Content reports provide insight into which files contain specific sensitive data.

See the [Sensitive Content Reports](SensitiveContent/Overview "Sensitive Content Reports") topic for additional information.

## Flexible Imports

Reports associated with the flexible imports provide insight into:

* The permissions applied to a particular resource
* What trustees are doing with their access
* What potentially sensitive data exists across the targeted environment

See the [Flexible Imports Feature](FlexibleImports/Overview "Flexible Imports Feature") topic for additional information.

## Access & Membership Change Modeling

Access and membership change modeling allows Access Information Center users to see what steps must be taken to adjust a trustee’s access to a specific resource, as well as what impact the changes will have on that trustee’s access across the targeted file system and Active Directory environments.

See the [Change Modeling](ChangeModeling/Overview "Change Modeling") topic for additional information.