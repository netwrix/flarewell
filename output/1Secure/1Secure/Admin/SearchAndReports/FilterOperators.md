---
sidebar_position: 47
title: Filter Operators
---

Filter: 

* All Files

Submit Search

# Filter Operators

When applying filters at search, you can specify operators that should be used as conditions for data you want to retrieve and compare with the certain filter value. Examples of conditions include Contains, Starts with, etc.

![](../../../Resources/Images/1Secure/Search_SearchResults.png)

The following operators can be used to specify search conditions:

| Operator | Description | Example |
| --- | --- | --- |
| Contains | This operator shows all entries that contain a value specified in the filter. | If you set the Who filter to contains *John*, you will get the following results: *Domain1\John*, *Domain1\Johnson*, *Domain2\Johnny*, *John@domain.com*. |
| Equals | This operator shows all entries with the exact value specified. Make sure to provide a full object name or path.  To apply this operator when adding filters in the Simple mode, provide a value in quotation marks (e.g., *"Domain1\John"*). | Use this operator if you want to get precise results, e.g., *\\FS\Share\NewPolicy.docx*. |
| Less than | This search shows all entries with the period less than the exact value specified. The operator is used with the "When" filter. | Specify the date and time, so that the search provides all the records which are less than this value. |
| Less than or equals | This search shows all entries with the period, which equals or less than exact value specified. The operator is used with the "When" filter. | Specify the date and time, so that the search provides all the records which are less than or equal to this value. |
| Greater than | This search shows all entries with the period which is greater than the exact value specified. The operator is used with the "When" filter. | Specify the date and time, so that the search provides all the records which are greater than this value. |
| Greater than or equals | This search shows all entries, which are equal or greater than the exact value specified. The operator is used with the "When" filter. | Specify the date and time, so that the search provides all the records which are greater than or equal to this value. |
| Not equal to | This operator shows all entries except those with the exact value specified.  In the Search field in the Simple mode, this operator appears as not, e.g., Who not for the Who filter. | If you set the Who filter to not equal to  *Domain1\John*, you will exclude the exact user specified and find all changes performed by other users, e.g., *Domain1\Johnson, Domain2\John*. |
| Starts with | This operator shows all entries that start with the specified value. | If you set the Who filter to starts with *Domain1\John*, you will find all changes performed by *Domain1\John*, *Domain1\Johnson*, and *Domain1\Johnny*. |
| Ends with | This operator shows all entries that end with the exact specified value. | If you set the Who filter to ends with *John*, you will find all changes performed by *Domain1\John*, *Domain2\Dr.John*, *Domain3\John*. |
| Does not contain | This operator shows all entries except those that contain the specified value.  In the Search field in the Simple mode, this operator appears as not, e.g., Who not for the Who filter. | If you set the Who filter to does not contain *John*, you will exclude the following users: *Domain1\John*, *Domain2\Johnson*, and *Johnny@domain.com*. |
| Exists | The search shows all the entries that exist for the specified values.  This operator is specific only for the Property changes filter. | If you set the Property Changes filter to **Exists**, the search will display the activity records with this property change. |
| Does not exist | The search shows all the entries except for the one you specified in the Does not exist value.  This operator is specific only for the Property changes filter. | If you set the Property Changes filter to **Does not exist**, the search will display all the activity records except for the one you specified in this filter. |