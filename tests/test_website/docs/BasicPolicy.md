---
title: "Configure Basic Domain Audit Policies"
sidebar_position: 1033
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

# Configure Basic Domain Audit Policies

Basic local audit policies allow tracking changes to user accounts and groups and identifying originating workstations. You can configure advanced audit policies for the same purpose too. See the [Configure Advanced Audit Policies](AdvancedPolicy.htm "Configure Advanced Audit Policies") topic for additional information.

1. Open the **Group Policy Management** console on any domain controller in the target domain: navigate to Start \> Windows Administrative Tools (Windows Server 2016 and higher) or Administrative Tools (Windows 2012) **Group Policy Management.**
2. In the left pane, navigate to **Forest:  \> Domains \> \** **\> Domain Controllers**. Right-click the effective domain controllers policy (by default, it is the **Default Domain Controllers Policy**), and select **Edit** from the pop-up menu.
3. In the **Group Policy Management Editor** dialog, expand the **Computer Configuration** node on the left and navigate to **Policies → Windows Settings → Security Settings → Local Policies → Audit Policy.**
4. Configure the following audit policies.

   | Policy | Audit Events |
   | --- | --- |
   | Audit logon events | *"Success"* and *"Failure"* |
   | Audit account logon events | *"Success"* and *"Failure"* |
   | Audit system events | *"Success"* |

   ![](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_NLA_AuditPolicies2016.png)
5. Run the following command to update group policy: `gpupdate /force`