---
sidebar_position: 75
title: File System Reports Quick Reference Guide
---

# File System Reports Quick Reference Guide

The following File System reports are available for selections within the Resources pane.

## File System Node Reports

The following reports are available at the File System node level:

| Report | Description |
| --- | --- |
| [Activity Summary Report](ActivitySummary "Activity Summary Report") | Provides an overview of activity performed on files and folders in each of the scanned servers. It reflects the total count of operations performed in each server, including activity in folders that are not shared. This is an activity report that does not include a date range filter, as it contains totals for all operations ever monitored by Access Analyzer for the targeted environment. |
| [Exceptions Report](Exceptions "Exceptions Report") | Provides a list of exceptions that were found across the targeted environment. This report includes a Details table. |
| [Modeled Access Changes Report](../ChangeModeling/ModeledAccessChanges "Modeled Access Changes Report") | Provides an enterprise wide view of modeled access changes. This report is blank if no changes have been modeled or if the modeled changes have no impact on the environment. This report includes the following tables:   * Permission Source – Displays all of the ways the trustee has been granted rights to the resource * Activity – Displays additional information on recent activity performed by the trustee which would have been impacted by the modeled change |
| [Sensitive Content Summary Report](SensitiveContentSummary "Sensitive Content Summary Report") | Provides a count of files where criteria matches were found in the targeted environment. This report includes a Details table. |
| [Server Summary Report](ServerSummary "Server Summary Report") | Provides a top-level view of servers that have been scanned. |

## File System > Server Level Reports

The following reports are available at the server level:

| Report | Description |
| --- | --- |
| [Activity Details Report](Server/ActivityDetails "Activity Details Report") | Provides details on every operation logged during the selected date range. Activity on DFS Namespaces at this level is rolled up to the server hosting the DFS Namespace. This report includes a Permission Changes table. |
| [Activity Statistics Report](Server/ActivityStatistics "Activity Statistics Report") | Provides statistical activity event information by user on the selected server during the specified date range. Activity on DFS Namespaces at this level is rolled up to the server hosting the DFS Namespace. This report includes line graphs for Active Users Trend and Traffic Trend. |
| [Exceptions Report](Server/Exceptions "Exceptions Report") | Provides a list of exceptions that were found within shares on the selected server. This report includes a Details table. |
| [Scan Summary Report](Server/ScanSummary "Scan Summary Report") | Provides a summary view of all shares on the selected server. |
| [Sensitive Content Details Report](Server/SensitiveContentDetails "Sensitive Content Details Report") | Provides details of files where criteria matches were found on the selected resource. This report includes a Matches table. |
| [Sensitive Content Summary Report](Server/SensitiveContentSummary "Sensitive Content Summary Report") | Provides a count of files where criteria matches were found on the selected resource. This report includes a Details table. |
| [Share Activity Summary Report](Server/ShareActivitySummary "Share Activity Summary Report") | Provides statistical activity event information by share on the selected server during the specified date range. Activity on DFS Namespaces at this level is rolled up to the server hosting the DFS Namespace. |

## File System > Server > Local Policies > Policy Level Reports

The following reports are available at the local policy level:

**NOTE:** There are no reports at the Local Policies node level.

| Report | Description |
| --- | --- |
| [Effective Policy Report](LocalPolicies/EffectivePolicy "Effective Policy Report") | Provides a list of users and groups who are effectively granted or denied access through the selected policy. |
| [Policy Report](LocalPolicies/Policy "Policy Report") | Provides a list of policies assigned for the selected local policy. |

## File System > Server > NFS Exports Node Report

The following report is available at the NFS Exports node level:

| Report | Description |
| --- | --- |
| [Scan Summary Report](NFSExports/ScanSummary "Scan Summary Report") | Provides a summary view of all shares on the server with the share type of Shared. |

## File System > Server > NFS Exports > Share & Subfolder Levels

The following reports are available at the share and subfolder levels under the NFS Exports node:

| Report | Description |
| --- | --- |
| [Activity Details Report](NFSExports/ActivityDetails "Activity Details Report") | Provides details on every operation logged during the selected date range. This report includes a Permission Changes table. |
| [Activity Statistics Report](NFSExports/ActivityStatistics "Activity Statistics Report") | Provides statistical activity event information by user on the selected resource during the specified date range. This report includes line graphs for Active Users Trend and Traffic Trend. |
| [Permissions Report](NFSExports/Permissions "Permissions Report") | Provides a list of trustees with permissions for the selected resource and access level for each trustee. |
| [Sensitive Content Report](NFSExports/SensitiveContent "Sensitive Content Report") | Provides a list of files and a hit count per file where criteria matches were found on the selected resource. This report includes a table with criteria matches visible to Access Information Center users with either Administrator or Security Team roles. The Matches table requires the store discovered sensitive data configuration for the Access Analyzer data collection or it will be blank. |

## File System > Server > Admin Shares Nodes Report

The following report is available at the Admin Shares node level:

| Report | Description |
| --- | --- |
| [Scan Summary Report](AdminShares/ScanSummary "Scan Summary Report") | Provides a summary view of all shares on the server with the share type of Admin. |

## File System > Server > Shared Folders Node Report

The following report is available at the Shared Folders node level:

| Report | Description |
| --- | --- |
| [Scan Summary Report](SharedFolders/ScanSummary "Scan Summary Report") | Provides a summary view of all shares on the server with the share type of Shared. |

## File System > Server > Shared Folders > Share & Subfolder Level Reports

The following reports are available at the share and subfolder levels:

| Report | Description |
| --- | --- |
| [Activity Details Report](ShareSubfolder/ActivityDetails "Activity Details Report") | Provides details on every operations logged during the selected date range. This report includes a Permission Changes table. |
| [Activity Statistics Report](ShareSubfolder/ActivityStatistics "Activity Statistics Report") | Provides statistical activity event information by user on the selected server during the specified date range This report includes line graphs for Active Users Trend and Traffic Trend. |
| [Effective Access Report](ShareSubfolder/EffectiveAccess "Effective Access Report") | Provides insight into who has what level of access to this resource through a calculation that encompasses server policies, share and folder permissions, and group membership. It contains a list of all trustees with access to the selected resource and specifies the effective access level. This report includes a Permission Source table. |
| [Exceptions Report](ShareSubfolder/Exceptions "Exceptions Report") | Displays a list of all trustees with access that are causing exceptions on the selected resource. This report includes a Permission Source table. |
| [Permissions Report](ShareSubfolder/Permissions "Permissions Report") | Provides a list of trustees with permissions for the selected resource. This report includes a table with trustee access levels Compared to Parent. |
| [Sensitive Content Report](ShareSubfolder/SensitiveContent "Sensitive Content Report") | Provides a list of files and a hit count per file where criteria matches were found on the selected resource. This report includes a table with criteria matches visible to Access Information Center users with either Administrator or Security Team roles. The Matches table requires the store discovered sensitive data configuration for the Access Analyzer data collection or it will be blank. |

## File System > Server > Exceptions Node Report

The following report is available at the Exceptions node level:

| Report | Description |
| --- | --- |
| [Exceptions Report](Exceptions/Exceptions "Exceptions Report") | Provides a list of exceptions found on the server. This report includes a Details table. |

## File System > Server > Exceptions > Exception Type Level Report

The following report is available at the exceptions type level:

| Report | Description |
| --- | --- |
| [Exceptions Report by Type](Exceptions/ExceptionsByType "Exceptions Report by Type") | Provides details on the selected exception type. This report includes a Permission Source table. |