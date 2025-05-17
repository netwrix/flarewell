---
sidebar_position: 107
title: Configure Local Audit Policies
---

Filter: 

* All Files

Submit Search

# Configure Local Audit Policies

You can choose to configure local audit policies or advanced audit policies. See the [Configure Advanced Audit Policies](AdvancedPolicy "Configure Advanced Audit Policies") topic for additional information.

Follow the steps to configure local audit policies.

**Step 1 –** On the audited server, open the Local Security Policy snap-in: navigate to Start > Windows Administrative Tools > Local Security Policy.

**Step 2 –** Navigate to Security Settings > Local Policies > Audit Policy.

**Step 3 –** Configure the following audit policies.

| Policy Name | Audit Events |
| --- | --- |
| Audit account management | "Success" |
| Audit object access | "Success" |
| Audit policy change | "Success" |

Local audit policy is configured.

![Local Security Policy snap-in](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_WS_Local_Audit_Policies2016.png "Local Security Policy snap-in")