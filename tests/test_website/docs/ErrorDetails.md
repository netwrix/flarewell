---
title: "Error Details"
sidebar_position: 706
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

# Error Details

On error, most requests contain an error description in the response body (except some requests with empty body, e.g., 404, 405). [Response Status Codes](ResponseStatusCodes)

The error details include:

| Block | Description |
| --- | --- |
| Category | Defines the type of error (XML formatting-related error, invalid input-related error, etc.) |
| Description | Provides details about this error. |
| Location | (optional) Provides a link to a corrupted text in request.  XML is considered a default format for Netwrix Auditor Integration API. Error location is defined in XML format. |

The error details have the format similar to the following:

| Format | Example |
| --- | --- |
| XML | ```
 ```
```
 ```
```
 ```
```
Category ```
```
Error Description ```
```
Error Location ```
```
 ```
```
 ```
|
| JSON | ```
{ ```
```
"ErrorList": [ ```
```
{ ```
```
"Category": "Category", ```
```
"Description": "Error Description", ```
```
"Location": "Error Location" ```
```
} ```
```
] ```
```
} ```
|

Review examples below to see how error details correspond to invalid requests.

| Request | Error details returned |
| --- | --- |
| Invalid request:  XML:  `curl -H "Content-Type: application/xml; Charset=UTF-8" https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/search -u Enterprise NetwrixUser:NetwrixIsCool --data-binary @C:\APIdocs\Search.xml`   ```
 ```
```
 ```
```
 ```
```
Administrator ```
```
Active Directory ```
```
Modified ```
```
 ```
```
 ```
* JSON:   `curl -H "Content-Type: application/json; Charset=UTF-8" https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/search?format=json -u Enterprise\NetwrixUser: NetwrixIsCool --data-binary @C:\APIdocs\Search.json`   ```
{ ```
```
"FilterList": { ```
```
"Who": "Administrator", ```
```
"DataSource": "Active Directory ```
```
"Action": "Added" ```
```
} ```
```
} ```
| 400 Bad Request   * XML:  ```
 ```
```
 ```
```
 ```
```
XMLError ```
```
0xC00CE56D End tag 'FilterList'  does not match the start tag 'DataSource' ```
```
 ```
```
 ```
```
 ```
* JSON:   If JSON is corrupted, server returns 500 Internal Server Error with empty body. |
| Invalid request:   * XML:   `curl https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/ enum?count=FIVE -u Enterprise NetwrixUser:NetwrixIsCool`   * JSON:   `curl https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/ enum?format=json&count=FIVE -u Enterprise\NetwrixUser: NetwrixIsCool` | 400 Bad Request   * XML:  ```
 ```
```
 ```
```
 ```
```
InputError ```
```
Invalid count parameter specified.  Error details: 0x80040204 Cannot convert the  attribute data type  ```
```
 ```
```
 ```
```
 ```
* JSON:  ```
{ ```
```
"ErrorList": [ ```
```
{ ```
```
"Category": "InputError", ```
```
"Description": "Invalid count parameter specified.  Error details: 0x80040204 Cannot convert the  attribute data type" ```
```
} ```
```
] ```
```
} ```
|
| Valid request, but the Audit Database is unreachable:   * XML:   `curl https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/enum -u Enterprise NetwrixUser:NetwrixIsCool`   * JSON:   `curl https://WKSWin12R2:9699/ netwrix/api/v1/activity_records/enum?format=json -u Enterprise\NetwrixUser: NetwrixIsCool` | 500 Internal Server Error   * XML:  ```
 ```
```
 ```
```
 ```
```
ServerError ```
```
0x80040C0A SQL Server cannot be  contacted, connection is lost (0x80040C0A SQL  Server cannot be contacted, connection is lost  (0x80004005 [DBNETLIB][ConnectionOpen (Connect()). ]SQL Server does not exist or access denied.))  [0x00007FFDCC06BBC8,0x00007FFDB99EF4BA; 0x00007FFDB99BEEEF,0x00007FFDB99EF4DC] ```
```
 ```
```
 ```
```
 ```
* JSON:  ```
{ ```
```
"ErrorList": [ ```
```
{ ```
```
"Category": "ServerError", ```
```
"Description": "0x80040C0A SQL Server cannot be  contacted, connection is lost (0x80040C0A SQL  Server cannot be contacted, connection is lost  (0x80004005 [DBNETLIB][ConnectionOpen (Connect()). ]SQL Server does not exist or access denied.))  [0x00007FFDCC06BBC8,0x00007FFDB99EF4BA; 0x00007FFDB99BEEEF,0x00007FFDB99EF4DC]" ```
```
} ```
```
] ```
```
} ```
|