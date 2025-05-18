---
title: "Data Discovery and Classification Reports"
sidebar_position: 920
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

# Data Discovery and Classification Reports

Follow the steps to review Data Discovery and Classification reports:

**Step 1 –** Navigate to **Reports** \> **Data Discovery and Classification** and select a report you are interested in.

**Step 2 –** Click View.

Data Discovery and Classification reports grouped by data sources.

The table below lists the reports available for Data Discovery and Classification:

| Report | Description |
| --- | --- |
| File Servers | |
| Activity reports | |
| Activity Related to Sensitive Files and Folders | This report lists all access attempts to files and folders that contain certain categories of sensitive data at the moment. |
| State-in-time reports | |
| Most Accessible Sensitive Files and Folders | This report shows the number of users that effectively have access to sensitive files or folders, sorted in descending order. Use this report to identify data at high risk and plan for corrective actions accordingly. |
| Overexposed Files and Folders | This report shows sensitive files and folders accessible by the specified users or groups, based on the combination of folder and share permissions. Use this report to identify data at high risk and plan for corrective actions accordingly. |
| Sensitive Files and Folders by Owner | This report shows ownership of files and folders that are stored in the specified file share and contain selected categories of sensitive data. Use this report to determine the owners of particular sensitive data. |
| Files and Folders Categories by Object | This report shows files and folders that contain specific categories of sensitive data. Use this report to see whether a specific file or folder contains sensitive data. |
| Sensitive Files Count by Source | This report shows the number of files that contain specific categories of sensitive data. Use this report to estimate amount of your sensitive data in each category, plan for data protection measures and control their implementation. |
| Sensitive File and Folder Permissions Details | This report shows permissions granted on files and folders that contain certain categories of sensitive data. Use this report to see who has access to a particular file or folder, via either group membership or direct assignment. Reveal sensitive content that has permissions different from the parent folder. |
| SharePoint | |
| Activity reports | |
| Activity Related to Sensitive Data Objects | This report shows changes and read operations on SharePoint sites and documents that contain sensitive information. Use this report to detect suspicious activity around your sensitive data. |
| State-in-time reports | |
| Sensitive Data Objects by Site Collection | For each SharePoint site collection listed, this report shows the categories of sensitive data stored there and the number of documents in each category. Use this report to reveal the number of sensitive files stored in your SharePoint site collections. |
| Sensitive Data Objects | For each site collection listed, this report shows the SharePoint objects (sites, lists and documents) that have been classified as containing sensitive information. Use this report to plan and control data protection measures for sensitive information stored on your SharePoint. |
| Sensitive Data Object Permissions | For each SharePoint object (site, list or document) listed, this report shows the user accounts that have access to this object, their effective permissions and how those permissions were granted (for example, permissions can be granted directly, via group membership or using SharePoint policy). Use this report to control access to SharePoint objects that contain sensitive data. |
| Overexposed Sensitive Data Objects | For each user account listed, this report shows the SharePoint objects (sites, lists and documents) containing sensitive data that the user can access based on their effective permissions. Use this report to identify overexposed data and plan measures to mitigate your risk. |
| Most Exposed Sensitive Data Objects | Lists the SharePoint objects (sites, lists and documents) containing sensitive data that can be accessed by the most users (or even Everyone), based on effective permissions. Use this report to identify data at high risk and plan corrective actions. |

## Requirements for Data Discovery and Classification Reports

The table below contains requirements to run Data Discovery and Classification reports. These are reports that help you to reduce the risk of data leaks and non-compliance by ensuring that all sensitive data resides in safe locations, that it isn't overexposed and that user activity around it is in line with security policies.

Applicable for:

* File Servers
* SharePoint
* SharePoint Online

| Report | Requirement |
| --- | --- |
| File Servers | |
| Activity Related to Sensitive Files and Folders | * Monitoring plan for File Server data source with activity audit enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| File and Folder Categories by Object | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Most Accessible Sensitive Files and Folders | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Overexposed Files and Folders | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor;  * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match);  * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive File and Folder Permissions Details | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive Files and Folders by Owner | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive Files and Folders by Source | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| SharePoint | |
| Activity Related to Sensitive Data Objects | * Monitoring plan for SharePoint data source with activity audit enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Overexposed Sensitive Data Objects | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive Data Object Permissions | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive Data Objects by Site Collection | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |
| Sensitive Data Objects | * Monitoring plan for File Server data source with 'Collect data for State-In-Time reports' feature enabled in Netwrix Auditor; * Netwrix Data Classification instance configured to crawl from the same source (naming must exactly match); * Sensitive Data Discovery correctly configured on the Netwrix Auditor Server. |

## Make Reports Handy

In addition to reviewing  reports, you can customize them with filters and create report subscriptions. Review the following for additional information:

* [View Reports](../View.htm "View Reports")
* [Create Subscriptions](../../Subscriptions/Create.htm "Create Subscriptions")