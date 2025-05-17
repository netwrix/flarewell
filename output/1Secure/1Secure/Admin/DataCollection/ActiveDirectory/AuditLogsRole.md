---
sidebar_position: 66
title: Assigning Management Roles
---

Filter: 

* All Files

Submit Search

# Assigning Management Roles

Perform this procedure only if the account selected for data collection is not a member of the **Organization Management** or the **Records Management** group.

1. On the computer where Microsoft Exchange 2019, 2016, 2013 or 2010 is installed, open the **Exchange Management Shell** under an account that belongs to the **Organization Management** group.
2. Use the following syntax to assign the required management role to a user:

   `New-ManagementRoleAssignment -Name  -User  -Role `

   For example:

   `New-ManagementRoleAssignment -Name "AuditLogsNetwrixRole" -User Corp\jsmith -Role "Audit Logs"`

   In this example, the user CORP\jsmith has been assigned the **Audit Logs** role.