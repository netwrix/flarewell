---
sidebar_position: 107
title: Activity Statistics Report
---

# Activity Statistics Report

The Activity Statistics report for a computer object provides statistical activity event information for the audited computer during the selected date range. This report includes a line graph for Traffic Trend.

![Activity Statistics report](../../../../../../../static/Content/Resources/Images/Access/InformationCenter/ResourceAudit/Computer/ActivityStatistics.png "Activity Statistics report")

This report is comprised of the following columns:

* Collector – Refers to the collection source for the permission (for example, **FileSystem** for the Access Analyzer File System Solution, **SharePoint** for the Access Analyzer SharePoint Solution, and so on)
* Server Name – Name of the file system server or SharePoint farm/instanceS where the activity event occurred
* Path – Location of the resource where the activity event occurred
* Reads – Count of view/read operations on resource
* Writes – Count of edit/modify operations on resource
* Manages – Count of permission change operations on resource
* Deletes – Count of delete operations on resource

The table data grid functions the same way as other table grids. See the [Data Grid Features](../../../General/DataGrid "Data Grid Features") topic for additional information.

There is one line graph at the bottom displaying the Traffic Trend for the audited computer. It provides a visual representation of the number of operations events that occurred by operation type over the selected date range. It indicates what volume of operations occurred per day. Each operation type is provided with a different color, as indicated by the legend. See the [Activity Report Results Pane Features](../Navigate/Overview#Activity "Activity Report Results Pane Features") topic for instructions on filtering the Trend graph.