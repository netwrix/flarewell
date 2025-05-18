---
title: "Configure Local Audit Policies"
sidebar_position: 1040
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

# Configure Local Audit Policies

Local audit policies must be configured on the target servers to get the "Who" and "When" values for the changes to the following monitored system components:

* Audit policies
* File shares
* Hardware and system drivers
* General computer settings
* Local users and groups
* Services
* Scheduled tasks
* Windows registry
* Removable media

You can also configure advanced audit policies for same purpose. See the [Configure Advanced Audit Policies](AdvancedPolicy.htm "Configure Advanced Audit Policies") topic for more information.

## Manual Configuration

While there are several methods to configure local audit policies, this topic covers just one of them: how to configure policies locally with the Local Security Policy snap-in. To apply settings to the whole domain, use the Group Policy but consider the possible impact on your environment.

Follow the steps to configure local audit policies.

**Step 1 –** On the audited server, open the Local Security Policy snap-in: navigate to Start \> Windows Administrative Tools \> Local Security Policy.

**Step 2 –** Navigate to Security Settings \> Local Policies \> Audit Policy.

**Step 3 –** Configure the following audit policies.

| Policy Name | Audit Events |
| --- | --- |
| Audit account management | "Success" |
| Audit object access | "Success" |
| Audit policy change | "Success" |

Local audit policy is configured.

![Local Security Policy snap-in](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_WS_Local_Audit_Policies2016.png "Local Security Policy snap-in")