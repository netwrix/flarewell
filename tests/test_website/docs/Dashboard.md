---
title: "IT Risk Assessment Dashboard"
sidebar_position: 901
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

# IT Risk Assessment Dashboard

To access the Risk Assessment dashboard, click the corresponding tile in the main window.

You can add any elements (a dashboard, report, alert, risk, etc.) to the Auditor Home screen to access them instantly. See the [Navigation](../Navigation/Overview.htm "Navigation") and [Customize Home Screen](../Navigation/CustomizeHome.htm "Customize Home screen") topics for additional information.

The IT risks are grouped into the following categories:

* Users and Computers
* Permissions
* Data
* Infrastructure

Within each category there are several key metrics identified by Netwrix industry experts who also suggested formulas for calculating metrics values. Risks are assessed against these metrics and displayed with the color indicators in accordance with the level:

* High — red
* Medium — yellow
* Low — green

[![](../static/img/Auditor/Images/Auditor/RiskAssessment/Dashboard_thumb_0_0.png)](../../../Resources/Images/Auditor/RiskAssessment/Dashboard.png)

After reviewing general risks assessment results in each category, you can drill-down to details covered in the underlying report. To do so, double-click the selected metric or use the View Report button.

## Customizing Metrics for Your Organization

Default threshold values for risk levels are set in accordance with recommendations of Netwrixindustry experts, as described in the [How Risk Levels Are Estimated](Levels.htm "How Risk Levels Are Estimated")  topic. They can be, however, easily customized to reflect your organization's internal security policies and standards. Follow the steps to customize the metrics.

**Step 1 –** In the dashboard pane, select the metric you need and in the **Actions** section on the right click Modify thresholds.

**Step 2 –** In the displayed dialog, specify new threshold values for risk levels.

**Step 3 –** Click OK to save the settings and close the dialog.

[![](../static/img/Auditor/Images/Auditor/RiskAssessment/Modify_thresholds_thumb_0_0.png)](../../../Resources/Images/Auditor/RiskAssessment/Modify_thresholds.png)

Also, for several metrics the Customize risk indicators command is available.

| For metric... | Use Customize risk indicators command to... |
| --- | --- |
| File and folder names containing sensitive data | Edit the list of words you consider to be indicators of sensitive content if detected in the file or folder name. |
| Potentially harmful files on file shares | Edit the list of extensions you consider to be indicators of potentially harmful files detected in the file share. |
| Servers with inappropriate operating systems | Edit the whitelist of permitted OS versions. Any other OS version will be considered a risk factor. |
| Servers with unauthorized antivirus software | Edit the whitelist of permitted antivirus tools. Any other antivirus will be considered a risk factor. |
| Administrative group membership sprawl | Edit the whitelist of permitted accounts that can be the members of local administrative groups. Any other account will be considered a risk factor. |

New settings will be applied/risk level thresholds will be refreshed after the next data collection session.

## Delivering Assessment Results as a File

You can create a subscription to periodically receive IT risk assessment results by email or using a file share. For that, in the dashboard window click Subscribe and configure the necessary settings. See the [Create Subscriptions](../Subscriptions/Create.htm "Create Subscriptions") topic for additional information.

You can also save current results to a PDF file by using the Export button in the dashboard window.