---
title: "Active Directory: Manual Configuration"
sidebar_position: 993
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

# Active Directory: Manual Configuration

To configure your domain for monitoring manually, you will need:

* Group Policy Management Console — Required if you plan to perform configuration steps from a domain controller

  -OR-
* ADSI Edit — Required if you plan to perform configuration steps from a server other than domain controller

**NOTE:** If these tools are not installed, refer to the following Microsoft articles:

* [Group Policy Management Console](`https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn265969(v=ws.11`) "Group Policy Management Console")
* [ADSI Edit](`https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc773354(v=ws.10`)?redirectedfrom=MSDN "ADSI Edit")

Follow the steps to configure your domain for monitoring.

**Step 1 –** Configure effective domain controllers policy (by default, Default Domain Controllers Policy). See the [Configure Basic Domain Audit Policies](BasicPolicy.htm "Configure Basic Domain Audit Policies")
or
[Configure Advanced Audit Policies](AdvancedPolicy.htm "Configure Advanced Audit Policies") topics for additional information.

**Step 2 –** Configure object-level auditing. See the [Configure Object-Level Auditing](ObjectLevel.htm "Configure Object-Level Auditing") topic for additional information.

**Step 3 –** Adjust the security event log size and retention settings. See the [Adjust Security Event Log Size and Retention](SecurityLog.htm "Adjust Security Event Log Size and Retention")topic for additional information.

**Step 4 –** If you have an on-premises Exchange server in your Active Directory domain, consider that some changes to AD can be made via that Exchange server. To be able to audit and report who made those changes, perform configuration steps as described in the [Exchange Administrator Audit Logging Settings](../Exchange/AuditLog.htm "Configure Exchange Administrator Audit Logging Settings") topic.

Optionally, you can adjust the Active Directory Tombstone Lifetime. See the [Adjust Active Directory Tombstone Lifetime (optional)](Tombstone.htm "Adjust Active Directory Tombstone Lifetime (optional)") topic for additional information.

Also, remember to perform the following steps for AD auditing:

**Step 1 –** Configure Data Collecting Account, as described in the [Additional Configuration to Review Changes Made via Exchange Server](Additional.htm "Additional Configuration to Review Changes Made via Exchange Server") topic.

**Step 2 –** Configure required protocols and ports, as described in the [Active Directory Ports](Ports.htm "Active Directory Ports") topic.

**Step 3 –** Enable Secondary Logon Service on the computer where Netwrix Auditor Server resides.

## Enable Secondary Logon Service

Follow the steps to Enable Secondary Logon Service.

**Step 1 –** On the computer where Auditor Server resides, navigate to Start \> Windows Administrative Tools \> **Services**.

**Step 2 –** In the **Services** dialog, locate the **Secondary Logon** service.

**Step 3 –** Right-click the service and on the **General** tab make sure that **Startup type** for this service is other than *Disabled*. The startup type can be either *Automatic* or *Manual*.