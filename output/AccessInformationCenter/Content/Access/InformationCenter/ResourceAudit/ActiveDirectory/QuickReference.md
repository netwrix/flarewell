---
sidebar_position: 58
title: Active Directory Reports Quick Reference
---

# Active Directory Reports Quick Reference

The following Active Directory reports are available for selection within the Resources pane.

## Active Directory Node Reports

The following reports are available at the Active Directory node level:

| Report | Description |
| --- | --- |
| [Domain Summary Report](DomainSummary "Domain Summary Report") | Provides a top-level view of domains that have been scanned. |
| [Exceptions Report](Exceptions "Exceptions Report") | Provides a list of exceptions that were found across the targeted Active Directory environment. This report includes a Details table. |

## Active Directory > Domain Level Reports

The following reports are available at the domain level:

| Report | Description |
| --- | --- |
| Activity Report | Displayed but not populated at the domain level. |
| [Exceptions Report](Domain/Exceptions "Exceptions Report") | Provides a list of exceptions found on the selected domain. This report includes a Details table. |
| [Membership Changes Report](Domain/MembershipChanges "Membership Changes Report") | Provides a list of groups that had membership changes on the selected domain during the specified date range. |
| [Principal Attribute Changes Report](Domain/PrincipalAttributeChanges "Principal Attribute Changes Report") | Provides change event information by trustee on the selected domain during the specified date range. |

## Active Directory > Domain > Domain Object Level Report

The following reports are available at the domain object level:

| Report | Description |
| --- | --- |
| [Access Report](DomainObject/Access "Access Report") | Provides information on the level of access trustees have at the domain object level. This report includes a Permission Source table. |
| [Permissions Report](DomainObject/Permissions "Permissions Report") | Provides the trustees that have rights on the selected Active Directory object. |

## Active Directory > Domain > Exceptions Node Report

The following report is available at the Exceptions node level:

| Report | Description |
| --- | --- |
| [Exceptions Report](Exceptions/Exceptions "Exceptions Report") | Provides the trustees that have rights on the selected Active Directory object. This report includes a Details table. |

## Active Directory > Domain > Exceptions > Exception Type Level Report

The following report is available at the exception type level:

| Report | Description |
| --- | --- |
| [Exceptions by Type Report](Exceptions/ExceptionsByType "Exceptions by Type Report") | Provides details on the selected exception type. An exception is defined as a problem or risk to Active Directory security. Each of these reports includes a Member Of table. Certain exception types also include a Members table. |