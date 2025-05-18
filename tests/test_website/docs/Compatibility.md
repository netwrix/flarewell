---
title: "Compatibility Notice"
sidebar_position: 702
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

# Compatibility Notice

Make sure to check your product version, and then review and update your add-ons and scripts leveraging Netwrix Auditor Integration API. Download the latest add-on version in the Add-on Store.

| Property in 8.0 – 8.5 | New property in 9.0 and above |
| --- | --- |
| * XML:  ```
 ```
* JSON:  ```
"AuditedSystem" ```
| * XML:  ```
 ```
* JSON:  ```
"DataSource" ```
|
| * XML:  ```
 ```
* JSON:  ```
"ManagedObject" ```
| * XML:  ```
 ```
```
Name ```
```
Unique ID ```
```
 ```
* JSON:  ```
"MonitoringPlan" : { ```
```
"ID": "{Unique ID}", ```
```
"Name": "Name" ```
```
} ```
Now the MonitoringPlan contains two sub-entries: ID and Name. The ID property is optional and is assigned automatically by the product. |
| — | * XML:  ```
 ```
```
Item name ```
```
 ```
* JSON:  ```
"Item": {"Name": "Item name"} ```
|

To learn more about input and output Activity Record structure, refer to [Activity Records](PostData/ActivityRecords).