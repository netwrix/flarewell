---
sidebar_position: 21
title: Data Collection & Automation Prerequisites
---

# Data Collection & Automation Prerequisites

Resource Reviews have the following prerequisites:

* [Data Collection Prerequisites](#Data "Data Collection Prerequisites")
* [Automation Prerequisites](#Automati "Automation Prerequisites")

  * [Sensitive Data Review Automation](#Sensitiv "Sensitive Data Review Automation")

## Data Collection Prerequisites

### File System

The following prerequisites are required for reviews of file system data.

Sensitive Data Reviews Requirement

Sensitive Data reviews of file system data requires the following setting be configured in the **FileSystem** > **0.Collection** Job Group in Netwrix Access Analyzer (formerly Enterprise Auditor):

* In the 1-FSAA System Scans Job, configure the Query by selecting the **Scan file-level details** checkbox on the File Details tab on the Default Scoping Options page of the File System Access Auditor Data Collector Wizard.

View Sensitive Content within Reviews Requirement

In order to view the potentially sensitive data during a review, the following setting must also be configured in the **FileSystem** > **0.Collection** Job Group in Netwrix Access Analyzer (formerly Enterprise Auditor):

* In the 1-SEEK System Scans Job, configure the Query by selecting the **Store discovered sensitive data** checkbox on the -Sensitive Data Settings page of the File System Access Auditor Data Collector Wizard.

### SharePoint

The following prerequisites are required for reviews of SharePoint data.

View Sensitive Content within Reviews Requirement

In order to view the potentially sensitive data during a review, the following setting must be configured in the **SharePoint** > **0.Collection** Job Group:

* In the 1-SPSEEK System Scans Job, configure the Query by selecting the **Store discovered sensitive data** checkbox on the DLP Audit Settings page of the SharePoint Access Auditor Data Collector Wizard.

False Positive Sensitive Data

Files that match multiple sensitive data criteria display in every sensitive data review with a matched criteria selected. Files that have been identified as false positives for sensitive content can be flagged either through a resource review or through the **Settings** > **Sensitive Data** node of the Netwrix Access Analyzer (formerly Enterprise Auditor) Console. This removes the file from reports on sensitive data until it has been un-flagged or the file has been modified and rescanned.

**NOTE:** A false positive is a file which matches the sensitive data criteria but does not contain actual sensitive data.

## Automation Prerequisites

When the Access Information Center has been configured to commit Active Directory group membership changes, the Review Administrator approval process will automatically commit approved changes recommended by owners during the review. Each type of review has additional requirements for automation of approved changes.

* Access review — The resource must have an assigned Access Group for the access-level being modified (Read, Modify, or Full Control), and these groups must be in an OU for groups to be managed through the Access Information Center
* Membership review — The group must be in an OU for groups to be managed through the Access Information Center
* Permissions review — The resource must have an assigned Access Group for the access-level being modified (Read, Modify, or Full Control)
* Sensitive Data review — There are no additional prerequisites

  **CAUTION:** Of the three possible actions of Keep, Remove, and Not Sensitive for a Sensitive Data review, the Remove action cannot be automated through the Access Information Center. It must be manually done outside of the application. See the [Sensitive Data Review Automation](#Sensitiv "Sensitive Data Review Automation") topic for additional information.

See the [Access Groups](../ResourceOwners/AccessGroups "Access Groups") topic for additional information.

### Sensitive Data Review Automation

When approving changes in a Sensitive Data review, only Not Sensitive (flag as False Positive) requests can be automatically committed.

Removing a file from a resource cannot be done through the Access Information Center.

Approving a Keep request has no action associated to it. The file does contain sensitive data and is to remain where it is.

Approving a Not Sensitive request to flag a file as a False Positive means the file is removed from Access Information Center and Netwrix Access Analyzer (formerly Enterprise Auditor) reports, which identify it as containing sensitive data matching that specific criteria. However, if the file matches multiple sensitive data criteria, the file still displays in reports and reviews for the other criteria. The file is added to the false positives list in the Netwrix Access Analyzer (formerly Enterprise Auditor) **Settings** > **Sensitive Data** node for that specific criteria. If the file is modified after being flagged, it may reappear in sensitive data reports and reviews if matches to the criteria were found on subsequent data collection scans.