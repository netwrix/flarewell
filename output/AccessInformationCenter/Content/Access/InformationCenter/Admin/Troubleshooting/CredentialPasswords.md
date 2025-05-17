---
sidebar_position: 294
title: Update Credential Passwords
---

# Update Credential Passwords

Credential passwords occasionally need to be updated due to various reasons, such as security policies that require passwords to be reset on a regular basis. The following types of credentials may be impacted by password changes or security policies:

* Database service account
* Active Directory service account
* SMTP authentication service account
* Application Service Account
* Bultin Administrator account

## Database Service Account

The Database service account grants access to the SQL Server database. It can be updated on the Database page of the Configuration interface. See the [Update the Database Service Account Password](../Configuration/Database#Update "Update the Database Service Account Password") topic for instructions.

## Active Directory Service Account

The Active Directory service account handles user authentication to the Access Information Center. It can be updated on the Active Directory page of the Configuration interface. It is also used to commit changes in Active Directory, if that feature has been enabled. See the [Update the Active Directory Service Account Password](../Configuration/ActiveDirectory#Update "Update the Active Directory Service Account Password") topic for instructions.

## SMTP Authentication Service Account

An SMTP server is required for the application to send notifications. If the SMTP server requires authentication, the service account can be updated on the Notifications page of the Configuration interface. See the [Configure SMTP Server Settings](../Configuration/Notifications#Configur "Configure SMTP Server Settings") topic for instructions.

## Builtin Administrator Account

The Builtin Administrator account is an application account that is created during the first launch. It is used to complete the initial configuration steps and to grant console access to domain users. This account can be disabled after Administrator users are added. However, if it is enabled and a security policy requires the password to be reset, it can be updated on the Console Access page of the Configuration interface. See the [Modify the Builtin Administrator Account](../Configuration/ConsoleAccess#Modify "Modify the Builtin Administrator Account") topic for modification instructions.