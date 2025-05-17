---
sidebar_position: 82
title: MySQL Reports Quick Reference Guide
---

# MySQL Reports Quick Reference Guide

The following MySQL reports are available for selections within the Resources pane.

## MySQL Node Report

The following report is available at the MySQL node level:

| Report | Description |
| --- | --- |
| [Sensitive Content Summary Report](SensitiveContentSummary "Sensitive Content Summary Report") | Provides a count of databases where criteria matches were found in the targeted environment. This report includes a Details table. |

## MySQL > Instance Level Reports

The following reports are available at the instance level:

| Report | Description |
| --- | --- |
| [Sensitive Content Details Report](Instance/SensitiveContentDetails "Sensitive Content Details Report") | Provides details of tables where criteria matches were found on the selected instance. This report includes a table with criteria matches visible to Access Information Center users with either Security Team Member or Administrator roles. The Matches table requires the storage of discovered sensitive data within the Access Analyzer database or it will be blank. |
| [Sensitive Content Summary Report](Instance/SensitiveContentSummary "Sensitive Content Summary Report") | Provides a count of tables where criteria matches were found on the selected instance. This report includes a Details table. |

## MySQL > Instance > Databases Node Reports

The following reports are available at the Databases node level:

| Report | Description |
| --- | --- |
| [Permissions Report](DatabaseTables/Permissions "Permissions Report") | Shows the permissions for the trustee on the selected resource. |
| [Sensitive Content Report](DatabaseTables/SensitiveContent "Sensitive Content Report") | Provides a list of paths and a hit count per table where criteria matches were found on the selected resource. This report includes a table with criteria matches visible to Access Information Center users with either Security Team Member or Administrator roles. The Matches table requires the storage of discovered sensitive data within the Access Analyzer database or it will be blank. |

## MySQL > Instance > Database Node > Database and Table Level Reports

The following reports are available at the database and table levels:

| Report | Description |
| --- | --- |
| [Permissions Report](DatabaseTables/Permissions "Permissions Report") | Shows the permissions for the trustee on the selected resource. |
| [Sensitive Content Report](DatabaseTables/SensitiveContent "Sensitive Content Report") | Provides a list of paths and a hit count per table where criteria matches were found on the selected resource. This report includes a table with criteria matches visible to Access Information Center users with either Security Team Member or Administrator roles. The Matches table requires the storage of discovered sensitive data within the Access Analyzer database or it will be blank. |