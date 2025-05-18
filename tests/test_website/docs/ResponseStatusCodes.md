---
title: "Response Status Codes"
sidebar_position: 703
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

# Response Status Codes

| Code | Status | Write Activity Records | Retrieve, search Activity Records |
| --- | --- | --- | --- |
| 200 OK | Success | Success. The body is empty.  Activity Records were written to the Audit Database and the Long-Term Archive. | Success. The body contains Activity Records.  Activity Records were retrieved from the Audit Database. |
| 400 Bad Request | Error | Error validating Activity Records.  Make sure the Activity Records are compatible with the [Schema](PostData/ActivityRecords.htm#Schema "Activity Records"). | Error validating request parameters or post data.  Make sure the post data files (Continuation mark, Search parameters) are compatible with their schemas and the `?count=` parameter is valid. |
| 401 Unauthorized | Error | The request is unauthorized and the body is empty. See for [API Endpoints](Endpoints.htm "API Endpoints") more information. | |
| 404 Not Found | Error | Error addressing the endpoint. The body is empty. The requested endpoint does not exist (e.g., /netwrix/api/v1/mynewendpoint/). | |
| 405 Method Not Allowed | Error | Error addressing the endpoint. The body is empty. Wrong HTTP request was sent (any except POST). | Error addressing the endpoint. The body is empty. Wrong HTTP request was sent (any except GET or POST). |
| 413 Request Entity Too Large | Error | Error transferring files. The body is empty. The posted file exceeds supported size. | |
| 500 Internal Server Error | Error | Error writing Activity Records to the Audit Database or the Long-Term Archive:   * One or more Activity Records were not processed. * Netwrix Auditor license has expired. * Internal error occurred. | Error retrieving Activity Records from the Audit Database:   * Netwrix Auditorlicense has expired. * The Netwrix Auditor Archive Service is unreachable. Try restarting the service on the computer that hosts Netwrix Auditor Server. * Internal error occurred. |
| 503 Service Unavailable | Error | The Netwrix Auditor Archive Service is busy or unreachable. Try restarting the service on the computer that hosts Netwrix Auditor Server. | — |

Most failed requests contain error in the response body (except those with empty body, e.g., 404, 405). [Error Details](ErrorDetails)