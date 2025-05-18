---
title: "Configure Virtual Appliance"
sidebar_position: 969
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

# Configure Virtual Appliance

Perform the following steps to configure your virtual appliance:

**Step 1 –** For **Windows Server**, the EULA will be displayed in the License terms page; read and accept the agreement.

**Step 2 –** Next, specify a password for the built-in administrator account. Then re-enter your password. Click Finish.

**Step 3 –** Log in to the virtual machine.

**Step 4 –** The Windows PowerShell opens and automatically runs the script. Press any key to read the license agreement and then press `Y` to accept it.

**Step 5 –**  Then you will be prompted to configure the virtual machine. Press Enter to start.

| Step | Description |
| --- | --- |
| Rename virtual machine | Specify a new name for the virtual machine (e.g., *`NA-Server`*).  The computer name must be properly formatted. It may contain letters (a-z, A-Z), numbers (0-9), and hyphens (-), but no spaces and periods (.). The name may not consist entirely of digits and may not be longer than 15 characters. |
| Add additional input languages | Select `Y` if you want to specify additional input languages.  Select `N` to proceed with English. |
| Configure network | * Select `Y` to use DHCP server to configure network settings automatically. * Select `N` to configure required parameters manually. In this case, you will be prompted to set up IP settings manually. |
| Join computer to the domain or workgroup | **To join a domain**  Select `Y`. Specify the fully qualified domain name to join (e.g., `corp.local`). Then specify domain administrator name and password.  For your convenience, the account specified will be added to the local Administrators group and set as account for collecting data from the target systems.  Domain Users group will be removed from the local Users group after the machine with the appliance joins the domain.  The script is starting to test your domain controller: by NETBIOS name first, then by DNS name and finally, using an IP address. If at least one of the tests is successful, the computer will be added to a domain. In case of failure, you will be prompted to do one of the following:   * Re-try to joint to the selected domain. In this case, the script uses the DNS name of your domain controller.  The name must be resolved. * Continue with Workgroup. See the procedure below on how to join the computer to a workgroup. * Cancel and **Return to Main Menu**. Select if you want to cancel the domain join and re-configure the machine. Press Enter and repeat menu section. You will return to step 5.   **To join a workgroup**  Select `N`. Specify the local administrator name and credentials.  For your convenience, the account specified will be set as account for collecting data from the target systems.  Netwrix Auditor is unable to work in a workgroup. Please confirm if you want to proceed. Otherwise, you will not be able to run reviews on data collected by Auditor. See the [Access Reviews](../../AccessReviews.htm "Access Reviews") topic for additional information about integration with Access Reviews. |
| Configure SQL Server | The shell script automatically configures SQL Server instance. The sysadmin server role on SQL Server instance is granted automatically to the BUILTIN\Administrators group. |

In the example below, review how the shell script configures the new VM:

![](../static/img/Auditor/Images/Auditor/VirtualApplianceIssues/Appliance_Script.PNG)

**Step 6 –** 
When the script execution completes, you will be prompted to reboot the virtual machine for the changes to take effect.

**Step 7 –** After reboot, log in to the virtual machine using the domain administrator credentials (for appliances joined to domain) or local administrator credentials (for appliances joined to workgroup).

For the first time, Auditor Client starts automatically. Later, you can always run it from the Start menu or launch it by double-clicking the Auditor shortcut on the desktop.

Do not close the Virtual Appliance Configuration window until the product configuration completes.

## What Is Next

Now you can evaluate Auditor functionality. Review the table below for more information.

| To... | Run... | Get more info |
| --- | --- | --- |
| * See a list of audit settings * See a list of rights and permissions required for data collecting account | — | * [Supported Data Sources](../../Requirements/SupportedDataSources.htm "Supported Data Sources") * [Data Collecting Account](../../Admin/MonitoringPlans/DataAccounts.htm "Data Collecting Account") |
| * Create a monitoring plan * Review data collection status * Configure the Long-Term Archive and the Audit Database settings * Assign roles and delegate control | Auditor Client | * [Monitoring Plans](../../Admin/MonitoringPlans/Overview.htm "Monitoring Plans") * [Netwrix Auditor Settings](../../Admin/Settings/Overview.htm "Settings") * [Role-Based Access and Delegation](../../Admin/MonitoringPlans/Delegation.htm "Role-based access and delegation") |
| * Browse data with interactive search * Review diagrams * Generate reports * Configure report subscriptions * Create alerts | Auditor Client | * [Reports](../../Admin/Reports/Overview.htm "Reports and Report Packs") * [Subscriptions](../../Admin/Subscriptions/Overview.htm "Subscriptions") * [Alerts](../../Admin/AlertSettings/Overview.htm "Alerts") |
| See the data collected by Auditor | Auditor Client | * [Access Reviews](../../AccessReviews.htm "Access Reviews") |

**NOTE:** If any errors occur, please contact [Netwrix technical support](`https://www.netwrix.com/support`).