---
title: "Continuation Mark"
sidebar_position: 713
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

# Continuation Mark

When exporting data from the Audit Database, a successful response includes:

* For XML—A `` inside the `` root element.
* For JSON—An object with the "ContinuationMark" field.

Continuation mark is a checkpoint, use it to retrieve data starting with the next Activity Record.

Send a POST request containing Continuation mark to the following endpoints:

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | [/netwrix/api/v1/activity_records/enum](../RetrieveActivityRecords) | Returns next Activity Records. |
| POST | [/netwrix/api/v1/activity_records/search](../SearchActivityRecords) | Returns next Activity Records matching a filter criteria. |

Ensure to pass information about transferred data, including `Content-Type:application/xml` or `application/json` and encoding. The syntax greatly depends on the tool you use.

You can send as many POST requests as you want. A new response returns next Activity Records and a new Continuation mark. Once all the Activity Records are retrieved, you will receive a 200 OK response with no Activity Records inside the `ActivityRecordList` root element (XML) or array (JSON).

## Schema

Copy the contents of `ContinuationMark` to a separate XML or JSON file (e.g., ContMark.xml).

| Format | Schema description |
| --- | --- |
| XML | The file must be compatible with the XML schema. On the computer where Auditor Server resides, you can find XSD file under *Netwrix_Auditor_installation_folder\Audit Core\API Schemas*.  The `ContinuationMark` root element contains a value previously returned by Netwrix Auditor Integration API. |
| JSON | JSON-formatted Continuation mark includes the field value in quotes. |

If you want to retrieve next Activity Records for your search, include the Continuation mark to your Search parameters file. [Search Parameters](SearchParameters)

## Example

|  |
| --- |
| XML |
| [Retrieve Activity Records](../RetrieveActivityRecords) |
| ```
 ```
```
 ```
```
PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A+PC9ucj4A ```
```
 ```
|
| [Search Activity Records](../SearchActivityRecords) |
| ```
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
| [Retrieve Activity Records](../RetrieveActivityRecords) |
| ```
"PG5yPjxuIG49IntFNzA...PjwvYT48L24+PC9ucj4A" ```
|
| [Search Activity Records](../SearchActivityRecords) |
| ```
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