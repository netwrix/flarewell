---
title: "Configure Advanced Audit Policies"
sidebar_position: 1036
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

# Configure Advanced Audit Policies

You can configure advanced audit policies instead of basic domain policies to collect Logon Activity changes with more granularity.

Perform the following procedures:

* [Configuring security options](#Config_security_options "Configuring security options")
* [Configuring advanced audit policies](#Config_Advanced_Policies "Configuring advanced audit policies")

## Configuring security options

Setting up both basic and advanced audit policies may lead to incorrect audit reporting. To force basic audit policies to be ignored and prevent conflicts, enable the *Audit: Force audit policy subcategory settings* policy.

To do it, perform the following steps:

1. Open the **Group Policy Management** console on any domain controller in the target domain: navigate to Start \> Windows Administrative Tools (Windows Server 2016 and higher) or Administrative Tools (Windows 2012) **Group Policy Management.**
2. In the left pane, navigate to **Forest:  \> Domains \> \** **\> Domain Controllers**. Right-click the effective domain controllers policy (by default, it is the **Default Domain Controllers Policy**), and select **Edit** from the pop-up menu.
3. In the Group Policy Management Editor dialog, expand the Computer Configuration node on the left and navigate to Policies → Windows Settings → Security Settings → Local Policies → Security Options.
4. Locate the Audit: Force audit policy subcategory settings to override audit policy category settings and make sure that policy setting is set to *"Enabled"*.

   ![](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_AD_NLA_Audit_Force_WinServer2016.png)
5. Run the following command to update group policy: `gpupdate /force`

## Configuring advanced audit policies

1. Open the **Group Policy Management** console on any domain controller in the target domain: navigate to Start \> Windows Administrative Tools (Windows Server 2016 and higher) or Administrative Tools (Windows 2012) **Group Policy Management.**
2. In the left pane, navigate to **Forest:  \> Domains \> \** **\> Domain Controllers**. Right-click the effective domain controllers policy (by default, it is the **Default Domain Controllers Policy**), and select **Edit** from the pop-up menu.
3. In the Group Policy Management Editor dialog, expand the Computer Configuration node on the left and navigate to Policies → Windows Settings → Security Settings → Advanced Audit Policy Configuration → Audit Policies .
4. Configure the following audit policies.

   | Policy Subnode | Policy Name | Audit Events |
   | --- | --- | --- |
   | Account Logon | * Audit Kerberos Service Ticket Operations * Audit Kerberos Authentication Service * Audit Credential Validation | *"Success"* and *"Failure"* |
   | * Audit Other Account Logon Events | *"Success"* and *"Failure"* |
   | Logon/Logoff | * Audit Logoff * Audit Other Logon/Logoff Events | *"Success"* |
   | * Audit Logon | *"Success"* and *"Failure"* |
   | System | * Audit Security State Change | *"Success"* |

   ![](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_NLA_AdvPol2016.png)
5. Run the following command to update group policy: `gpupdate /force`