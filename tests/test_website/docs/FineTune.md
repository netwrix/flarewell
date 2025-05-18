---
title: "Fine-Tune Your Plan and Edit Settings"
sidebar_position: 879
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

# Fine-Tune Your Plan and Edit Settings

At any time, you can review your plan settings and fine-tune Audit Database, notification and data collection settings.

To modify most plan settings, you must be assigned the Global administrator role in the product or the Configurator role on the plan. The Global reviewer or this plan's Reviewer can modify Activity Summary recipients. See the [Role-Based Access and Delegation](Delegation.htm "Role-Based Access and Delegation") topic for additional information.

Follow the steps to edit your plan settings:

**Step 1 –** Select a plan in the All Monitoring Plans list and click Edit.

**Step 2 –** In the right pane, select Edit settings.

**Step 3 –** In the Plan Settings page, review the tabs and modify the settings.

| Option | Description |
| --- | --- |
| General | |
| Name  Description | Update a plan name or its description. |
| Data Collection | |
| Specify the account for collecting data   * Not specified * User/Password * gMSA | Specify a new user name and a password for the account that Auditor  will use to collect data.  Make sure the account has sufficient permissions to collect data. See the [Data Collecting Account](DataAccounts.htm "Data Collecting Account") topic for additional information about the rights and permissions, and instructions on how to configure them. |
| Audit Database | |
| Disable security intelligence and make data available only in activity summaries | Keep this checkbox cleared if you want Auditor to write data to the Audit Database. |
| Use default SQL Server settings | Select this checkbox to write data to a SQL Server instance with connection parameters as shown in **Settings** \> **Audit Database**. See the [Audit Database](../Settings/AuditDatabase.htm "Audit Database") topic for additional information. |
| Specify custom connection parameters | Specify this option to use non-default settings (e.g., use a different authentication method or user).  Make sure to store data on the same SQL Server instance. Otherwise some data may become unavailable for search and reporting. |
| Notifications | |
| Specify Activity Summary delivery schedule | Configure how often you want to receive an Activity Summary. By default, it is delivered once a day, at 3 AM. You can specify custom delivery time and frequency (e.g., every 6 hours starting 12 AM — at 12 AM, 6 AM, 12 PM, 6 PM). |
| Customize notifications | By default, Activity Summary lists changes and activity in email body. For most data sources, if an Activity Summaries contains more than 1,000 activity records, these records are sent as a CSV attachment, bigger attachments are compressed in ZIP files.   * Attach Activity Summary as a CSV file — You can configure Auditor to always send emails with attachments instead of listing activity and changes in email body. * Compress attachment before sending — You can configure Auditor to always compress attachments in a ZIP file, irrespective of its size and number of activity records. |
| Specify the recipients who will receive daily activity summaries | Modify a list of users who will receive daily activity summaries. Click Add Recipient and provide email address. |