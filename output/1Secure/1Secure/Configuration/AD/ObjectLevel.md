---
sidebar_position: 86
title: Configure Object-Level Auditing
---

Filter: 

* All Files

Submit Search

# Configure Object-Level Auditing

Object-level auditing must be configured for the **Domain** partition if you want to collect information on user activity in the domain. You must also enable object-level auditing for **Configuration**.

Auditing of the Configuration partition is enabled.

Follow the steps to configure object-level auditing for the Domain partition.

**Step 1 –** Open the **Active Directory Users and Computers** console on any domain controller in the target domain: navigate to **Start** > **Windows Administrative** Tools (Windows Server 2016 and higher) or Administrative Tools (Windows 2012) > **Active Directory Users and Computers**.

**Step 2 –** In the **Active Directory Users and Computers** dialog, click **View** in the main menu and ensure that the **Advanced Features** are enabled.

![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ADUC_AdvSecWinServer2016.png)

**Step 3 –** Right-click the **** node and select **Properties.** Select the **Security** tab and click **Advanced**. In the **Advanced Security Settings for ** dialog, select the **Auditing** tab.

![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ADUC_AdvAuditing_WinServer2016.png)

**Step 4 –** Do one of the following depending on the OS:

* On pre-Windows Server 2012 versions:

  1. Click **Add**. In the **Select user, Computer, Service account, or Group** dialog, type *"Everyone"* in the **Enter the object name to select** field.
  2. In the **Audit Entry** dialog that opens, set the *"Successful"* flag for all access entries except the following: *Full Control*, *List Contents*, *Read All Properties* and *Read Permissions*.

     ![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ObjectLevel_Entry2008.png)
  3. Make sure that the **Apply these auditing entries to objects and/or containers within this container only** checkbox is cleared. Also, make sure that the **Apply onto** parameter is set to *"This object and all descendant objects"*.
  4. Click **Ok**.
* On Windows Server 2012 and above

  1. Click **Add**. In the **Auditing Entry** dialog, click the **Select a principal** link.
  2. In the **Select user, Computer, Service account, or Group** dialog, type *"Everyone"* in the **Enter the object name to select** field.
  3. Set **Type** to *"Success"* and **Applies to** to *"This object and all descendant objects"*.
  4. Under **Permissions**, select all checkboxes except the following: *Full Control*, *List Contents*, *Read All Properties* and *Read Permissions*.
  5. Scroll to the bottom of the list and make sure that the **Only apply these auditing settings to objects and/or containers within this container** checkbox is cleared.

     ![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ObjectLevel_WinServer2016.png)
  6. Click **Ok**.

Follow the steps to enable object-level auditing for the Configuration partition.

To perform this procedure, you will need the [ADSI Edit](http://technet.microsoft.com/en-us/library/cc773354(v=ws.10).aspx "ADSI Edit") utility. In Windows Server 2008 and above, this component is installed together with the AD DS role, or it can be downloaded and installed along with Remote Server Administration Tools. See the [Install ADSI Edit](ADSI "Install ADSI Edit") topic for additional information on how to install the ADSI Edit utility.

**Step 1 –** On any domain controller in the target domain, navigate to Start>Windows Administrative Tools (Windows Server 2016 and higher) or Administrative Tools **(Windows 2012)** **> ADSI Edit**.

**Step 2 –** Right-click the **ADSI Edit** node and select **Connect To**. In the **Connection Settings** dialog, enable **Select a well-known Naming Context** and select **Configuration** from the drop-down list.

![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ADSI_ConnectionWinServer2016.png)

**Step 3 –** Expand the **Configuration ** node. Right-click the **CN=Configuration, DC=,DC=…** node and select **Properties.**

**Step 4 –** In the **CN=Configuration, DC=, DC= Properties** dialog select the **Security** tab and click **Advanced**. In the **Advanced Security Settings for Configuration** dialog, open the **Auditing** tab.

**Step 5 –**  Do one of the following depending on the OS:

* On pre-Windows Server 2012 versions:

  1. Click **Add**. In the **Select user, Computer, Service account, or Group** dialog, type *"Everyone"* in the **Enter the object name to select** field.
  2. In the **Audit Entry** dialog that opens, set the *"Successful"* flag for all access entries except the following: *Full Control*, *List Contents*, *Read All Properties* and *Read Permissions*.

     ![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ObjectLevel_Entry2008.png)
  3. Make sure that the **Apply these auditing entries to objects and/or containers within this container only** checkbox is cleared. Also, make sure that the **Apply onto** parameter is set to *"This object and all descendant objects"*.
  4. Click **Ok**.
* On Windows Server 2012 and above

  1. Click **Add**. In the **Auditing Entry** dialog, click the **Select a principal** link.
  2. In the **Select user, Computer, Service account, or Group** dialog, type *"Everyone"* in the **Enter the object name to select** field.
  3. Set **Type** to *"Success"* and **Applies to** to *"This object and all descendant objects"*.
  4. Under **Permissions**, select all checkboxes except the following: *Full Control*, *List Contents*, *Read All Properties* and *Read Permissions*.
  5. Scroll to the bottom of the list and make sure that the **Only apply these auditing settings to objects and/or containers within this container** checkbox is cleared.

     ![](../../../Resources/Images/Auditor/ManualConfig/ManualConfig_ObjectLevel_WinServer2016.png)
  6. Click **Ok**.