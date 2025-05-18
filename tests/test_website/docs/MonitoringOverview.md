---
title: "Monitoring Overview"
sidebar_position: 962
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

# Monitoring Overview

Aggregated statistics on the monitoring plans is provided in the Monitoring overview widget. It displays current statuses of all monitoring plans:

* Ready (green indicator)—The monitoring plans (one or several) successfully processed the data sources with all their items and are ready for the next run.
* Pay attention (yellow indicator)—The monitoring plans (one or several) require your attention, as some items were not processed completely but only partially. This status applies to the monitoring plans targeted at Logon Activity and Windows File Server. See the table below for details.
* Take action (red indicator)—Any data source or item in the monitoring plan (one or several) was processed with errors.

After you click View details, the Monitoring Overview window will be displayed.

[![](../static/img/Auditor/Images/Auditor/Health/MonitoringOverview_thumb_0_0.png)](../../../../Resources/Images/Auditor/Health/MonitoringOverview.png)

It provides the hierarchical list of monitoring plans, processed data sources and corresponding items with their current status and date/time of the last data processing session. For data sources and items their current status is depicted as follows:

| Entity | Status | Description |
| --- | --- | --- |
| Data source | Disabled | A data source can be disabled manually via its settings (by switching Monitor this data source and collect activity data to OFF), or automatically, if the license is not valid any more (for example, the count of licensed objects was exceeded, or the trial period has expired). |
| Empty | No items have been added to this data source yet. |
| Enabled | Monitor this data source and collect activity data is set to ON in the data source settings. |
| Not available | The monitoring plan is corrupted and cannot process its data sources, so it is recommended to remove it and create anew. |
| Not responding | Data collector for this data source is not responding. The underlying items will not be displayed for such data source. |
| Working | The data source is being processed at the moment. |
| (not displayed) | The data source status is unknown. |
| Item | Pay attention | The item was processed with some issues (non-critical). This status applies to the monitoring plans targeted at Logon Activity and Windows File Server. It means that data collection from at least one entity completed with errors.  For example, a MyFileServer item included in the File Server monitoring plan contains all CIFS shares hosted on the MyFileServer computer.  If any of these shares was processed with errors while others were processed successfully, the processing of the whole MyFileServer item will be considered partially completed, and the monitoring plan will have a yellow indicator, requiring your attention.  Click the Details link to examine the product log. |
| Ready | The item was processed successfully and is ready for the next run of data collection. |
| Take action | Critical error(s) occurred while processing this item.  Click the Details link to examine the product log. |
| Working | The item is being processed at the moment. |

You can use the Search field, or apply a filter to display the information you need. For example, in the Apply Filters dialog you can select the Show only plans with issues to display only the monitoring plans that require attention and corrective actions.

This information will help you to troubleshoot the product operation, detect and eliminate the root cause of the monitoring errors, providing for auditing continuity and compliance.