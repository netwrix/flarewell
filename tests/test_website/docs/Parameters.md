---
title: "Define Parameters"
sidebar_position: 849
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

# Define Parameters

Before running or scheduling the add-on, you must define connection details: Auditor Server host, user credentials, etc. Most parameters are optional, the script uses the default values unless parameters are explicitly defined. You can skip or define parameters depending on your execution scenario and security policies.
See the [Choose Appropriate Execution Scenario](Deployment.htm "Choose Appropriate Execution Scenario") topic for additional information.

| Parameter | Default value | Description |
| --- | --- | --- |
| **Connection to Netwrix Auditor** | | |
| NetwrixAuditorHost | localhost:9699 | Assumes that the add-on runs on the computer hosting the Auditor Server and uses default port 9699.  If you want to run the add-on on another machine, provide a name of the computer where Auditor Server resides (e.g., 172.28.6.15, EnterpriseNAServer, WKS.enterprise.local).  To specify a non-default port, provide a server name followed by the port number (e.g., WKS.enterprise.local:9999). |
| NetwrixAuditorUserName | Current user credentials | Unless specified, the add-on runs with the current user credentials.  If you want the add-on to use another account to connect to Auditor Server, specify the account name in the *DOMAIN\username* format.  The account must be assigned the Global reviewer role in Auditor or be a member of the Netwrix Auditor **Client Users** group on the computer hosting Auditor Server. |
| NetwrixAuditorPassword | Current user credentials | Unless specified, the script runs with the current user credentials. Provide a different password if necessary. |

## In-Script Parameters

You may also need to modify the parameters that define how EventIDs should be generated for exported events, though their default values address most popular usage scenarios. In-script parameters are listed in the table below. To modify them, open the script for edit and enter the values you need.

Once set, these parameter values must stay unchanged until the last run of the script — otherwise dynamically calculated EventIDs will be modified and applied incorrectly.

| Parameter | Default value | Description |
| --- | --- | --- |
| **EventID generation** | | |
| GenerateEventId | True | Defines whether to generated unique EventIDs. Possible parameter values:   * True — generate unique EventIDs using Activity Record fields * False — do not generate a unique ID, set EventID=0 for all cases   EventID is generated through CRC32 calculation that involves the following Activity Record field values:   * ObjectType * Action * DataSource (optional, see below for details)   Only the lowest 16 bits of the calculation result are used.  See the [Activity Records](../../API/PostData/ActivityRecords.htm "Activity Records") topic for additional information. |
| IncludeDataSourceToMakeEventId\* | True | Defines whether the DataSource field of Activity Record should be used in the EventID calculation. This parameter is applied only if GenerateEventId is set to *TRUE*. |
| SetDataSourceAsEventCategory | True | Defines whether to fill in Event Category event field with a numeric value derived from the DataSource field of Activity Record.  Possible parameter values:   * True — generate a numeric value for Event Category using Activity Record field * False — do not generate a numeric value, set Event Category=1 for all cases   The Event Category field value is generated through CRC32 calculation that involves the DataSource field of Activity Record.  Only the lowest 9 bits of the calculation result are used. |
| SetDataSourceAsEventSource | False | Defines whether to fill in the Event Source event field with the value from the DataSource field of Activity Record. Possible parameter values:   * True — fill in the Event Source with the value from DataSource field of Activity Record, adding the prefix defined by $EventSourcePrefix. Default prefix is *NA*, for example:*NA Windows Server* * False — set Event Source to *Netwrix_Auditor_Integration_API* for all cases   If the script cannot fill in the Event Source for some DataSource, the default value *Netwrix_Auditor_Integration_API* will be used.  If the event source for particular DataSource does not exist in the Netwrix_Auditor_Integration event log, elevated privileges are required for add-on execution. |

\* When configuring the **IncludeDataSourceToMakeEventId** parameter, consider that the *Object Type - Action* pair may be identical for several data sources (e.g., Object='User' and Action='Added'); thus, excluding DataSource from calculation may lead to the same EventID (duplicates). See the [Run the Add-On with PowerShell](../IBMQRadar/PowerShell.htm "Run the Add-On with PowerShell") topic for additional information about duplicates.\*