---
title: "Software Requirements"
sidebar_position: 684
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

# Software Requirements

The table below lists the software requirements for the Auditor installation:

| Component | Full installation (both Auditor Server and Client) | Client installation (client only) |
| --- | --- | --- |
| Operating system (English-only) | Windows Server OS:   * Windows Server 2025 * Windows Server 2022  * Windows Server 2019 * Windows Server 2016 * Windows Server 2012 R2   Windows Desktop OS (64-bit):   * Windows 11 * Windows 10 | Windows Server OS:   * Windows Server 2025 * Windows Server 2022 * Windows Server 2019 * Windows Server 2016 * Windows Server 2012 R2   Windows Desktop OS (32 and 64-bit):   * Windows 11 * Windows 10 |
| .NET Framework | * .NET Framework 4.8 and above.  See the following Microsoft article for additional information about .Net Framework installer redistributable: [Microsoft .NET Framework 4.8 offline installer for Windows.](`https://support.microsoft.com/en-us/topic/microsoft-net-framework-4-8-offline-installer-for-windows-9d23f658-3b97-68ab-d013-aa3c3e7495e0` "Microsoft .NET Framework 4.8 offline installer for Windows") | — |
| Installer | * Windows Installer 3.1 and above   See the following Microsoft article for additional information about Windows Installer redistributable: [Windows Installer 3.1 v2 (3.1.4000.2435) is available](`https://support.microsoft.com/en-us/topic/windows-installer-3-1-v2-3-1-4000-2435-is-available-e3978d9b-5fbf-bfec-71b9-1a463290065a` "Windows Installer 3.1 v2 (3.1.4000.2435) is available") | * Windows Installer 3.1 and above   See the following Microsoft article for additional information about Windows Installer redistributable: [Windows Installer 3.1 v2 (3.1.4000.2435) is available](`https://support.microsoft.com/en-us/topic/windows-installer-3-1-v2-3-1-4000-2435-is-available-e3978d9b-5fbf-bfec-71b9-1a463290065a` "Windows Installer 3.1 v2 (3.1.4000.2435) is available") |

## Other Components

To monitor your data sources, you will need to install additional software components on Auditor Server, in the monitored environment, or in both locations.

| Data source | Components |
| --- | --- |
| * Active Directory * Exchange Server * Exchange Online | *On the computer where* Auditor *Server*  *is installed:*   * [Windows PowerShell 3.0](`https://www.microsoft.com/en-us/download/details.aspx?id=34595` "Windows PowerShell 3.0") and above |
| * AD FS | *On the computer where* Auditor *Server*  *is installed:*   * Windows Remote Management must be configured to allow remote PowerShell usage. For that, set up the **TrustedHosts** list:   + to include all AD FS servers, use the following cmdlet: `Set-Item wsman:\localhost\Client\TrustedHosts -value '*' -Force;`   + to include specific AD FS servers (monitored items), do the following:   1. Use Get cmdlet to obtain the existing **TrustedHosts** list.   2. If necessary, add the IP addresses of required AD FS servers to existing list (use comma as a separator).   3. Provide the updated list to the cmdlet as a parameter. For example:  `Set-Item wsman:\localhost\Client\TrustedHosts -value '172.28.57.240,172.28.57.127' -Force;`  See the following Microsoft article [Installation and configuration for Windows Remote Management](`https://docs.microsoft.com/en-us/windows/win32/winrm/installation-and-configuration-for-windows-remote-management` "Installation and configuration for Windows Remote Management") for additional information about TrustedHosts. |
| * Windows Server (with enabled network traffic compression) * User Activity | *In the monitored environment:*   * .NET Framework 4.8 and above.  See the following Microsoft article for additional information about .Net Framework installer redistributable: [Microsoft .NET Framework 4.8 offline installer for Windows.](`https://support.microsoft.com/en-us/topic/microsoft-net-framework-4-8-offline-installer-for-windows-9d23f658-3b97-68ab-d013-aa3c3e7495e0` "Microsoft .NET Framework 4.8 offline installer for Windows") |
| * Microsoft Entra ID Ports * SharePoint Online | Usually, there is no need in any additional components for data collection. |
| * Oracle Database | Oracle Database 12c and above:  *On the computer where* Auditor *Server* *is installed:*   * Oracle Instant Client.    + Download the appropriate package from Oracle website: [Instant Client Packages](`https://www.oracle.com/database/technologies/instant-client.html` "Instant Client Packages"). Netwrix recommends installing the latest available version (Netwrix Auditor is compatible with version 12 and above).   + Install, following the instructions, for example, [Instant Client Installation for Microsoft Windows 64-bit](`https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html#ic_winx64_inst` "Instant Client Installation for Microsoft Windows 64-bit").  Check your Visual Studio Redistributable version. Applicable packages for each Oracle Database version with downloading links are listed in the installation instructions: [Instant Client Installation for Microsoft Windows 64-bit](`https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html#ic_winx64_inst` "Instant Client Installation for Microsoft Windows 64-bit").   Oracle Database 11g:  Auditor provides limited support of Oracle Database 11g. See the [Considerations for Oracle Database 11g](../Configuration/Oracle/Overview.htm#Consider "Considerations for Oracle Database 11g") topic for additional information.  *On the computer where* Auditor *Server* *is installed:*   * [Microsoft Visual C++ 2010 Redistributable Package](`https://www.microsoft.com/en-us/download/details.aspx?id=14632` "Microsoft Visual C++ 2010 Redistributable Package")—can be installed automatically during the monitoring plan creation. * Oracle Data Provider for .NET and Oracle Instant Client  Netwrix recommends the following setup steps:    1. Download the [64-bit Oracle Data Access Components 12c Release 4 (12.1.0.2.4) for Windows x64 (ODAC121024_x64.zip)](`http://www.oracle.com/technetwork/database/windows/downloads/index-090165.html` "64-bit Oracle Data Access Components 12c Release 4 (12.1.0.2.4) for Windows x64 (ODAC121024_x64.zip)") package.   2. Run the setup and select the Data Provider for .NET checkbox. Oracle Instant Client will be installed, too.   3. On the ODP.NET (Oracle Data Provider) step make sure the Configure ODP.NET and/or Oracle Providers for ASP.Net at machine-wide level checkbox is selected . |
| * Group Policy | *On the computer where* Auditor *Server* *is installed:*   * Group Policy Management Console. Download Remote Server Administration Tools that include GPMC for:   + [Windows 8.1](`http://www.microsoft.com/en-us/download/details.aspx?id=39296` "Windows 8.1")   + [Windows 10](`https://www.microsoft.com/en-us/download/details.aspx?id=45520` "Windows 10") * For Windows Server 2012 R2/2016, Group Policy Management is turned on as a Windows feature. |

## Using SSRS-based Reports

SQL Server Reporting Services are needed for this kind of reports. See the [Requirements for SQL Server to Store Audit Data](SQLServer.htm "Requirements for SQL Server to Store Audit Data") topic for additional information. If you plan to export or print such reports, check the requirements below.

**NOTE:** Please note that if you are going to use SQL Express plan, do not install SSRS and Auditor on the domain controller.

Export SSRS-based reports

To export SSRS-based reports, it is recommended Internet Explorer is installed on the machine where Auditor client runs. If IE is not available, you can use the **Print** function or click the button **Open in browser** and export the report directly from Netwrix Auditor.

See the following Microsoft article for the full list of the supported browsers: [Browser Support for Reporting Services and Power View](`https://learn.microsoft.com/en-us/sql/reporting-services/browser-support-for-reporting-services-and-power-view?view=sql-server-ver16` "Browser Support for Reporting Services and Power View").

Follow the steps to configure Internet Options to allow file downloads for the Local intranet zone.

**Step 1 –**  Select **Internet Options** and click **Security**.

**Step 2 –** Select **Local intranet** zone and click **Custom level**.

**Step 3 –** In the Settings list, locate **Downloads** \> **File download** and make sure the **Enabled** option is selected.

Printing

To print SSRS-based reports, SSRS Report Viewer and Auditor Client require ActiveX Control to be installed and enabled on the local machine. See the [Impossible to Export a Report](`https://helpcenter.netwrix.com/bundle/z-kb-articles-salesforce/page/kA04u000000HDfkCAG.html` "Impossible to Export a Report")  Netwrix knowledge base article for additional information.

You can, for example, open any SSRS-based report using your default web browser and click **Print**. The browser will prompt for installation of the additional components it needs for printing. Having them installed, you will be able to print the reports from Auditor UI as well.

## Server and Client

It is recommended to deploy Auditor server on the virtualized server – to simplify backup, provide scalability for future growth, and facilitate hardware configuration updates. Auditor client can be deployed on a physical or virtual workstation, as it only provides the UI.

You can deploy Netwrix Auditor on the VM running on any of the following hypervisors:

* VMware vSphere Hypervisor (ESXi)

  + You can deploy Netwrix Auditor to VMware cloud. You can install the product to a virtual machine or deploy as virtual appliance.
* Microsoft Hyper-V
* Nutanix AHV (Acropolis Hypervisor Virtualization) 20180425.199

See the [Virtual Deployment Overview](../Install/VirtualAppliance/Overview.htm "Virtual Appliance Overview") topic for additional information.

### Domains and Trusts

You can deploy Auditor on servers or workstations running supported Windows OS version. See system requirements for details.

Installation on the domain controller is not supported.

If you plan to have the audited system and Auditor Server residing in the workgroups, consider that in such scenario the product cannot be installed on the machine running Windows 7.

Domain trusts, however, may affect data collection from different data sources. To prevent this, consider the recommendations and restrictions listed below.

| If Auditor Server and the audit system reside... | Mind the following restrictions... |
| --- | --- |
| In the same domain | No restrictions |
| In two-way trusted domains | No restrictions |
| In non-trusted domains | * The computer where Auditor Server is installed must be able to access the target system (server, share, database instance, SharePoint farm, DC, etc.) by its DNS or NetBIOS name. * For monitoring Active Directory, File Servers, SharePoint, Group Policy, Inactive Users, Logon Activity, and Password Expiration, the domain where your target system resides as well as all domain controllers must be accessible by DNS or NetBIOS names—use the *nslookup* command-line tool to look up domain names. * For monitoring Windows Server and User Activity, each monitored computer (the computer where Netwrix Auditor User Activity Core Service resides) must be able to access the Auditor Server host by its DNS or NetBIOS name. |
| In workgroups | * The computer where Auditor Server is installed must be able to access the target system (server, share, database instance, SharePoint farm, DC, etc.) by its DNS or NetBIOS name. * For monitoring Active Directory, File Servers, SharePoint, Group Policy, Inactive Users, Logon Activity, and Password Expiration, the domain where your target system resides as well as all domain controllers must be accessible by DNS or NetBIOS names—use the *nslookup* command-line tool to look up domain names. * For monitoring Windows Server and User Activity, each monitored computer (the computer where Netwrix Auditor User Activity Core Service resides) must be able to access the Auditor Server host by its DNS or NetBIOS name. |

In the next sections you will find some recommendations based on the size of your monitored environment and the number of activity records (ARs) the product is planned to process per day.

Activity record stands for one operable chunk of information in Auditor workflow.

### Simple Deployment

This scenario can be used for PoC, evaluation, or testing purposes. It can be also suitable for small infrastructures, producing only several thousands of activity records per day. In this scenario, you only deploy Auditor Server and default client, selecting Full installation option during the product setup.

[![](../static/img/Auditor/Images/Auditor/DeploymentPlan/NA_Setup_Select_Type_thumb_0_0.png)](../../Resources/Images/Auditor/DeploymentPlan/NA_Setup_Select_Type.png)

If you plan to implement this scenario in bigger environments, consider hardware requirements listed in the Auditor documentation.

### Distributed Deployment (Client-Server)

In this scenario, multiple Auditor clients are installed on different machines.

Follow the steps to perform distributed deployment.

**Step 1 –**  Install Auditor server and default client, selecting Full installation during the product setup.

**Step 2 –** Then install as many clients as you need, running the setup on the remote machines and selecting Client installation during the setup. Alternatively, you can install Auditor client using Group Policy. See the [Install Client via Group Policy](../Install/ViaGroupPolicy.htm "Install Client via Group Policy") topic for additional information.

Default local client will be always installed together with the Auditor in all scenarios.