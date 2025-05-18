---
title: "Windows Server Registry Keys"
sidebar_position: 1041
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

# Windows Server Registry Keys

Review the basic registry keys that you may need to configure for monitoring Windows Server with Netwrix Auditor. Navigate to Start → Run and type *"regedit"*.

| Registry key (REG_DWORD type) | Description / Value |
| --- | --- |
| HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Netwrix Auditor\Windows Server Change Reporter | |
| CleanAutoBackupLogs | Defines the retention period for the security log backups:   * 0—Backups are never deleted from Domain controllers * [X]— Backups are deleted after [X] hours |
| ProcessBackupLogs | Defines whether to process security log backups:   * 0—No * 1—Yes   Even if this key is set to *"0"*, the security log backups will not be deleted regardless of the value of the CleanAutoBackupLogs key. |

## Event Log

Review the basic registry keys that you may need to configure for monitoring event logs with Netwrix Auditor. Navigate to Start → Run and type *"regedit"*.

| Registry key (REG_DWORD type) | Description / Value |
| --- | --- |
| HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432NODE\Netwrix Auditor\Event Log Manager\\Database Settings | |
| ConnectionTimeout | Defines SQL database connection timeout (in seconds). |
| BatchTimeOut | Defines batch writing timeout (in seconds). |
| DeadLockErrorCount | Defines the number of write attempts to a SQL database. |
| HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432NODE\Netwrix Auditor\Event Log Manager | |
| CleanAutoBackupLogs | Defines the retention period for the security log backups:   * 0—Backups are never deleted from Domain controllers * [X]— Backups are deleted after [X] hours |
| ProcessBackupLogs | Defines whether to process security log backups:   * 0—No * 1—Yes   Even if this key is set to *"0"*, the security log backups will not be deleted regardless of the value of the CleanAutoBackupLogs key. |
| WriteAgentsToApplicationLog | Defines whether to write the events produced by the Netwrix Auditor Event Log Compression Service to the Application Log of a monitored machine:   * 0—Disabled * 1—Enabled |
| WriteToApplicationLog | Defines whether to write events produced by Netwrix Auditor to the Application Log of the machine where the product is installed:   * 0—No * 1—Yes |