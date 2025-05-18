---
title: "Use Filters in Advanced Mode"
sidebar_position: 908
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

# Use Filters in Advanced Mode

Netwrix Auditor provides an advanced set of filters and match type operators that enable you to customize your searches even more precisely.

Switch to Advanced mode to review your current search in details and modify it if necessary. Click Add to add a new filter to your search.

Review the following for additional information:

* [Apply Additional Filters](#Apply)
* [Search Conditions](#Change "Search Conditions")

## Apply Additional Filters

Expand the Filter list to find additional filters or filter values. The most commonly used filters are described in [Use Filters in Simple Mode](FilterSimple.htm "Use Filters in Simple Mode"). Review the following for additional information:

| Filter | Description | Example |
| --- | --- | --- |
| Action | Limits your search to the selected actions only.  Specify an action from the Value list or type it yourself. The Action filter in the Advanced mode contains actions besides those available in basic mode (added, modified, removed, and read). Reported actions vary depending on the data source and object type.   |  |  | | --- | --- | | * Added | * Add (Failed Attempt) | | * Removed | * Remove (Failed Attempt) | | * Modified | * Modify (Failed Attempt) | | * Read | * Read (Failed Attempt) | | * Moved | * Move (Failed Attempt) | | * Renamed | * Rename (Failed Attempt) | | * Checked in | * Checked out | | * Discard check out | * Successful Logon | | * Failed Logon | * Logoff | | * Copied | * Sent | | * Session start | * Session end | | * Activated |  | | You are investigating suspicious user activity. You have already identified the intruder and now you want to see if any files were deleted or moved, and emails sent.  Since you are interested in specific actions only, set the Action filter to Removed, Moved, and Sent. |
| Object type | Limits your search to objects of a specific type only.  Specify an object type from the Value list or type it yourself. This filter modifies the What filter.  The value list is prepopulated with the most frequent object types. | You noticed that some domain policies were changed and you want to investigate this issue.  Your What filter is set to *Policy*, and so you keep receiving search results such as *HiSecPolicy, \\FS\Share\NewPolicy.docx*, *`http://corp/sites/col1/Lists/Policy.*` These entries correspond to different object types and data sources.  Since you are looking for GPOs only, select GroupPolicy from the Value list. |
| Data source | Limits your search to the selected data source only.  Specify a data source from the Value list or type it yourself. | You are investigating suspicious user activity. A user specified in the Who filter made a lot of changes across your IT infrastructure, so the search results became difficult to review.  Since you are only interested in the way this user's activity could affect your Active Directory domain and Exchange organization, set the Data source filter to Active Directory and Exchange to limit the search results. |
| Monitoring plan | Limits your search to the selected plan only.  Specify the name from the Value list or type it yourself. | You are investigating suspicious user activity. A user specified in the Who filter made a lot of changes across your IT infrastructure, so the search results became difficult to review.  Since you are only interested in the way this user's activity could affect file shares audited within a single plan, set the Monitoring plan filter to *"My servers"* to limit the search results. |
| Item | Limits your search to the selected item only.  This filter can be helpful if have several items of the same type in your monitoring plan (e.g., two Active Directory domains).  Specify the name from the Value list or type it yourself. | Your monitoring plan is configured to track domains and includes your secured corporate domain and a domain for temporary employees. You are investigating who logged in your secured corporate domain outside business hours.  You can set the Item filter to this domain name to limit the search results and exclude logons to computers from a less important domain. |
| Working hours | Limits your search results to entries that occurred within the specified hours.  You can use this filter together with When if you need, for example, to search for activity in the non-business hours during the last week. | You are investigating an incident and want to know who accessed sensitive data outside business hours.  You can set this filter as *Not equal to* and specify the time interval from *8:00 AM* to *6:00 PM*. Filtered data will include only operations that occurred outside this interval, that is, during non-business hours. |
| Data categories | Limits your search results to entries that contain sensitive data comply with a classification rule.  You can use this filter together with Equal to PCIDSS to, for example, to search for sensitive files that contain data regulated by the PCIDSS. | You are searching all documents containing cardholder data that can potentially be mapped with the PCIDSS compliance standard.  You can set this filter *as equal to* and specify the value as *PCIDSS*. Filtered data will contain only files that match this criteria.  This filter shows activity records collected from the following data sources:   * Windows File Servers * ShrePoint * SharePoint Online |
| Details | Limits your search results to entries that contain the specified information in the Details column.  The Details column normally contains data specific to your target, e.g., assigned permissions, before and after values, start and end dates.  This filter can be helpful when you are looking for a unique entry. | You discovered that a registry key was updated to *"242464"*. Now you want to investigate who made the change and what the value was before.  You can set the Details filter to *242464* to find this change faster. |
| Before\* | Limits your search results to entries that contain the specified before value in the Details column. | You are investigating an incident in which the SAM-account-name attribute was changed for an account in your Active Directory domain.  You can set the Before filter to the previous name (e.g., *John2000*) to find the new name faster. |
| After\* | Limits your search results to entries that contain the specified after value in the Details column. | You are investigating a security incident and want to know who enabled a local Administrator account on your Windows Server.  You can set the After filter to this account's current state (e.g., *Enabled*) to find this change faster. |
| Everywhere | Limits your search results to entries that contain the specified value in any column. | You are investigating a security incident. You have already identified the intruder (e.g., *BadActor*) and now you want to see all actions made by intruder's account or with it.  Since the intruder can be the actor (Who), the object (What), or can even show up in details, set the Everywhere filter to intruder's name. |

\* If you plan to audit an SQL Server for data changes and browse the results using 'Before' and 'After' filter values, make sure that the audited SQL database tables have a primary key (or a unique column). Otherwise, 'Before' and 'After' values will not be reported.

\* – If you plan to audit an SQL Server for data changes and browse the results using 'Before' and 'After' filter values, make sure that the audited SQL database tables have a primary key (or a unique column). Otherwise, 'Before' and 'After' values will not be reported.

## Search Conditions

When you apply filters at search, you can specify operators that should be used as conditions for data you want to retrieve and compare with the certain filter value. A condition can be, for example, Contains, Starts with, and so on.

[![](../static/img/Auditor/Images/Auditor/Search/AdvancedFilters_thumb_0_0.png)](../../../Resources/Images/Auditor/Search/AdvancedFilters.png)

The following operators can be used to specify search conditions:

| Operator | Description | Example |
| --- | --- | --- |
| Contains | This operator shows all entries that contain a value specified in the filter. | If you set the Who filter to contains *John*, you will get the following results: *Domain1\John*, *Domain1\Johnson*, *Domain2\Johnny*, *John@domain.com*. |
| Equals | This operator shows all entries with the exact value specified. Make sure to provide a full object name or path.  To apply this operator when adding filters in the Simple mode, provide a value in quotation marks (e.g., *"Domain1\John"*). | Use this operator if you want to get precise results, e.g., *\\FS\Share\NewPolicy.docx*. |
| Not equal to | This operator shows all entries except those with the exact value specified.  In the Search field in the Simple mode, this operator appears as not, e.g., Who not for the Who filter. | If you set the Who filter to not equal to  *Domain1\John*, you will exclude the exact user specified and find all changes performed by other users, e.g., *Domain1\Johnson, Domain2\John*. |
| Starts with | This operator shows all entries that start with the specified value. | If you set the Who filter to starts with *Domain1\John*, you will find all changes performed by *Domain1\John*, *Domain1\Johnson*, and *Domain1\Johnny*. |
| Ends with | This operator shows all entries that end with the exact specified value. | If you set the Who filter to ends with *John*, you will find all changes performed by *Domain1\John*, *Domain2\Dr.John*, *Domain3\John*. |
| Does not contain | This operator shows all entries except those that contain the specified value.  In the Search field in the Simple mode, this operator appears as not, e.g., Who not for the Who filter. | If you set the Who filter to does not contain *John*, you will exclude the following users: *Domain1\John*, *Domain2\Johnson*, and *Johnny@domain.com*. |
| In group | This operator relates to the Who filter. It instructs Netwrix Auditor to show only data for the accounts included in the specified group. | If you set the In group condition for Who filter to *Domain\Administrators*, only the data for the accounts included in that group will be displayed. |
| Not in group | This operator relates to the Who filter. It instructs Netwrix Auditor to show only data for the accounts not included in the specified group. | If you set the Not in group condition for Who filter to *Domain\Administrators*, only the data for the accounts not included in that group will be displayed. |

When you add a new search filter, the Contains operator is used by default.

To modify conditions for the selected filters, make sure you have switched to the Advanced search mode.

[![](../static/img/Auditor/Images/Auditor/Search/Filter/Advanced_thumb_0_0.png)](../../../Resources/Images/Auditor/Search/Filter/Advanced.png)

The image below represents the same search filters as they are shown in the Search field in the Simple mode.

[![](../static/img/Auditor/Images/Auditor/Search/Filter/AdvancedExample_thumb_0_0.png)](../../../Resources/Images/Auditor/Search/Filter/AdvancedExample.png)