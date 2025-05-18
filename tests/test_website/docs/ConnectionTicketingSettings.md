---
title: "Connection and Ticketing Settings"
sidebar_position: 853
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

# Connection and Ticketing Settings

It is recommended that you use configuration wizard to specify connection and ticketing settings. However, you can adjust them manually, using the information provided in this section.

## Settings for ConnectWise Ticket Creation

Specify how data arriving from Auditor should be used to fill in ConnectWise ticket fields. For that, review `` section of the ConnectWiseSettings.xml file. The parameters inside this section correspond to ConnectWise ticket fields and use the same naming (e.g., priority, urgency).

Each `` includes the `` and `` pair that defines a ConnectWise ticket field and a value that will be assigned to it. For most parameters, default values are provided. Add more ticket parameters or update values if necessary.

|  |  | Description |
| --- | --- | --- |
| Summary | [Netwrix Auditor]  %AlertName% | Instructs the system to fill in the Summary ticket field with the Auditor alert name (e.g., *[Netwrix Auditor] Password Reset)*. |
| InitialDescription | Alert Details:  Who: %Who%  Action: %Action%  Object type: %ObjectType%  What: %What%  When: %When%  Where: %Where%  Workstation: %Workstation%  Details: %Details%    Data source: %DataSource%  Monitoring plan: %MonitoringPlanName%  Item: %Item%  Sent by Netwrix Auditor from %Computer% | Instructs the system to fill in the InitialDescription ticket field with the Auditor activity record data. To read more about activity records, see the [Reference for Creating Activity Records](../../API/ActivityRecordReference.htm "Reference for Creating Activity Records") topic for additional information.  You may need to fill in the internal description intended for use by MSP only (this description will not be visible to managed clients), perform the following steps:  **Step 1 –** Run the configuration wizard (or modify *ConnectWiseSettings.xml*) to specify the settings you need.  **Step 2 –** Then open *ConnectWiseSettings.xml* for edit.  **Step 3 –** Locate the **InitialDescription** parameter and change the Name attribute to *initialInternalAnalysis*. |
| Impact/Urgency | Medium | Instructs the system to set ticket Impact/Urgency to *Medium*. |

## Parameters for Handling Related Tickets

Review the `` section. It shows what information about related tickets will be included in your current ticket. Update the template if necessary.

| CorrelationTicketFormat | Description |
| --- | --- |
| Previous incident for the same alert type:  Id: %id% | The service will automatically substitute parameters from this section with values from a related ticket. |

## Parameters for Reopening Tickets

Review the `` section. It defines the tickets the add-on can reopen automatically.

| Name | Description |
| --- | --- |
| ClosedTicketStates  TicketState | Lists closed ticket statuses.  By default, resolved, closed, and canceled tickets can be reopened.  To specify a new status, provide its ID in the `` tag (e.g., 8 for canceled). |
| NewState | Defines a ticket status once it is reopened. By default, is set to *new*. To specify another status, provide its ID in the `` tag (e.g., *1* for *new*). |

When finished, save your changes to configuration file.

Remember to restart the add-on service every time you update any of configuration files.

## Review Other Parameters

You can update other parameters with your own values if necessary; however, it is recommended that you contact Netwrixbefore modifying this section.

| Name | Description |
| --- | --- |
| IgnoreUploadAttachmentError | Instructs the add on to ignore the attachment upload errors.   * If false, a corresponding error message will be displayed. * If true, the file that failed to upload will be stored to the **MissingAttachments** subfolder in the add-on folder. Error message will not appear on the screen; instead, the following record will be written to the add-on log: *Attached files for ticket id: \{0\} dumped: '\{attachmentPath\}'*   Default parameter value is **true**. |

You can also review the `` section. It shows information related to ConnectWise Manage objects.

Example:

\

\

\company\

\

\

\id\

\

\42 - enter ID of the company-ticket originator

\

\

\

\

\board\

\

\

\id\

\

\1 - enter ID of the service board for the tickets

\

\

\

\

\priority\

\

\

\id\

\

\4\

\

\

\

\

\team\

\

\

\id\

\

\25 - enter ID of the service team responsible for resolution

\

\

\

\