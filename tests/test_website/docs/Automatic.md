---
title: "Active Directory: Automatic Configuration"
sidebar_position: 990
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

# Active Directory: Automatic Configuration

This is a recommended method of applying Active Directory audit settings required by Auditor to monitor your AD domain. With this approach, the program will check your current audit settings at each data collection session and adjust them if necessary.

To adjust audit settings automatically, do any of the following:

* When creating a new monitoring plan, at the first step of the wizard select the **Adjust audit settings automatically** option. See the [Create a New Monitoring Plan](../../Admin/MonitoringPlans/Create.htm "Settings for Data Collection") topic for additional information.

[![](../static/img/Auditor/Images/Auditor/MonitoringPlans/MP_wizard_step1_AD_thumb_0_0.png)](../../../Resources/Images/Auditor/MonitoringPlans/MP_wizard_step1_AD.png)

* For the existing monitoring plan, modify data collection settings for Active Directory data source, selecting **Adjust audit settings automatically** option.   
  See the [Manage Data Sources](../../Admin/MonitoringPlans/DataSource.htm "Manage Data Sources") and [Active Directory](../../Admin/MonitoringPlans/ActiveDirectory/Overview.htm "Active Directory Plans") topics for additional information.
* For both new and existing monitoring plans, you can click **Launch Audit Configuration Assistant** (in the wizard step or in the plan settings, respectively) to launch a special tool that can detect current infrastructure settings and adjust them as needed for monitoring. See the [Audit Configuration Assistant](../../Tools/AuditConfigurationAssistant.htm "Audit Configuration Assistant") topic for additional information.

If any conflicts are detected with your current audit settings, automatic audit configuration will not be performed. For a full list of audit settings required for Netwrix Auditor to collect comprehensive audit data and instructions on how to configure them, refer to the [Active Directory](Overview.htm "Active Directory") topic.

See also:

* [Active Directory](Overview.htm "Active Directory")
* [Audit Configuration Assistant](../../Tools/AuditConfigurationAssistant.htm "Audit Configuration Assistant")
* [Active Directory: Manual Configuration](Manual.htm "Active Directory: Manual Configuration")