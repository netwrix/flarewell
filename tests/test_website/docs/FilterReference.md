---
title: "Reference for Creating Search Parameters File"
sidebar_position: 699
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

# Reference for Creating Search Parameters File

Review this section to learn more about operators and how to apply them to Activity Record filters to create a unique search. You can:

* Add different filters to your search. Search results will be sorted by all selected filters since they work as a logical AND.

  | Format | Example |
  | --- | --- |
  | XML | ```
Admin ```
```
Active Directory ```
```
User ```
|
  | JSON | ```
"Who" : { "Equals" : "Admin" }, ```
```
"DataSource" : { "NotEqualTo" : "Active Directory" }, ```
```
"What" : "User" ```
|
* Specify several values for the same filter. To do this, add two entries one after another.

  Entries with Equals, Contains, StartsWith, EndsWith, and InGroup operators work as a logical OR (Activity Records with either of following values will be returned). Entries with DoesNotContain and NotEqualTo operators work as a logical AND (Activity Records with neither of the following values will be returned).

  | Format | Example |
  | --- | --- |
  | XML | ```
Admin ```
```
Analyst ```
|
  | JSON | ```
"Who" : [ "Admin" , "Analyst" ] ```
Use square brackets to add several values for the entry. |

Review the following for additional information:

* [Filters](Filters)
* [Operators](FilterOperators)

The table below shows filters and Activity Records matching them.

| Filters | Matching Activity Records |
| --- | --- |
| * XML:  ```
Administrator ```
```
 ```
```
SharePoint ```
```
 ```
```
 ```
```
Read ```
```
 ```
* JSON:  ```
"Who" : "Admin", ```
```
"DataSource" : "SharePoint", ```
```
"Action" : { ```
```
"NotEqualTo" : "Read"  ```
```
} ```
| Retrieves all activity records where administrator made any actions on SharePoint, except Read.   * XML:  ```
 ```
```
Added ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
SharePoint ```
```
 ```
```
http://demolabsp:8080 (SharePoint farm) ```
```
 ```
```
List ```
```
20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7 ```
```
`http://demolabsp/lists/Taskslist ```
```
2017-02-17T09:28:35Z ```
```
`http://demolabsp ```
```
Enterprise\Administrator ```
```
172.28.15.126 ```
```
 ```
```
 ```
```
Removed ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
SharePoint ```
```
 ```
```
http://demolabsp:8080 (SharePoint farm) ```
```
 ```
```
List ```
```
20160217093959797091D091D2EAF4A89BF7A1CCC27D15857 ```
```
`http://demolabsp/lists/Old/Taskslist ```
```
2017-02-17T09:28:35Z ```
```
`http://demolabsp ```
```
Enterprise\Administrator ```
```
172.28.15.126 ```
```
 ```
* JSON:  ```
{ ```
```
"Action": "Added", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "SharePoint", ```
```
"Item": {"Name": "http://demolabsp:8080 (SharePoint farm)"}, ```
```
"ObjectType" : "List", ```
```
"RID" : "20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7", ```
```
"What" : "`http://demolabsp/lists/Taskslist",` ```
```
"When" : "2017-02-17T09:28:35Z", ```
```
"Where" : "`http://demolabsp",` ```
```
"Who" : "Enterprise\\Administrator", ```
```
"Workstation" : "172.28.15.126" ```
```
}, ```
```
{ ```
```
"Action" : "Removed", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "SharePoint", ```
```
"Item": {"Name": "http://demolabsp:8080 (SharePoint farm)"}, ```
```
"ObjectType" : "List", ```
```
"RID": "20160217093959797091D091D2EAF4A89BF7A1CCC27D15857", ```
```
"What" : "`http://demolabsp/lists/Old/Taskslist",` ```
```
"When" : "2017-02-17T09:28:35Z", ```
```
"Where" : "`http://demolabsp",` ```
```
"Who" : "Enterprise\\Administrator", ```
```
"Workstation" : "172.28.15.126" ```
```
} ```
|
| * XML:  ```
Administrator ```
```
Added ```
* JSON:  ```
"Who" : "Administrator", ```
```
"Action" : "Added" ```
| Retrieves all activity records where administrator added an object within any data source.   * XML:  ```
 ```
```
Added ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
SharePoint ```
```
 ```
```
http://demolabsp:8080 (SharePoint farm) ```
```
 ```
```
List ```
```
20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7 ```
```
`http://demolabsp/lists/Taskslist ```
```
2017-02-17T09:28:35Z ```
```
`http://demolabsp ```
```
Enterprise\Administrator ```
```
172.28.15.126 ```
```
 ```
```
 ```
```
Added ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
Exchange ```
```
 ```
```
enterprise.local (Domain) ```
```
 ```
```
Mailbox ```
```
2016021116354759207E9DDCEEB674986AD30CD3D13F5DEA3 ```
```
Shared Mailbox ```
```
2017-02-10T14:46:00Z ```
```
eswks.enterprise.local ```
```
Enterprise\Administrator ```
```
 ```
* JSON:  ```
{ ```
```
"Action" : "Added", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "SharePoint", ```
```
"Item": {"Name": "http://demolabsp:8080 (SharePoint farm)"}, ```
```
"ObjectType": "List", ```
```
"RID": "20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7", ```
```
"What": "`http://demolabsp/lists/Taskslist",` ```
```
"When": "2017-02-17T09:28:35Z", ```
```
"Where": "`http://demolabsp",` ```
```
"Who": "Enterprise\\Administrator", ```
```
"Workstation": "172.28.15.126" ```
```
}, ```
```
{ ```
```
"Action" : "Added", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource" : "Exchange", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType" : "Mailbox", ```
```
"RID": "2016021116354759207E9DDCEEB674986AD30CD3D13F5DEA3", ```
```
"What": "Shared Mailbox", ```
```
"When": "2017-02-10T14:46:00Z", ```
```
"Where": "eswks.enterprise.local", ```
```
"Who": "Enterprise\\Administrator" ```
```
} ```
|
| * XML:  ```
Admin ```
```
Analyst ```
* JSON:  ```
"Who" : [ "Admin" , "Analyst" ] ```
| Retrieves all activity records where admin or analyst made any changes within any data source.   * XML:  ```
 ```
```
Added ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
File Servers ```
```
 ```
```
wks.enterprise.local (Computer) ```
```
 ```
```
Folder ```
```
2016021116354759207E9DDCEEB674986AD30CD3D13F5DDA3 ```
```
Annual_Reports ```
```
2017-02-10T14:46:00Z ```
```
wks.enterprise.local ```
```
Enterprise\Admin ```
```
 ```
```
 ```
```
Removed ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
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
User ```
```
2016021116354759207E9DDCEEB674986AD30CD3D13F5DAA3 ```
```
Anna.Smith ```
```
2017-02-10T10:46:00Z ```
```
dc1.enterprise.local ```
```
Enterprise\Analyst ```
```
172.28.6.15 ```
```
 ```
* JSON:  ```
{ ```
```
"Action": "Added", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource" : "File Servers", ```
```
"Item": {"Name": "wks.enterprise.local (Computer)"}, ```
```
"ObjectType": "Folder", ```
```
"RID": "2016021116354759207E9DDCEEB674986AD30CD3D13F5DDA3", ```
```
"What": "Annual_Reports", ```
```
"When": "2017-02-10T14:46:00Z", ```
```
"Where": "wks.enterprise.local", ```
```
"Who": "Enterprise\\Admin" ```
```
}, ```
```
{ ```
```
"Action": "Removed", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "Active Directory", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType": "User", ```
```
"RID": "2016021116354759207E9DDCEEB674986AD30CD3D13F5DAA3", ```
```
"What": "Anna.Smith", ```
```
"When": "2017-02-10T10:46:00Z", ```
```
"Where": "dc1.enterprise.local", ```
```
"Who": "Enterprise\\Analyst", ```
```
"Workstation": "172.28.6.15" ```
```
} ```
|
| * XML:  ```
 ```
```
 ```
```
 ```
```
 ```
```
 ```
```
2017-01-16T16:30:00Z ```
```
 ```
```
 ```
```
2017-02-01T00:00:00Z ```
```
 ```
```
 ```
* JSON:   "When" : [  \{"LastSevenDays" : ""\},  \{  "From" : "2017-01-16T16:30:00Z",  "To" : "2017-02-01T00:00:00Z"  \}  ] | Retrieves all activity records for all data sources and users within a specified data range:   * January 16, 2017 — February 1, 2017 * March 11, 2017 — March 17, 2017 (assume, today is March, 17).      * XML:  ```
 ```
```
Modified ```
```
My Cloud ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23701} ```
```
My Cloud ```
```
 ```
```
Exchange Online ```
```
 ```
```
mail@corp.onmicrosoft.com (Office 365 tenant) ```
```
 ```
```
Mailbox ```
```
201602170939597970997D56DDA034420B9044249CC15EC5A ```
```
Shared Mailbox ```
```
2017-03-17T09:37:11Z ```
```
BLUPR05MB1940 ```
```
admin@corp.onmicrosoft.com ```
```
 ```
```
 ```
```
Successful Logon ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
Logon Activity ```
```
 ```
```
enterprise.local (Domain) ```
```
 ```
```
Logon ```
```
20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7 ```
```
stationexchange.enterprise.local ```
```
2017-02-17T09:28:35Z ```
```
enterprisedc1.enterprise.local ```
```
ENTERPRISE\Administrator ```
```
stwin12R2.enterprise.local ```
```
 ```
* JSON:  ```
{ ```
```
"Action" : "Modified", ```
```
"MonitoringPlan" : "My Cloud", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23701}", ```
```
"Name": "My Cloud" ```
```
}, ```
```
"DataSource": "Exchange Online", ```
```
"Item": { ```
```
"Name": "mail@corp.onmicrosoft.com (Office 365 tenant)" ```
```
}, ```
```
"ObjectType" : "Mailbox", ```
```
"RID" : "201602170939597970997D56DDA034420B9044249CC15EC5A", ```
```
"What" : "Shared Mailbox", ```
```
"When" : "2017-03-17T09:37:11Z", ```
```
"Where" : "BLUPR05MB1940", ```
```
"Who" : "admin@corp.onmicrosoft.com" ```
```
}, ```
```
{ ```
```
"Action" : "Successful Logon", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "Logon Activity", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType": "Logon", ```
```
"RID" : "20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7", ```
```
"What" : "stationexchange.enterprise.local", ```
```
"When" : "2017-02-17T09:28:35Z", ```
```
"Where" : "enterprisedc1.enterprise.local", ```
```
"Who" : "ENTERPRISE\\Administrator", ```
```
"Workstation" : "stwin12R2.enterprise.local" ```
```
} ```
|
| * XML:  ```
 ```
```
Logon Activity ```
```
 ```
* JSON:  ```
"DataSource" : "Logon Activity" ```
| Retrieves all activity records for Logon Activity data source irrespective of who made logon attempt and when it was made.   * XML:  ```
 ```
```
Successful Logon ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
Logon Activity ```
```
 ```
```
enterprise.local (Domain) ```
```
 ```
```
Logon ```
```
20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7 ```
```
stationexchange.enterprise.local ```
```
2017-02-17T09:28:35Z ```
```
enterprisedc1.enterprise.local ```
```
ENTERPRISE\Administrator ```
```
stwin12R2.enterprise.local ```
```
 ```
```
 ```
```
Successful Logon ```
```
 ```
```
{42F64379-163E-4A43-A9C5-4514C5A23798} ```
```
Compliance ```
```
 ```
```
Logon Activity ```
```
 ```
```
enterprise.local (Domain) ```
```
 ```
```
Logon ```
```
201602170939597970997D56DDA034420B9044249CC15EC5A ```
```
stationwin12r2.enterprise.local ```
```
2017-02-17T09:37:11Z ```
```
enterprisedc2.enterprise.local ```
```
ENTERPRISE\Analyst ```
```
stwin12R2.enterprise.local ```
```
 ```
* JSON:  ```
{ ```
```
"Action" : "Successful Logon", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "Logon Activity", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType" : "Logon", ```
```
"RID" : "20160217093959797091D091D2EAF4A89BF7A1CCC27D158A7", ```
```
"What" : "stationexchange.enterprise.local", ```
```
"When" : "2017-02-17T09:28:35Z", ```
```
"Where" : "enterprisedc1.enterprise.local", ```
```
"Who" : "ENTERPRISE\\Administrator", ```
```
"Workstation" : "stwin12R2.enterprise.local" ```
```
}, ```
```
{ ```
```
"Action" : "Successful Logon", ```
```
"MonitoringPlan": { ```
```
"ID": "{42F64379-163E-4A43-A9C5-4514C5A23798}", ```
```
"Name": "Compliance" ```
```
}, ```
```
"DataSource": "Logon Activity", ```
```
"Item": {"Name": "enterprise.local (Domain)"}, ```
```
"ObjectType" : "Logon", ```
```
"RID" : "201602170939597970997D56DDA034420B9044249CC15EC5A", ```
```
"What" : "stationwin12r2.enterprise.local", ```
```
"When" : "2017-02-17T09:37:11Z", ```
```
"Where" : "enterprisedc2.enterprise.local", ```
```
"Who" : "ENTERPRISE\\Analyst", ```
```
"Workstation" : "stwin12R2.enterprise.local" ```
```
} ```
|