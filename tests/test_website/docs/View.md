---
title: "View Reports"
sidebar_position: 912
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

# View Reports

To view reports, users need the following:

1. Sufficient access rights in Netwrix Auditor, which are provided through role assignment:

* Users with *Reviewer* role can generate the reports for their delegated scope only, and view them in any Netwrix Auditor client or in a web browser.
* Users with *Global administrator* or *Global reviewer* role can also create subscriptions to reports.

2. The Browser role on the SSRS Report Server. See the [SQL Server Reporting Services](../../Requirements/SQLServerReportingService.htm "Configure SSRS Account") topic for additional information.

To view a report

You can add any elements (a dashboard, report, alert, risk, etc.) to the Auditor Home screen to access them instantly. See the [Navigation](../Navigation/Overview.htm "Navigation") and [Customize Home Screen](../Navigation/CustomizeHome.htm "Customize Home screen") topics for additional information.

1. In Netwrix Auditor Home screen, click ![](../static/img/Auditor/Images/Auditor/HomeScreen/Reports_tile.PNG)on the left, and in the tree on the left select the report you need.

To speed up the process, you can use the **Search** field, entering the keyword to search by.

[![](../static/img/Auditor/Images/Auditor/Report/SearchReports_thumb_0_0.png)](../../../Resources/Images/Auditor/Report/SearchReports.png)

2. Click View button in the right pane.

To learn how to subscribe to a report, see [Create Subscriptions](../Subscriptions/Create.htm "Create Subscriptions").

## Troubleshooting

If no data is displayed in the report, you may need to do the following:

1. Make sure that the Audit Database settings are configured properly in the monitoring plan, and that data is written to databases that reside on the default SQL Server instance. See the [Audit Database](../Settings/AuditDatabase) topic for additional information.
2. For SSRS-based reports - verify that SSRS (SQL Server Reporting Services) settings are configured properly. See the [Audit Database](../Settings/AuditDatabase.htm "Audit Database") topic for additional information.
3. For state-in-time reports - verify that the monitoring plan that provides data for the report has the corresponding option selected. See the [Create a New Monitoring Plan](../MonitoringPlans/Create.htm "Settings for Data Collection") topic for additional information.

## Customize Report with Filters

Report filters allow you to display changes matching certain criteria. For example, you can filter changes by audited domain or object type. Filtering does not delete changes, but modifies the report view allowing you to see changes you are interested in. Filters can be found in the upper part of the Preview Report page.

To apply filters

1. Navigate to Reports and generate a report.
2. Apply required filters to the report and click View Report. For example, you can update report timeframe, change *Who* and *Where* values, apply sorting, etc.

Wildcards are supported. For example, type *%corp\administrator%* in the in the Who domain\user field if you want to view changes made by the corp\administrator user only .

Do not use % in the exclusive filters (e.g., Who (Exclude domain\user)). Otherwise, you will receive an empty report.

*escape_characters* are not supported.

The example below applies to the All Changes by Server report and shows the before and after views of the report. The filters may vary slightly depending on the audited system and report type.

The report without filtering:

![](../static/img/Auditor/Images/Auditor/Report/AllChangesServer.png)

The report below displays changes for all audited systems made by the CORP\Administrator user on the ROOTDC2 domain controller for a month sorted by the action type.

![](../static/img/Auditor/Images/Auditor/Report/AllChangesServerFiltered.png)