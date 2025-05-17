---
sidebar_position: 88
title: 'Active Directory: manual configuration'
---

Filter: 

* All Files

Submit Search

# Active Directory: manual configuration

To configure your domain for monitoring manually, you will need:

* **Group Policy Management Console** — if you plan to perform configuration steps from a domain controller

  -OR-
* **ADSI Edit** — if you plan to perform configuration steps from a server other than domain controller

If these tools are not installed, refer to the related topics:

* [Install ADSI Edit](ADSI "Install ADSI Edit")
* [Group Policy Management Console](GroupPolicyManagementConsole "Group Policy Management Console")

Take the following configuration steps:

**Step 1 –**  Configure effective domain controllers policy (by default, Default Domain Controllers Policy). See [Configure Basic Domain Audit Policies](DomainAuditPolicies "Configure Basic Domain Audit Policies")
or
[Configure Advanced Audit Policies](AdvancedPolicy "Configure Advanced Audit Policies") for details.

**Step 2 –** [Configure Object-Level Auditing](ObjectLevel "Configure Object-Level Auditing")

**Step 3 –** Adjust Security Event Log Size and Retention Settings

**Step 4 –** If you have an on-premises Exchange server in your Active Directory domain, consider that some changes to AD can be made via that Exchange server. To be able to audit and report who made those changes, you should [Configure Exchange Administrator Audit Logging Settings](../../Admin/DataCollection/ActiveDirectory/AuditLogging "Configure Exchange Administrator Audit Logging Settings")

Also, remember to do the following for AD auditing:

**Step 1 –** Configure Data Collecting Account, as described in [Active Directory Auditing](../../Admin/DataCollection/ActiveDirectory/ActiveDirectoryAuditing "Active Directory Auditing")

**Step 2 –** Configure required protocols and ports, as described in [Protocols and Ports Required for Monitoring Active Directory, Exchange, and Group Policy](ProtocolsAndPorts "Protocols and Ports Required for Monitoring Active Directory, Exchange, and Group Policy") topic.

**Step 3 –** [Enable Secondary Logon Service](SecondaryLogonService "Enable Secondary Logon Service") on the computer where Netwrix Cloud Agent resides.