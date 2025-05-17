---
sidebar_position: 73
title: Configure Non-Administrative Account to Collect Logon Activity
---

Filter: 

* All Files

Submit Search

# Configure Non-Administrative Account to Collect Logon Activity

This section contains instructions on how to configure an account to collect Logon Activity with minimum rights assignment. The instructions below apply only if you are going to set a source with disabled network traffic compression and do not want to adjust audit settings automatically. Do the following:

Before creating an account, grant the *Read* permission on the SECURITY registry key `(HKEY_LOCAL_MACHINE\SECURITY)` for an admin account under which you will make changes in Group Policy.

Do the following:

**Step 1 –** Create a domain user with the following privileges:

* Back up files and directories. [Configure the Back up Files and Directories Policy](../Computer/BackupFilesDirectories "Configuring 'Back up Files and Directories' Policy")
* Log on as a batch job. [Define Log On As a Batch Job Policy](../ActiveDirectory/LogOnAsBatch "Define Log On As a Batch Job Policy")
* Manage auditing and security log. [Configure the Manage Auditing and Security Log Policy](../ActiveDirectory/ManageAuditingSecurityLog "Configuring 'Manage Auditing and Security Log' Policy")

**Step 2 –** Grant the *Read* permission on the following registry keys to this user:

* HKEY\_LOCAL\_MACHINE\SECURITY\Policy\PolAdtEv
* HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Control\SecurePipeServers\winreg
* HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Security

[Assigning Permission To Read the Registry Key](../ActiveDirectory/PermissionsRegistryKeys "Assigning Permission To Read the Registry Key") how to do it using Registry Editor.