---
title: "Assign Permission To Read the Registry Key"
sidebar_position: 988
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

# Assign Permission To Read the Registry Key

This permission is required only if the account selected for data collection is not a member of the Domain Admins group. This permission should be assigned on each domain controller in the audited domain, so if your domain contains multiple domain controllers, it is recommended to assign permissions through Group Policy, or automatically using [Audit Configuration Assistant](../../Tools/AuditConfigurationAssistant.htm "Audit Configuration Assistant"). To assign permissions manually, use the Registry Editor snap-in or the Group Policy Management console. See the [Permissions for Group Policy Auditing](../GroupPolicy/Permissions.htm "Permissions for Group Policy Auditing")topic for additional information.

## Assign Permission Via the Registry Editor Snap-in

Follow the steps to assign permission via the Registry Editor snap-in.

**Step 1 –** On your target server, open Registry Editor: navigate to **Start \> Run** and type *"regedit"*.

**Step 2 –** In the left pane, navigate to *HKEY_LOCAL_MACHINE\SYSTEM\CurrentControl Set\Services\EventLog\Security*.

**Step 3 –** Right-click the **Security** node and select **Permissions** from the pop-up menu.

**Step 4 –** Click **Add** and enter the name of the user that you want to grant permissions to.

**Step 5 –** Check **Allow** next to the **Read** permission.

**Step 6 –** For auditing Logon Activity, you also need to assign the Read permission to the *HKEY_LOCAL_MACHINE\SECURITY\Policy\PolAdtEv* registry key.

## Assign Permission Using the Group Policy Management Console

Follow the steps to assign permission using the Group Policy Management console.

**Step 1 –** Open the Group Policy Management console on any domain controller in the target domain: navigate to Start \> Windows Administrative Tools (Windows Server 2016/2019) or Administrative Tools (Windows 2012 R2 and below) \> Group Policy Management.

**Step 2 –** In the left pane, navigate to Forest:  \> Domains \>  \> Domain Controllers. Right-click the effective domain controllers policy (by default, it is the *Default Domain Controllers Policy*), and select Edit .

**Step 3 –** In the Group Policy Management Editor dialog, expand the Computer Configuration node on the left and navigate to Policies \> Windows Settings \> Security Settings \> Registry.

**Step 4 –** Right-click in the pane and select Add Key.

**Step 5 –** Navigate to `HKEY_LOCAL_MACHINE\SECURITY\Policy\PolAdtEv` and click OK.

**Step 6 –** Click Add and enter the name of the user that you want to grant permissions to and press Enter.

**Step 7 –** Check Allow next to the *Read* permission and click OK

**Step 8 –** In the pop-up window, select Propagate inheritable permissions to all subkeys and click OK.

**Step 9 –** Repeat the steps 4-8 for keys below:

* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurePipeServers\winreg`;
* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\EventLog\Security`.

**Step 10 –** Close Group Policy Management console.

**Step 11 –** Navigate to Start \> Run and type `cmd`. Input the `gpupdate /force` command and press Enter. The group policy will be updated.

**Step 12 –** Type `repadmin/syncall` command and press Enter for replicate GPO changes to other domain controllers.

**Step 13 –** Ensure that new GPO settings were applied to the domain controllers.