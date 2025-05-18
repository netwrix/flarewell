---
title: "Install Client via Group Policy"
sidebar_position: 673
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

# Install Client via Group Policy

The Netwrix Auditor client can be deployed on multiple computers via Group Policy. This can be helpful if you want to grant access to configuration and audit data to a significant number of employees and, therefore, have to run Netwrix Auditor installation on multiple computers.

If installing via Group Policy, make sure to deploy Netwrix Auditor client and Netwrix Auditor server on different machines. If both components are installed on the same machine, you may experience issues with future upgrades.

To run the Netwrix Auditor installation, you must be a member of the local Administrators group.

## Extract MSI File

1. Download the product installation package.
2. Open the command prompt: navigate to Start → Run and type "*cmd*".
3. Enter the following command to extract the msi file into %Temp% folder:

   `Netwrix_Auditor.exe -d%Temp%`

   where %Temp% can be replaced with any folder you want to extract the file to.
4. Navigate to this directory and locate Netwrix_Auditor_client.msi.

## Create and Distribute Installation Package

1. Create a shared folder that will be used for distributing the installation package.

   Make sure that the folder is accessible from computers where the Netwrix Auditor clients are going to be deployed. You must grant the Read permissions on this folder to these computer accounts.
2. Copy Netwrix_Auditor_client.msi to the shared folder.

## Create a Group Policy to Deploy Netwrix Auditor

It is recommended to create a dedicated organizational unit using Active Directory Users and Computers and add computers where you want to deploy the Netwrix Auditor client.

Follow the steps to create a Group Policy

**Step 1 –** Open the **Group Policy Management** console on any domain controller in the target domain: navigate to Start \> Windows Administrative Tools (Windows Server 2016 and higher) or Administrative Tools (Windows 2012) **Group Policy Management.**

**Step 2 –** In the left pane, navigate to **Forest:  → Domain →** **\, right-click \** and select **Create a GPO in this domain and Link it here**.

![](../static/img/Auditor/Images/Auditor/SilentGPInstall/WinServer2016_OU_GPO_for_Deploy.png)

**Step 3 –**  Right-click the newly created GPO and select **Edit** from the pop-up menu.

**Step 4 –** In the Group Policy Management Editor dialog, expand the **Computer Configuration** node on the left and navigate to **Policies → Software Settings → Software installation.**

**Step 5 –** In the right page, right-click and select New → Package.

**Step 6 –** In the dialog that opens, locate Netwrix_Auditor_client.msi and click Open.

**Step 7 –** In the Deploy Software dialog, select Advanced.

![](../static/img/Auditor/Images/Auditor/SilentGPInstall/Add_Msi.PNG)

**Step 8 –** In the Netwrix Auditor Properties dialog, select the Deployment tab and click Advanced.

**Step 9 –** In the Advanced Deployment Options dialog, select the Ignore language when deploying this package checkbox.

![](../static/img/Auditor/Images/Auditor/SilentGPInstall/WinServer2016_Advanced_Deployment_options.png)

**Step 10 –** Close the Netwrix Auditor Properties dialog.

**Step 11 –** Reboot computers where you want to deploy the Netwrix Auditor client.

The product will be automatically installed on computers affected by the newly created Group Policy after reboot.