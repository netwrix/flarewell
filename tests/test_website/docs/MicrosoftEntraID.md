---
title: "Microsoft Entra ID State-In-Time Reports"
sidebar_position: 923
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

# Microsoft Entra ID State-In-Time Reports

To instruct Netwrix Auditor to collect data needed for the report, make sure that Collect data for state-in-time reports option is selected in the corresponding monitoring plan properties. See [Create a New Monitoring Plan](../../../MonitoringPlans/Create.htm "Create a New Plan").

**NOTE:** For Microsoft Entra ID, only the current date snapshot can be used for Reports.

## User Accounts - Attributes

The report shows specific AD attributes for the Microsoft Entra ID (formerly Azure AD) accounts that meet the specified filtering criteria. Use this report to discover Microsoft Entra ID accounts with settings that violate company policies or applicable compliance standards.

For this report to function properly, you must enable the Collect data for state-in-time reports option for the data source in the monitoring plan settings. See the [Settings for Data Collection](../../../MonitoringPlans/Create.htm#Settings "Settings for Data Collection") [topic for more information.](../../../../Solutions/ManagePlans/Accounts)

### Tips to Work with Report

1. Set desired filters in the report header. See the [Filters](#Filters "Filters") topic for more information.
2. Select as many Accounts details to show as needed. Selected details are shown in the table view for each account that comply filtering criteria.
3. Filter on Sort by to bring important accounts' data to front.
4. Add filters by specific attribute values to narrow your report scope. In this case, the report shows only accounts that contains these values. See the [Reported Attributes](#Reported "Reported Attributes") topic for more information.
5. The report is limited by 2000 records. To view all, create subscription to the report. The subscription (email attachment or file uploaded to a file share) will contain complete data.
6. If you have more than 2000 entities within the report scope, sorting might work incorrectly. Apply filters to narrow your report scope.

### Filters

You can narrow your reporting scope using multiple filters. Review the full list of available filters and values:

* Monitoring plan — name of the monitoring plan set to collect data from the AD domain you need.
* Time zone — select you time zone.
* Item — name of the item within your monitoring plan.
* Sort by — list of available sorting parameters.
* Account enabled — select whether you want to see disabled accounts or not.
* Department — provide the name of the department if needed.
* Attribute/Value — list of available AD attributes with the ability to provide specific value.

### Reported Data

For the account(s) you selected using filters, the summary section includes:

* Total account count — total number of accounts that meet selected filtering criteria.

* Enabled accounts —total number of enabled accounts that meet selected filtering criteria.
* Disabled accounts —total number of disabled accounts that meet selected filtering criteria.

### Reported Attributes

The following account attributes are reported:

| Attribute (display name in report) | Microsoft Entra ID attribute mapping | Possible values | Description |
| --- | --- | --- | --- |
| Account enabled | accountEnabled | Yes/No | Specifies, whether the user account is enabled or disabled: the "true" value indicates that the account is enabled. |
| Change password on next sign in | passwordProfile | Yes/No | Specifies the password profile for a user. The password in the profile must satisfy the minimum requirements as specified by the passwordPolicies property. By default, a strong password is required. |
| Change password on next sign in with MFA | passwordProfile | Yes/No | Specifies the password profile for the user. The password in the profile must satisfy the minimum requirements as specified by the passwordPolicies property. By default, a strong password is required. |
| City | city | Example: "*London*" | The city where a user is located. Maximum length 128. |
| Cloud-only | onPremisesSyncEnabled | Yes/No | true if this object is synced from any on- premises directory; false if this object was originally synced from any on- premises directory but is no longer synced; null if this object has never been synced from any on-premises directory (default). |
| Country | country | Example: "*US*" | The country/region in which the user is located. Example: "US" or "UK". Maximum length 128. |
| Creation date | createdDateTime | 1/21/2021 4:08:00 PM | The created date of the user object. |
| Department | department | Example: "*Accounting and Finance*" | The name for the department in which the user works. Maximum length is 64 characters. |
| Display name | displayName | Example: "*John Smith*" | The name displayed in the address book for the user. This is usually the combination of the user's first name, middle initial and last name. This property is required when a user is created and it cannot be cleared during updates. Maximum length is 256 characters. |
| First name | givenName | Example: "*John*" | The given name (first name) of the user. Maximum length is 64 characters. |
| Is licensed | – | – | – |
| Last DirSync time | onPremisesLastSyncDateTime | Example: *3/20/2021 2:13:00 PM* | M Indicates the last time at which the object was synchronized with the on-premises directory; for example: "2013- 02- 16T03:04:54Z". The Timestamp type represents date and time information using ISO 8601 format and is always in UTC time. |
| Last name | surname | Example: "*Smith*" | The user's surname (family name or last name). Maximum length is 64 characters. |
| Licenses | – | Example: *OFFICE 365 E1* | – |
| Manager | manager | Example: "*James**Williams*" | The user or contact that is this user's manager. |
| Manager email | – | Example: *JWilliams@gmail.com* | – |
| Office | physicalDeliveryOfficeName (officeLocation) | Example: *1068* | The office location in the user's place of business. Maximum length is 128 characters. |
| Password last change | lastPasswordChangeDateTime | Example: *4/6/2021 6:17:00 PM* | The time when this Microsoft Entra ID Plans user last changed their password. The date and time information uses ISO 8601 format and is always in UTC time. |
| Password never expires | passwordPolicies | Yes/No | Specifies password policies for the user. This value is an enumeration with one possible value being “DisableStrongPassword”, which allows weaker passwords than the default policy to be specified. “DisablePasswordExpiration” can also be specified. The two may be specified together; for example: "DisablePasswordExpiration, DisableStrongPassword". |
| Phone number | businessPhones | Example: *+1-202-555-155* | The telephone numbers for the user.  Although this is a string collection, only one number can be set for this property. |
| Role membership | – | Example: "*Exchange Service Administrator, Company Administrator*" | – |
| Sign in names | identities | *Example: "user_company.com#EXT#@officenwxqc.onmicrosoft.com"* | Represents the identities that can be used to sign into this user account. An identity can be provided by Microsoft (also known as a local account), by organizations, or by social identity providers such as Facebook, Google, and Microsoft, and tied to a user account. May contain multiple items with the same signInType value. `https://docs.microsoft.com/en-` us/graph/api/resources/objectid entity?view=graph-rest-1.0 |
| Strong password required | passwordPolicies | Yes/No | Specifies password policies for the user. This value is an enumeration with one possible value being “DisableStrongPassword”, which allows weaker passwords than the default policy to be specified. “DisablePasswordExpiration” can also be specified. The two may be specified together; for example: "DisablePasswordExpiration, DisableStrongPassword". |
| Title | jobTitle | Example: "*Business development manager*" | The user's job title. Max length is 128. |
| User principal name | userPrincipalName | Example: "*user_company.com#EXT#@officenwxqc.onmicrosoft.com*" | The user principal name (UPN) of wxq the user. The UPN is an Internet- style login name for the user based on the Internet standard RFC 822. By convention, this should map to the user's email name. The general format is alias@domain, where the domain must be present in the tenant's collection of verified domains. This property is required when a user is created. The verified domains for the tenant can be accessed from the verifiedDomains property of organization. NOTE: While this property can contain accent characters, they can cause access issues to first-party applications for the user. |
| User type | userType | Example: "*Member*" | A string value that can be used to classify user types in your directory, such as "Member" and "Guest". |