---
title: "Operators"
sidebar_position: 704
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

# Operators

Review the table below to learn more about operators.

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