---
title: "Search Activity Records"
sidebar_position: 697
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

# Search Activity Records

The search functionality in the Netwrix Auditor Integration API reproduces interactive search available in the Netwrix Auditor client. See the [Netwrix Auditor Intelligence Guide](`https://www.netwrix.com/download/documents/Netwrix_Auditor_User_Guide.pdf` "Netwrix Auditor Intelligence Guide") and [View and Search Collected Data](../Admin/Search/Overview.htm "View and Search Collected Data") topic for detailed instruction on how to search and filter audit data.

As the interactive search in the Netwrix Auditor client, this REST API endpoint allows you to retrieve Activity Records matching a certain criteria. You can create your own set of filters in the Search parameters file. See the [Search Parameters](PostData/SearchParameters.htm "Search Parameters") topic for more information. Activity Records are retrieved according to the account's delegated scope.

## Endpoint

To retrieve Activity Records matching a certain criteria, send a POST request containing search parameters (also may include a Continuation mark). See the [Search Parameters](PostData/SearchParameters.htm "Search Parameters") topic for more information.

| Method | Endpoint | POST Data |
| --- | --- | --- |
| `POST` | ``https://\{host:port\}/netwrix/api/v1/activity_records/search\{?format=json\}\{&count=Number\}`` | [Search Parameters](PostData/SearchParameters) |

## Request Parameters

| Parameter | Mandatory | Description |
| --- | --- | --- |
| `host:port` | Yes | Replace with the IP address or a name of your Netwrix Auditor Server host and port (e.g., *172.28.6.15:9699*, *stationwin12:9699*, *WKSWin2012.enterprise.local:9699*).  With enabled HTTPS, provide the computer name as it appears in certificate properties. |
| `format=json` | No | Add this parameter to retrieve data in JSON format. Otherwise, XML-formatted Activity Records will be returned. |
| `count=Number` | No | Add this parameter to define the number of Activity Records to be exported. Replace `Number` with a number (e.g., `?count=1500`). |

Optional parameters (format and count) can be provided in any order. The first parameter must start with ?, others are joined with &, no spaces required (e.g., `?format=json&count=1500`).

## Response

| Request Status | Response |
| --- | --- |
| Success | The HTTP status code in the response header is 200 OK. The response body contains Activity Records and Continuation Mark.   |  |  |  | | --- | --- | --- | | ```
HTTP/1.1 200 OK ```
```
Server: Microsoft-HTTPAPI/2.0 ```
```
Content-Length: 311896 ```
```
Content-Type: application/xml ```
```
Date: Fri, 08 Apr 2017 13:56:22 GMT ```
| or | ```
HTTP/1.1 200 OK ```
```
Server: Microsoft-HTTPAPI/2.0 ```
```
Content-Length: 311896 ```
```
Content-Type: application/json ```
```
Date: Fri, 08 Apr 2017 13:56:22 GMT ```
| |
| Error | The header status code is an error code. Depending on the error code, the response body may contain an error object. |

## Usage Example—Retrieve All Activity Records Matching Search Criteria

Follow the steps- to retrieve all Activity Records matching search criteria.

**Step 1 –** Send a POST request containing search parameters. See the [Search Parameters](PostData/SearchParameters.htm "Search Parameters") topic for more information.

As an example, this request retrieves Activity Records where administrator added new objects to the Active Directory domain. Groups and group policies are not taken into account. Changes could only occur between September 16, 2016 and March 16, 2017.

Ensure to pass information about transferred data, including `Content-Type:application/xml` or `application/json` and encoding. The syntax greatly depends on the tool you use.

**Step 2 –** Receive the response. Activity Records are retrieved according to the account's delegated scope. Below is an example of a successful search request. The status is 200 OK. For XML, a response body contains the `ActivityRecordList` root element with Activity Records matching filter criteria and a Continuation mark inside. For JSON, a response body contains the `ActivityRecordList` array with Activity Records matching filter criteria and collected in braces \{\}, and a Continuation mark.

|  |
| --- |
| XML |
| ```
 ```
```
 ```
```
PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A ```
```
 ```
```
 ```
```
AD Monitoring ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
 ```
```
Active Directory ```
```
 ```
```
enterprise.local (Domain) ```
```
 ```
```
user ```
```
20160215110503420B9451771F5964A9EAC0A5F35307EA155 ```
```
\local\enterprise\Users\Jason Smith ```
```
Added ```
```
2017-02-14T15:42:34Z ```
```
EnterpriseDC1.enterprise.local ```
```
ENTERPRISE\Administrator ```
```
EnterpriseDC1.enterprise.local ```
```
 ```
```
... ```
```
... ```
```
 ```
|
| JSON |
| ```
{ ```
```
"ActivityRecordList": [ ```
```
{ ```
```
"Action": "Added", ```
```
"MonitoringPlan" : { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "AD Monitoring" ```
```
}, ```
```
"DataSource": "Active Directory", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType": "user", ```
```
"RID": "20160215110503420B9451771F5964A9EAC0A5F35307EA155", ```
```
"What": "\\local\\enterprise\\Users\\Jason Smith", ```
```
"When": "2017-02-14T15:42:34Z", ```
```
"Where": "EnterpriseDC1.enterprise.local", ```
```
"Who": "ENTERPRISE\\Administrator", ```
```
"Workstation": "EnterpriseDC1.enterprise.local" ```
```
}, ```
```
{...}, ```
```
{...} ```
```
], ```
```
"ContinuationMark": "PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A" ```
```
} ```
|

**Step 3 –** Continue retrieving Activity Records. Send a POST request containing your search parameters and this Continuation mark to the same endpoint. [Continuation Mark](PostData/ContinuationMark)

|  |
| --- |
| XML |
| `curl -H "Content-Type:application/xml; Charset=UTF-8" https://WKSWin2012:9699/netwrix/api/v1/activity_records/search -u Enterprise\NetwrixUser:NetwrixIsCool --data-binary @C:\APIdocs\Search.xml`   ```
 ```
```
 ```
```
PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A+PC9ucj4A ```
```
 ```
```
Administrator ```
```
Active Directory ```
```
Added ```
```
Group ```
```
 ```
```
2016-09-16T16:30:00+11:00 ```
```
2017-03-16T00:00:00Z ```
```
 ```
```
 ```
```
 ```
|
| JSON |
| `curl -H "Content-Type:application/json; Charset=UTF-8" https://WKSWin2012:9699/netwrix/api/v1/activity_records/search?format=json -u Enterprise\NetwrixUser:NetwrixIsCool --data-binary @C:\APIdocs\Search.json`   ```
{ ```
```
"ContinuationMark": "PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A+PC9ucj4A", ```
```
"FilterList": { ```
```
"Who": "Administrator", ```
```
"DataSource": "Active Directory", ```
```
"Action": "Added", ```
```
"ObjectType": { "DoesNotContain": "Group"}, ```
```
"When": { ```
```
"From": "2016-09-16T16:30:00+11:00", ```
```
"To": "2017-03-16T00:00:00Z" ```
```
} ```
```
} ```
```
} ```
|

Ensure to pass information about transferred data, including `Content-Type:application/xml` or `application/json` and encoding. The syntax greatly depends on the tool you use.

**Step 4 –** Receive the next response. On success, the status is 200 OK. For XML, a response body contains the `ActivityRecordList` root element with next Activity Records and a new Continuation mark inside. For JSON, a response body contains the `ActivityRecordSearch` array with next Activity Records collected in braces \{\} and a new Continuation mark.

**Step 5 –** Continue retrieving Activity Records. Send POST requests containing your search parameters with new Continuation marks until you receive a 200 OK response with no Activity Records inside the `ActivityRecordList`. It means you retrieved all Activity Records matching your search criteria.