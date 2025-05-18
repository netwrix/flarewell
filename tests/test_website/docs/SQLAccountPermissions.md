---
title: "Account Permissions in SQL
 Server"
sidebar_position: 928
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

# Account Permissions in SQL Server

Details the effective permissions that the specified account has on the SQL Server objects of the selected type. Use this report to review the permissions granted to users through your SQL Server objects.

[![](../static/img/Auditor/Images/Auditor/Report/SQLServer/AccountPermissionsSQLServer_thumb_0_0.png)](../../../../../Resources/Images/Auditor/Report/SQLServer/AccountPermissionsSQLServer.png)

## Reported data

The report has a summary section with general information on the selected account, and the details section presented in the table format.

The summary section shows:

* **User account**— name or SID of the account
* **Account type** —possible values:
  + Windows Account
  + Login SQL Authentication
  + DB SQL User with password
* **Job title** —reported for Active Directory users as set in their corresponding attribute. If not set, *\* is reported.
* **Total objects count** — total number of objects that this account has access to.

The detailed information under summary includes:

* **Object path** — monitored object path as formatted by Netwrix Auditor in the activity records (see '*What*' field in the reports, search results and activity summaries). For example, if reporting on the database hosted on selected SQL Server, the path will be as follows: *Databases\database_name*.
* **Object type** — monitored object type; for the full list of supported object types, refer to [SQL Server](../../../../Configuration/SQLServer/Overview.htm "SQL Server") topic.
* **Means granted** —how access permissions were granted to this account, e.g., *Direct permissions* or *Server role permissions*.
* **Effective grant** —the effective set of permissions granted to this account on the selected object.

## Filters

This report has the following filters:

* **Monitoring plan** — name of the monitoring plan set to collect data from the SQL Server you need.
* **Time zone** — time zone where Netwrix Auditor server is located, for example, UTC-08:00. This value is filled in automatically.
* **Snapshot date** —select the date of state-in-time snapshot you want to report on. By default, the report includes data obtained during the latest data collection session (*Current Session*). To report on other snapshots, make sure they are available through import. For details, see **Manage historical snapshots** option description in [SQL Server](../../../MonitoringPlans/SQLServer/Overview.htm "SQL Server Plans")
* **Item**— name of the SQL Server instance monitored with selected monitoring plan.
* **Object path** — path to the monitored object, as formatted by Netwrix Auditor in the activity records (see '*What*' field in the reports, search results and activity summaries). Wildcard (\*) is supported. For example, to report on the database hosted on selected SQL Server, specify the path as follows: *Databases\database_name*.
* **Object type**— type of the monitored object that provided data for this report. Possible values: *Database*, *Server Instance*.
* **Permissions** —access permissions whose assignment you want to be reported for selected account.
* **Means granted** —how access permissions were granted to this account. You can select *Directly*, *Inherited*, or both (default setting).
* **Account type** —possible values: *Windows Account*, *Login SQL Authentication*, *DB SQL User with password*.
* **User account**—name or SID of the account whose permission assignments are reported.

## Considerations and limitations

* Reporting for case-sensitive SQL Servers and databases is not supported.
* Permissions for INFORMATION_SCHEMA granted via *master db* will not be reported.
* The report will not show the RESTORE capability for the database owner.

* When calculating effective rights and permissions, the following will not be considered:

  + Ownership chaining
  + Cross DB ownership chaining
  + Trustworthy database
  + SQL Server agent fixed database roles

## Related reports

* Clicking a Object permissions link opens the [Object Permissions in SQL
  Server](SQLObjectPermissions.htm "Object Permissions in SQL Server") report.
* Clicking a Means granted link opens the **[SQL Server Means Granted](SQLMeansGranted.htm "SQL Server Means Granted")** report.

## Usage example

Database administrators in the *Corp* organization need to discover what kind of permissions a certain user has on the **SQLSrv01\SQLServer2016** instance. This instance is included in the monitoring plan named *SQL Servers Monitoring*.

To examine the relevant data, they generated the **Account Permissions in SQL Server** report with the filters set as follows:

* **Monitoring plan:***SQL Servers Monitoring*
* **Snapshot date:***Current Session*
* **Item:***SQLSrv01\SQLServer2016*
* **User account:** *Corp\Ian.Harris*

The report revealed that this user has access permissions for the master database. To discover how they were granted, click the link in the **Means granted** field.