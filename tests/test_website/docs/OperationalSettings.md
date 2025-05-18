---
title: "Operational Settings"
sidebar_position: 851
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

# Operational Settings

This section describes how to configure settings of the main add-on component, Netwrix Auditor **ConnectWise Manage Integration Service**, required for its operation, including connection to Auditor Server, activity records processing, queuing and forwarding, ticket creation, and so on.

For that, follow the steps:

**Step 1 –** Navigate to the add-on folder and select ITSMSettings.xml.

**Step 2 –** Define operational parameters such as Auditor connection settings, the number of tickets the service can create per hour, ability to reopen closed tickets, etc. For most parameters, default values are provided. You can adjust them depending on your execution scenario and security policies. Use the following format: `value`.

| Parameter | Default value | Description |
| --- | --- | --- |
| NetwrixAuditorHost | https://localhost:9699 | The add-on runs on the computer where Auditor Server resides and uses the default Integration API port (TCP port **9699**). To specify a non-default port, provide a new port number (e.g., *`https://localhost:8788*`).  The add-on must always run locally, on the computer where Auditor Server resides. |
| NetwrixAuditorUserName | — | Unless specified, the Netwrix Auditor **ConnectWise Manage Integration Service** runs under the LocalSystem account.  If you want this service to use another account to connect to Auditor Server, specify the account name in the *DOMAIN\username* format in this parameter value.  The user account for running the service and connecting to Auditor Server must be granted the Global administrator role in Auditor or be a member of the Netwrix Auditor **Administrators** group. It must also have sufficient permissions to create files on the local computer. |
| NetwrixAuditorPassword | — | Provide a password for the account. Unless an account is specified, the service runs under the LocalSystem account and does not require a password. |
| TicketFloodLimit | 10 | Specify the maximum number of standalone tickets the service can create during TicketFloodInterval.  If a ticket flood limit is reached, the service writes all new alerts into a single ticket. |
| TicketFloodInterval | 3600 | Specify the time period, in seconds. During this time period, the service can create as many tickets as specified in TicketFloodLimit. The default value is 3600 seconds, i.e., 1 hour. |
| ConsolidationInterval | 900 | Specify the time period, in seconds. During this time period, the service does not process similar alerts as they happen but consolidates them before updating open tickets. The default values is 900 seconds, i.e., 15 minutes.  This option works in combination with UpdateTicketOnRepetitiveAlertsand is helpful if you want to reduce the number of ticket updates on ConnectWise Manage side. I.e., this option defines the maximum delay for processing alerts and updating existing tickets. Tickets for new alert types are created immediately.  For example, a new alert is triggered—the service opens a new ticket. The alert keeps firing 20 times more within 10 minutes. Instead of updating the ticket every time, the service consolidates alerts for 15 minutes, and then updates a ticket just once with all collected data. |
| CheckAlertQueueInterval | 5 | Internal parameter. Check and process the alert queue every N seconds; in seconds. |
| UpdateTicketOnRepetitiveAlerts | true | Instead of creating a new ticket, update an existing active ticket if a similar alert occurs within UpdateInterval.  To open a new ticket for every alert, set the parameter to *"false"*. |
| ReopenTicketOnRepetitiveAlerts | true | Instead of creating a new ticket, reopen an existing ticket that is in a closed state (be default, closed, canceled, and resolved) if a similar alert occurs within UpdateInterval.  This option works only when UpdateTicketOnRepetitiveAlerts is set to *"true"*.  If you want to reopen closed tickets, you must be granted the right to perform Write operations on inactive tickets. |
| UpdateInterval | 86400 | Specify the time period, in seconds. If a similar alert occurs in less than N seconds, it is treated as a part of an existing ticket. The default value is 86400 seconds, i.e., 24 hours.  If an alerts is triggered after the UpdateInterval is over, a new ticket is created. |
| EnableTicketCorrelation | true | Review history and complement new tickets with information about similar tickets created previously. This information is written to the Description field.  This option is helpful if you want to see if there is any correlation between past tickets (from the last month, by default) and a current ticket. |
| CorrelationInterval | 2592000 | Specify the time period, in seconds. During this time period, the service treats similar tickets as related and complements a new ticket with data from a previous ticket. The default value is 2592000 seconds, i.e., 1 month.  Information on alerts that are older than 1 month is removed from internal service storage. |
| ProcessActivityRecord QueueInterval | 5 | Internal parameter. Process activity record queue every N seconds; in seconds. |
| DisplayOnlyFirstActivityRecord | true | Add only the first activity record in the work notes, activity records that update this ticket will be added as attachments to this ticket. If false, all activity records will be displayed in the ticket work notes. |
| ActivityRecordRequestsRetention | | |
| RequestLimit | 5000 | Internal parameter. The maximum number of activity record requests the service can store in its internal memory. Once the limit is reached, the service clears activity record requests starting with older ones. |
| RequestLimitInterval | 604800 | Internal parameter. The service can store the activity record requests not older than N seconds; in seconds. Older activity record requests are cleared. |
| ActivityRecordWebRequests | | |
| RequestLimit | 200 | Internal parameter. The maximum number of activity records the service can retrieve in a single request. |
| RequestTimeout | 180 | Internal parameter. By default, 3 minutes. Defines the connection timeout. |
| TicketRequestsRetention | | |
| RequestLimit | 300000 | Internal parameter. The maximum number of ticket requests the service can store in its internal memory. Once the limit is reached, the service clears ticket requests starting with older ones. |
| RequestLimitInterval | 604800 | Internal parameter. The service can store the ticket requests not older than N seconds; in seconds. Older tickets requests are cleared. |

**Step 3 –** Restart the service every time you update ITSMSettings.xml configuration file.