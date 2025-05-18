---
title: "Search Parameters"
sidebar_position: 715
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

# Search Parameters

Send the search parameters in the POST request body to narrow down the search results returned by the [/netwrix/api/v1/activity_records/search](../SearchActivityRecords) endpoint. The Search parameters file includes one or more filters with operators and values (e.g., to find entries where *data source* is *SharePoint*); it may also contain a [Continuation Mark](ContinuationMark.htm "Continuation Mark"). Generally, the Search parameters file looks similar to the following:

|  |
| --- |
| XML |
| ```
 ```
```
 ```
```
Continuation mark ```
```
 ```
```
Value ```
```
Value1 ```
```
Value2 ```
```
Value1 ```
```
Value2 ```
```
Value1 ```
```
Value2 ```
```
 ```
```
 ```
|
| JSON |
| ```
{ ```
```
"ContinuationMark": "Continuation Mark", ```
```
"FilterList": { ```
```
"Filter1": "Value", ```
```
"Filter2": [ "Value1", "Value2" ], ```
```
"Filter3": { ```
```
"MatchType1": "Value1", ```
```
"MatchType2": "Value2" ```
```
}, ```
```
"Filter4": [ "Value1", { "MatchType": "Value2" } ] ```
```
} ```
```
} ```
|

Ensure to pass information about transferred data, including `Content-Type:application/xml` or `application/json` and encoding. The syntax greatly depends on the tool you use.

## Schema

| Format | Schema description |
| --- | --- |
| XML | The file must be compatible with the XML schema. On the computer where Auditor Server resides, you can find XSD file under *Netwrix_Auditor_installation_folder\Audit Core\API Schemas*.  The `ActivityRecordSearch` root element includes the `FilterList` element with one or more `Filter` elements inside. The root element may contain a `ContinuationMark` element.  Each `Filter` specified within the `FilterList` must have a value to search for. The element may also include a modifier—a match type operator.  minOccurs="0" indicates that element is optional and may be absent in the Search parameters. |
| JSON | The `FilterList` object includes with one or more `Filter` entries inside. JSON may contain a `ContinuationMark` object. Each `Filter` specified within the `FilterList` must have a value to search for. The entry may also include a modifier—a match type operator. |

Review the following for additional information:

* [Filters](../Filters)
* [Operators](../FilterOperators)

## Example

|  |
| --- |
| XML |
| ```
 ```
```
 ```
```
 ```
```
Administrator ```
```
My Hybrid Cloud enterprise  ```
```
Active Directory ```
```
Exchange ```
```
Removed ```
```
Added ```
```
Group ```
```
 ```
```
2016-01-16T16:30:00+11:00 ```
```
2017-01-01T00:00:00Z ```
```
 ```
```
 ```
```
 ```
|
| JSON |
| ```
{ ```
```
"FilterList": { ```
```
"Who": { "NotEqualTo": "Administrator" }, ```
```
"MonitoringPlan": "My Hybrid Cloud enterprise", ```
```
"DataSource": [ "Active Directory", { "StartsWith": "Exchange" } ], ```
```
"Action": [ "Added", "Removed" ], ```
```
"ObjectType": { "DoesNotContain": "Group" }, ```
```
"When": { ```
```
"From": "2016-01-16T16:30:00+11:00", ```
```
"To": "2017-01-01T00:00:00Z" ```
```
} ```
```
} ```
```
} ```
|