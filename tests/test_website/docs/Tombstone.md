---
title: "Adjust Active Directory Tombstone Lifetime (optional)"
sidebar_position: 994
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

# Adjust Active Directory Tombstone Lifetime (optional)

You can restore deleted Active Directory objects and their attributes using the Netwrix Auditor Object Restore for Active Directory tool shipped with Netwrix Auditor. The tool finds the information on deleted objects in the product snapshots (this data is stored in the Long-Term Archive, a local file-based storage of audit data) and AD tombstones.

To be able to restore deleted Active Directory objects longer, increase the **Active Directory tombstone lifetime** property (set by default to 180 days). Netwrix recommends setting it to 2 years (**730 days**). You can specify any number of days, but a selected value should not exceed the Long-Term Archive retention period.

Take into consideration that increasing tombstone lifetime may affect Active Directory performance and operability.

To perform this procedure, you will need the [ADSI Edit](`http://technet.microsoft.com/en-us/library/cc773354(v=ws.10`).aspx) utility.utility.

Follow the steps to change the tombstone lifetime attribute.

**Step 1 –** On any domain controller in the target domain, navigate to Start \> Windows Administrative Tools **\> ADSI Edit**.

**Step 2 –** Right-click the **ADSI Edit** node and select **Connect To**. In the **Connection Settings** dialog, enable **Select a well-known Naming Context** and select **Configuration** from the drop-down list.

![](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_ADSI_ConnectionWinServer2016.png)

**Step 3 –** Navigate to **Configuration \,DC= → CN=Services → CN=Windows NT → CN=Directory Service**. Right-click it and select **Properties** from the pop-up menu.

**Step 4 –** In the **CN=Directory Service Properties** dialog, locate the **tombstoneLifetime** attribute in the **Attribute Editor** tab.

![](../static/img/Auditor/Images/Auditor/ManualConfig/ManualConfig_ADSI_Tombstone_WinServer2016.png)

**Step 5 –** Click **Edit**. Set the value to *"730"* (which equals 2 years).