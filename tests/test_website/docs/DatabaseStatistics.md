---
title: "Database Statistics"
sidebar_position: 963
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

# Database Statistics

Databases may tend to run out of free space due to poor capacity provisioning or to retention settings not configured properly. Use the Database statistics widget to examine database size and adjust retention accordingly. The widget displays the name of default SQL Server instance hosting all Netwrix Auditor databases, the overall database capacity at the moment and its change over the last day (24 hours).

Transaction logs size is not included in the calculations.

After you click View details, the following information will be displayed for the specified SQL Server instance:

[![](../static/img/Auditor/Images/Auditor/Health/DBStats_overview_thumb_0_0.png)](../../../../Resources/Images/Auditor/Health/DBStats_overview.png)

The Database name column contains the list of Netwrix Auditor databases hosted by the specified instance of the SQL Server:

* Special databases are created automatically on the default SQL Server instance to store:
  + alerts—*Netwrix_AlertsDB* database
  + activity records collected using Integration API—*Netwrix_Auditor_API* database
  + internal event records—*Netwrix_Auditor_EventLog* database
  + data collected by Netwrix Auditor self-audit—*Netwrix_Self_Audit* database
  + data needed for overview reports generation—*Netwrix_OverviewReportsDB*
* To store data from the data sources included in the monitoring plan, dedicated Audit databases are created and named by user (default name format is *Netwrix_Auditor_\*)

The following capacity metrics are displayed for each database:

* **State**—database state summary
* **Size**—current database size (logs are not included)
* **Activity records**—number of the activity records stored in the database at the moment

After you expand the database node, the detailed database properties will be shown:

[![](../static/img/Auditor/Images/Auditor/Health/DBStatistics_thumb_0_0.png)](../../../../Resources/Images/Auditor/Health/DBStatistics.png)

These properties are as follows:

| Property | Possible Values | Description |
| --- | --- | --- |
| Size limit | *\* | For SQL Server Express Edition–shows database size limitations |
| Unlimited |  |
| State description | OK | Database is operating properly. |
| Capacity error | Database is running low on disk space.  -OR-  Size limit for SQL Server Express Edition will be reached soon (threshold is 500 MB, i.e. 5% of 10 GB limit remaining). |
| Failed to store data | Failed to store data to the database due to some issues. |
| Unavailable | Failed to connect to the database. |
| Upgrade in progress | Database is being upgraded. |
| Monitoring plans | *\* | All monitoring plans for which this database is a target.  Usually it is recommended to configure a dedicated database for each plan. |

You can use the Search field, or apply a filter to display the information you need. For example, in the Apply Filters dialog you can select the Show only plans with issues to display only the monitoring plans that require attention and corrective actions.

This information will help you to troubleshoot the product operation, detect and eliminate the root cause of the monitoring errors, providing for auditing continuity and compliance.