---
title: "API Endpoints"
sidebar_position: 696
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

# API Endpoints

| Method | Endpoint | POST Data | Description |
| --- | --- | --- | --- |
| GET | /netwrix/api/v1/activity_records/enum | — | Returns Activity Records.  [Retrieve Activity Records](RetrieveActivityRecords) |
| POST | /netwrix/api/v1/activity_records/enum | [Continuation Mark](PostData/ContinuationMark) | Returns next 1,000 Activity Records.  [Continuation Mark](PostData/ContinuationMark) |
| POST | /netwrix/api/v1/activity_records/search | [Search Parameters](PostData/SearchParameters) | Returns Activity Records matching a criteria defined in search parameters.  [Search Activity Records](SearchActivityRecords) |
| POST | /netwrix/api/v1/activity_records/ | [Activity Records](PostData/ActivityRecords) | Writes data to the Audit Database.  [Write Activity Records](WriteActivityRecords) |

### Authentication

Authentication is required for all endpoints. The following authentication methods are supported:

* NTLM—recommended

  If NTLM authentication is disabled through a group policy, you will not be able to address Netwrix Auditor Server by its IP address.
* Negotiate
* Digest
* Basic

### Account Permissions

Netwrix Auditor restricts control to its configuration and data collected by the product. Role-based access system ensures that only relevant employees and services can access the exact amount of data they need. To be able to retrieve activity records or supply data to the Audit Database, an account must be assigned a role in the product. [Role-Based Access and Delegation](../Admin/MonitoringPlans/Delegation)

| To... | Required role |
| --- | --- |
| Retrieve all activity records and write data | The user must be assigned the Global administrator role in the product, or be a member of the Netwrix Auditor Administrators group on the computer that hosts Netwrix Auditor Server. |
| Retrieve all activity records | The user must be assigned the Global reviewer role in the product or be a member of the Netwrix Auditor Client Users group on the computer that hosts Netwrix Auditor Server. |
| Retrieve activity records within a limited scope | The user must be assigned the Reviewer role on a monitoring plan or folder with plans. In this case, Netwrix Auditor Server will retrieve only activity records the user is allowed to review according to the scope delegated (e.g., a scope can be limited to a single domain or file share). |
| Write activity records | The user must be assigned the Contributor role in the product. |

Review the example below to see how to authenticate in cURL:

* `curl https://172.28.6.15:9699/netwrix/api/v1/activity_records/enum -u Enterprise\NetwrixUser:NetwrixIsCool`