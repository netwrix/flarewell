---
title: "Create Subscriptions"
sidebar_position: 903
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

# Create Subscriptions

To create new subscriptions and manage existing subscriptions, you must be assigned the Global administrator or Global reviewer role in the product. See the [Role-Based Access and Delegation](../MonitoringPlans/Delegation.htm "Role-Based Access and Delegation") topic for additional information.

1. Do one of the following depending on subscription type:

   | To... | Do... |
   | --- | --- |
   | Subscribe to a report | On the main Auditor page, navigate to Reports. Specify the report that you want to subscribe to and click Subscribe. |
   | Subscribe to Behavior anomalies dashboard report | On the main Auditor page, navigate to Behavior anomalies, then in the dashboard window click Subscribe. |
   | Subscribe to search | 1. Navigate to Search and set appropriate search criteria. See the [Use Filters in Simple Mode](../Search/FilterSimple.htm "Use Filters in Simple Mode") topic for additional information. Click Search. 2. Navigate to Tools and select Subscribe. |
   | Subscribe to risk assessment overview | On the main Auditor page, navigate to Risk assessment and in the dashboard window click Subscribe. |
2. On the Add Subscription page, complete the following fields:

   | Option | Description |
   | --- | --- |
   | General | |
   | Subscription name | Enter the name for the subscription. |
   | Report name  *OR*  Email subject | For report subscription—You cannot edit report name.  For subscription to search and risk assessment overview—Specify email subject to identify subscription emails from Auditor. For example, "*Successful read attempts on important file shares*". |
   | Send empty subscriptions when no activity occurred  Available for report and search subscriptions only. | Slide the switch to Yes if you want to receive a report even if no changes occurred. |
   | Specify delivery options | * File format—Configure reports to be delivered as the pdf or csv files for search subscriptions; and pdf, docx, csv or xls files for report subscriptions. Available for report and search subscriptions only.  * File delivery—Select delivery method:    + Attach to email—Select this option to receive data as email attachments.  The maximum size of the attachment file is 50 MB. Attachments larger than 50MB will be uploaded to *\\\\Netwrix_Auditor_Subscriptions$\LostAndFound\* folder on Netwrix Auditor server. They will be available for 7 days. Check the subscription email to get the files.   + Upload to a file share—Select this option to save data on the selected file share. Click Browse to select a folder on the computer that hosts Auditor Server or specify a UNC path to a shared network resource.  Make sure that the recipients have sufficient rights to access it and the Long-Term Archive service account has sufficient rights to upload reports. See the [File-Based Repository for Long-Term Archive](../../Requirements/LongTermArchive.htm "File-Based Repository for Long-Term Archive") topic for additional information. **NOTE:** Make sure that the AD Computer account for the Auditor host server also has read access on the file share where the Subscriptions are being uploaded. |
   | Other tabs | |
   | Recipients | Shows the number of recipients selected and allows specifying emails where reports are to be sent.  Expand the Recipients list and click Add to add more recipients. |
   | Schedule | Allows specifying report delivery schedule (daily, certain days of week, a certain day of a certain month).  By default, risk assessment overview and search subscription delivery is scheduled to 7.00 am daily, report subscription delivery - to 8.00 am daily. |
   | Filters | * For report subscription—Specify the report filters, which vary depending on the selected report. * For subscription to risk assessment overview—Select one or several monitoring plans and risk categories whose data you want to be included. By default, you will receive data on all risk categories, provided by all monitoring plans configured for risk assessment. * For search subscription—Specify filters in the same way as for search. See the [Use Filters in Advanced Mode](../Search/FilterAdvanced.htm "Use Filters in Advanced Mode") topic for additional information.  For search subscription, you can also select a parameter to sort actions by and the sorting order. |
   | History  For search and risk assessment subscriptions only. | * Contains subscription generation details (intervals, status, last run time, start type). If the subscription failed, expand its details to understand and resolve error, then click the Try again link. * Allows for on-demand subscription delivery—for that, click Run Now. On successful subscription generation you will receive the results that match your criteria for the scheduled period. |