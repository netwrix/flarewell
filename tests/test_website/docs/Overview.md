---
title: "Windows Server"
sidebar_position: 1039
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

# Windows Server

Netwrix Auditor relies on native logs for collecting audit data. Therefore, successful change and access auditing requires a certain configuration of native audit settings in the audited environment and on the Auditor console computer. Configuring your IT infrastructure may also include enabling certain built-in Windows services, etc. Proper audit configuration is required to ensure audit data integrity, otherwise your change reports may contain warnings, errors or incomplete audit data.

**CAUTION:** Folder associated with Netwrix Auditor must be excluded from antivirus scanning. See the [Antivirus Exclusions for Netwrix Auditor](`https://helpcenter.netwrix.com/bundle/z-kb-articles-salesforce/page/kA04u0000000HirCAE.html` "Antivirus Exclusions for Netwrix Auditor") knowledge base article for additional information.

You can configure your IT Infrastructure for monitoring in one of the following ways:

* Automatically through a monitoring plan – This is a recommended method. If you select to automatically configure audit in the target environment, your current audit settings will be checked on each data collection and adjusted if necessary.
* Manually – Native audit settings must be adjusted manually to ensure collecting comprehensive and reliable audit data. You can enable Auditor to continually enforce the relevant audit policies or configure them manually:

  + The Remote Registry and the Windows Management Instrumentation (WMI) service must be started. See the [Enable Remote Registry and Windows Management Instrumentation Services](RemoteRegistry.htm "Enable Remote Registry and Windows Management Instrumentation Services") topic and the [Configure Windows Registry Audit Settings](WindowsRegistry.htm "Configure Windows Registry Audit Settings") topic for additional information.
  + The following advanced audit policy settings must be configured:

    - The Audit: Force audit policy subcategory settings (Windows 7 or later) security option must be enabled.
    - For Windows Server 2008—The Object Access, Account Management, and Policy Change categories must be disabled while the Security Group Management, User Account Management, Handle Manipulation, Other Object Access Events, Registry, File Share, and Audit Policy Change subcategories must be enabled for *"Success"*.
    - For Windows Server 2008 R2 / Windows 7 and above—Audit Security Group Management, Audit User Account Management, Audit Handle Manipulation, Audit Other Object Access Events, Audit Registry, Audit File Share, and Audit Audit Policy Changeadvanced audit policies must be set to *"Success"*.
    - See the [Configure Local Audit Policies](LocalPolicy.htm "Configure Local Audit Policies") topic and the [Configure Advanced Audit Policies](AdvancedPolicy.htm "Configure Advanced Audit Policies") topic for additional information.
  + The following legacy audit policies can be configured instead of advanced: Audit object access, Audit policy change, and **Audit account management** must be set to *"Success"*.
  + The Enable Persistent Time Stamp local group policy must be enabled. This policy should be configured manually since Auditor does not enable it automatically. See the [Configure Enable Persistent Time Stamp Policy](PersistentTimestamp.htm "Configure Enable Persistent Time Stamp Policy") topic for additional information.
  + The Application, Security, and System event log maximum size must be set to 4 GB. The retention method must be set to *“Overwrite events as needed”*. See the [Adjusting Event Log Size and Retention Settings](EventLog.htm "Adjusting Event Log Size and Retention Settings") topic for additional information.
  + For auditing scheduled tasks, the Microsoft-Windows-TaskScheduler/Operational event log must be enabled and its maximum size must be set to 4 GB. The retention method of the log must be set to *“Overwrite events as needed”*.
  + For auditing DHCP, the Microsoft-Windows-Dhcp-Server/Operational event log must be enabled and its maximum size must be set to 4 GB. The retention method of the log must be set to *“Overwrite events as needed”*. See the [Adjust DHCP Server Operational Log Settings](DHCP.htm "Adjust DHCP Server Operational Log Settings") topic for additional information.
  + For auditing DNS, the Microsoft-Windows-DNS-Server/Audit event log must be enabled and its maximum size must be set to 4 GB. The retention method of the log must be set to *“Overwrite events as needed”*.
  + The following inbound Firewall rules must be enabled:

    - Remote Event Log Management (NP-In)
    - Remote Event Log Management (RPC)
    - Remote Event Log Management (RPC-EPMAP)
    - Windows Management Instrumentation (ASync-In)
    - Windows Management Instrumentation (DCOM-In)
    - Windows Management Instrumentation (WMI-In)
    - Network Discovery (NB-Name-In)
    - File and Printer Sharing (NB-Name-In)
    - Remote Service Management (NP-In)
    - Remote Service Management (RPC)
    - Remote Service Management (RPC-EPMAP)
    - Performance Logs and Alerts (DCOM-In)
    - Performance Logs and Alerts (TCP-In)
  + If the audited servers are behind the Firewall, review the list of protocols and ports required for Netwrix Auditor and make sure that these ports are opened. See the [Windows Server Ports](Ports.htm "Windows Server Ports") topic for additional information.
  + For auditing removable storage media, two Event Trace Session objects must be created. See the [Configure Removable Storage Media for Monitoring](RemovableStorage.htm "Configure Removable Storage Media for Monitoring") topic for additional information.
  + If you want to use Network traffic compression, make sure that the Auditor console computer is accessible by its FQDN name.
  + For auditing IIS:

    - The **Remote Registry** service must be running and its **Startup Type** must be set to *"Automatic"*.
    - The Microsoft-IIS-Configuration/Operational log must be enabled and its maximum size must be set to 4 GB. The retention method of the log must be set to *“Overwrite events as needed”*.

Whatever method you choose to configure Windows Server for auditing (manual or automated), also remember to do the following:

1. Configure Data Collecting Account, as described in the [Data Collecting Account](../../Admin/MonitoringPlans/DataAccounts.htm "Data Collecting Account") topic.
2. Configure required protocols and ports, as described in the [Windows Server Ports](Ports.htm "Windows Server Ports") topic.

## Exclude Monitored Objects

You can fine-tune Netwrix Auditor by specifying data that you want to exclude from the Windows Server monitoring scope.

Follow the steps to exclude data from the Windows Server monitoring scope:

**Step 1 –** Navigate to the *%Netwrix Auditor installation folder%\Windows Server Auditing* folder.

**Step 2 –** Edit the \*.txt files, based on the following guidelines:

* Each entry must be a separate line.
* Wildcards (\* and ?) are supported. A backslash () must be put in front of (\*), (?), (,), and () if they are a part of an entry value.
* Lines that start with the # sign are treated as comments and are ignored.

| File | Description | Syntax |
| --- | --- | --- |
| omitcollectlist.txt | Contains a list of objects and their properties to be excluded from being monitored.  If you want to restart monitoring these objects, remove them from the omitcollectlist.txt and run data collection at least twice. | `monitoring plan name,server name,class name,property name,property value`  `class name` is a mandatory parameter, it cannot be replaced with a wildcard. `property name` and `property value` are optional, but cannot be replaced with wildcards either.  For example:   ```
#*,server,MicrosoftDNS_Server ```
```
#*,*,StdServerRegProv ```
|
| omiterrors.txt | Contains a list of errors/warnings to be omitted from logging to the Netwrix Auditor System Health event log. | `monitoring plan name,server name,error text`  For example:  `*,productionserver1.corp.local,*Access is denied*` |
| omitreportlist.txt | Contains a list of objects to be excluded from reports and Activity Summary emails. In this case audit data is still being collected. | `monitoring plan name,who,where,object type,what,property name`  For example:  `*,CORP\\jsmith,*,*,*,*` |
| omitsitcollectlist.txt | Contains a list of objects to be excluded from State-in-time reports. | `monitoring planname,server name,class name,property name,property value`  `class name` is a mandatory parameter, it cannot be replaced with a wildcard. `property name` and `property value` are optional, but cannot be replaced with wildcards either.  For example:  `*,server,MicrosoftDNS_Server`  `*,*,StdServerRegProv` |
| omitstorelist.txt | Contains a list of objects to be excluded from being stored to the Audit Archive and showing up in reports. In this case audit data is still being collected. | `monitoring plan name,who,where,object type,what,property name`  For example:  `*,*,*,Scheduled task,Scheduled Tasks\\User_Feed_Synchronization*,*` |

## Monitored Objects

This section lists Windows Server components and settings whose changes Netwrix Auditor can monitor.

When monitoring a Windows Server, Netwrix Auditor needs to audit some registry settings. See the [Windows Server Registry Keys](#WindowsRegistry "Windows Server Registry Keys") section for additional information. If you want Netwrix Auditor to audit custom registry keys, see the [Monitoring Custom Registry Keys](#Audit_Custom_Registry_keys "Monitoring Custom Registry Keys")[Monitoring Custom Registry Keys](#Audit_Custom_Registry_keys "Monitoring Custom Registry Keys")topic for additional information.

In the table below, double asterisks (\*\*) indicates the components and settings for which the Who value is reported as *“Not Applicable”*.

| Object type | Attributes |
| --- | --- |
| General Computer Settings | |
| Computer | * System state changed to Started * System state changed to Stopped. Reason: Reason type * System state changed to Stopped. Reason: unexpected shutdown or system failure |
| Computer Name | * Computer Description * Name * Domain |
| Environment Variables | * Type * Value |
| Event Log | * Event Log Cleared |
| General | * Caption * Organization * Registered User * Serial Number * Service Pack\*\* * Version\*\* |
| Remote | * Enable Remote Desktop on this computer |
| Startup and Recovery | * Automatically Restart * Dump File * Dump Type * Overwrite any existing file * Send Alert * System Startup Delay * Write an Event |
| System Time | * System time changed from ... to ... * Time zone changed  Not supported on Windows Server 2008 SP2 and Windows Server 2008 R2. |
| Add / Remove Programs | |
| Add or Remove Programs | * Installed For\*\* * Version |
| Services | |
| System Service | * Action in case of failed service startup * Action in case of service stopping * Allow service to interact with desktop * Caption * Created * Deleted * Description * Name * Path to executable * Service Account * Service Type * Start Mode * Error Control |
| Audit Policies | |
| Local Audit Policy | * Added Audit settings  Only for the Global Object Access Auditing advanced policies. * Successful audit enabled/disabled * Failure audit enabled/disabled |
| Per-User Local Audit Policy | * Success audit include added * Success audit include removed * Failure audit include added * Failure audit include removed * Success audit exclude added * Success audit exclude removed * Failure audit exclude added * Failure audit exclude remove |
| Hardware | |
| Base Board\*\* | * Hosting Board * Status * Manufacturer * Product * Version * Serial Number |
| BIOS\*\* | * Manufacturer * Version |
| Bus\*\* | * Bus Type * Status |
| Cache Memory\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Purpose * Status |
| CD-ROM Drive\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Media Type * Name * SCSI Bus * SCSI Logical Unit * SCSI Port * SCSI Target ID * Status |
| Disk Partition\*\* | * Primary Partition * Size (bytes) * Starting offset (bytes) |
| Display Adapter\*\* | * Adapter RAM (bytes) * Adapter Type * Bits/Pixel * Configuration Manager Error Code * Driver Version * Installed Drivers * Last Error Description * Last Error Code * Refresh Rate * Resolution * Status |
| DMA\*\* | * Status |
| Floppy Drive\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Status |
| Hard Drive\*\* | * Bytes/Sector * Configuration Manager Error Code * Interface Type * Last Error Description * Last Error Code * Media Loaded * Media Type * Model * Partitions * SCSI Bus * SCSI Logical Unit * SCSI Port * SCSI Target ID * Sectors/Track * Size (bytes) * Status * Total Cylinders * Total Heads * Total Sectors * Total Tracks * Tracks/Cylinder |
| IDE\*\* | * Configuration Manager Error Code * Description * Last Error Description * Last Error Code * Status |
| Infrared\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Status |
| Keyboard\*\* | * Configuration Manager Error Code * Description * Last Error Description * Last Error Code * Layout * Name * Status |
| Logical Disk\*\* | * Description * File System * Size (bytes) * Status |
| Monitor\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Monitor Type * Status |
| Network Adapter | * Adapter Type   \* * Configuration Manager Error Code * Default IP Gateway   \* * DHCP Enabled\* * DHCP Server * DNS Server Search Order * IP Address   \* * Last Error Description * Last Error Code * MAC Address * Network Connection Name * Network Connection Status * Service Name * Status   \* — indicates the properties whose changes may not be reported correctly, displaying "*Who*" (i.e. initiator's account) as *System*. |
| Network Protocol\*\* | * Description * Status |
| Parallel Ports\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Status |
| PCMCIA Controller\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Status |
| Physical Memory\*\* | * Capacity (bytes) * Status * Manufacturer * Memory Type * Speed * Part Number * Serial Number |
| Pointing Device\*\* | * Configuration Manager Error Code * Double Click Threshold * Handedness * Hardware Type * Last Error Description * Last Error Code * Number of buttons * Status |
| Printing | * Comment\*\* * Hidden\*\* * Local\*\* * Location\*\* * Name\*\* * Network\*\* * Port Name\*\* * Printer error information * Published\*\* * Shared\*\* * Share Name\*\* * Status |
| Processor\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Max Clock Speed (MHz) * Name * Status |
| SCSI\*\* | * Configuration Manager Error Code * Description * Last Error Description * Last Error Code * Status |
| Serial Ports\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Maximum Bits/Second * Name * Status |
| Sound Device\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Status |
| System Slot\*\* | * Slot Designation * Status |
| USB Controller\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Name * Status |
| USB Hub\*\* | * Configuration Manager Error Code * Last Error Description * Last Error Code * Name * Status |
| DHCP configuration | |
| If the DHCP server runs on Windows Server 2008 (or below), then the Who value for DHCP server configuration events is reported as *“Not Applicable”*. | |
| Server role | * Added * Removed |
| Server settings | * Type:   + IPv4   + IPv4 Filters   + IPv6 * Action:   + Modified |
| DHCP scope | * Type:   + IPv4   + Multicast IPv4   + Superscope for IPv4   + IPv6 * Action:   + Added   + Removed   + Modified   + Moved |
| DHCP Reservation | * Type:   + IPv4   + IPv6 * Action:   + Added   + Removed   + Modified |
| DHCP Policy | * Type:   + IPv4   + IPv4 server-wide * Action:   + Added   + Removed   + Modified   + Renamed |
| Removable media | |
| Removable Storage Media\*\* | Netwrix Auditor does not report on floppy/optical disk and memory card storage medias.  For removable storages, the When value reports actual time when a change was made and/or a target server was started.   * Device class:   + CD and DVD   + Floppy Drives   + Removable Disk   + Tape Drives   + Windows Portable Devices   When the Audit Object Access local audit policy and/or the Audit Central Access Policy Staging  Audit Removable Storage advanced audit policies are enabled on the target server, the `gpupdate /force` command execution issues removable storage restart. These actions are disclosed in Netwrix Auditor reports, search, and activity summaries. Note that these actions are system, not user-effected. |
| Scheduled Tasks | |
| Scheduled Task | * Account Name * Application * Comment * Creator * Enabled * Parameters * Triggers |
| Local Users and Groups | |
| Local Group | * Description * Name * Members |
| Local User | * Description * Disabled/Enabled * Full Name * Name * User cannot change password * Password Never Expires * User must change password at next logon |
| DNS Configuration | |
| The Who value will be reported for DNS configuration settings only if the DNS server runs on Windows Server 2012 R2. See the following Microsoft article for additional information: [Update adds query logging and change auditing to Windows DNS servers](`https://support.microsoft.com/en-us/kb/2956577` "Update adds query logging and change auditing to Windows DNS servers"). | |
| DNS Server | * Address Answer Limit * Allow Update * Auto Cache Update * Auto Config File Zones * Bind Secondaries * Boot Method * Default Aging State * Default No Refresh Interval * Default Refresh Interval * Disable Auto Reverse Zones * Disjoint Nets * Ds Available * Ds Polling Interval * Ds Tombstone Interval * EDns Cache Timeout * Enable Directory Partitions * Enable Dns Sec * Enable EDns Probes * CD-ROM D  Enable Netmask Ordering * Event Log Level * Fail On Load If Bad Zone Data * Forward Delegations * Forwarders * Forwarding Timeout * Is Slave * Listen Addresses * Log File Max Size * Log File Path * Log Level * Loose Wildcarding * Max Cache TTL * Max Negative Cache TTL * Name Check Flag * No Recursion * Recursion Retry * Recursion Timeout * Round Robin * Rpc Protocol * Scavenging Interval * Secure Cache Against Pollution * Send Port * Server Addresses |
| DNS Zone | * Aging State * Allow update * Auto created * Data file name * Ds integrated * Expires after * Forwarder slave * Forwarder timeout * Master servers * Minimum TTL * No refresh interval * Notify * Notify servers * Owner name * Paused * Primary server * Refresh interval * Responsible person * Retry interval * Reverse * Scavenge servers * Secondary servers * Secure secondaries * Shutdown * TTL * User NB stat * Use WINS * Zone type |
| DNS Resource Records | |
| The Who value will be reported for DNS Resource Records only if the DNS server runs Windows Server 2012 R2. See the following Microsoft article for additional information: [Update adds query logging and change auditing to Windows DNS servers](`https://support.microsoft.com/en-us/kb/2956577` "Update adds query logging and change auditing to Windows DNS servers"). | |
| DNS AAAA | * Container name * IPv6 Address * Owner name * Record class * TTL * Zone type |
| DNS AFSDB | * Container name * Owner name * Server name * Server subtype * Record class * TTL * Zone type |
| DNS ATM A | * ATM Address * Container name * Format * Owner name * Record class * TTL * Value * Zone type |
| DNS A | * Container name * IP Address * Owner name * Record class * TTL * Zone type |
| DNS CNAME | * Container name * FQDN for target host * Owner name * Record class * TTL * Zone type |
| DNS DHCID | * Container name * DHCID (base 64) * Owner name * Record class * TTL * Zone type |
| DNS DNAME | * Container name * FQDN for target domain * Owner name * Record class * TTL * Zone type |
| DNS DNSKEY | * Algorithm * Container name * Key type * Key (base 64) * Name type * Owner name * Protocol * Record class * Signatory field * TTL * Zone type |
| DNS DS | * Algorithm * Container name * Data * DigestType * Key tag * Owner name * Record class * TTL * Zone type |
| DNS HINFO | * Container name * CPU type * Operating system * Owner name * Record class * TTL * Zone type |
| DNS ISDN | * Container name * ISDN phone number and DDI * ISDN subaddress * Owner name * Record class * TTL * Zone type |
| DNS KEY | * Algorithm * Container name * Key type * Key (base 64) * Name type * Owner name * Protocol * Record class * Signatory field * TTL * Zone type |
| DNS MB\*\*\* | * Container name * Mailbox host * Owner name  * Record class * TTL * Zone type |
| DNS MD | * Container name * MD host * Owner name  * Record class * TTL * Zone type |
| DNS MF | * Container name * MF host * Owner name  * Record class * TTL * Zone type |
| DNS MG | * Container name * Member mailbox * Owner name  * Record class * TTL * Zone type |
| DNS MINFO | * Container name * Error mailbox * Owner name * Responsible mailbox  * Record class * TTL * Zone type |
| DNS MR | * Container name * Owner name * Replacement mailbox  * Record class * TTL * Zone type |
| DNS MX | * Container name * FQDN of mail server * Mail server priority * Owner name  * Record class * TTL * Zone type |
| DNS NAPTR | * Container name * Flag string * Order * Owner name * Preference * Record class * Regular expression string * Replacement domain * Service string * TTL * Zone type |
| DNS NS | * Container name * Name servers * Owner name * TTL |
| DNS NXT | * Container name * Next domain name * Owner name * Record class * Record types * TTL * Zone type |
| DNS PTR | * Container name * Owner name * PTR domain name * Record class * TTL * Zone type |
| DNS RP | * Container name * Mailbox of responsible person * Optional associated text (TXT) record * Owner name  * Record class * TTL * Zone type |
| DNS RRSIG | * Algorithm * Container name * Key tag * Labels * Original TTL * Owner name * Record class * Signature expiration (GMT) * Signature inception (GMT) * Signature (base 64) * Signer's name * TTL * Type covered * Zone type |
| DNS RT | * Container name * Intermediate host * Owner name * Preference  * Record class * TTL * Zone type |
| DNS SIG | * Algorithm * Container name * Key tag * Labels * Original TTL * Owner name * Record class * Signature expiration (GMT) * Signature inception (GMT) * Signature (base 64) * Signer's name * TTL * Type covered * Zone type |
| DNS SRV | * Container name * Host offering this service * Owner name * Port number * Priority * Record class * TTL * Weight * Zone type |
| DNS TEXT | * Container name * Owner name * Record class * Text * TTL * Zone type |
| DNS WINS | * Cache time-out * Container name * Do not replicate this record * Lookup time-out * Owner name * Record class * Wins servers * Zone type |
| DNS WKS | * Container name * IP address * Owner name * Protocol * Record class * Services * TTL * Zone type |
| DNS X25 | * Container name * Owner name * Record * Record class * TTL * X.121 PSDN address * Zone type |
| File Shares | |
| Share | * Access-based enumeration * Caching * Description * Enable BranchCache * Encrypt data access * Folder path * Share permissions * User limit |

### Windows Server Registry Keys

If you want to monitor changes to system components on a Windows Server, make sure that Windows Registry audit settings are configured on that Windows server.

This refers to the following keys:

* HKEY_LOCAL_MACHINE\SOFTWARE
* HKEY_LOCAL_MACHINE\SYSTEM
* HKEY_USERS\.DEFAULT

For these keys and subkeys, the following advanced permissions must be audited ("*Successful*" audit type required):

* Set Value
* Create Subkey
* Delete
* Write DAC
* Write Owner

The below is the full list of keys (and subkeys) involved in Windows Server auditing.

|  |  |
| --- | --- |
| Hardware | * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Network\{4D36E972-E325-11CE-BFC1-08002BE10318\}(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318\}(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services(|\.\*) |
| General | * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\CrashControl(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\CrashControl(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Control\CrashControl(|\.\*) * HKEY_LOCAL_MACHINE\Software\WOW6432NODE\Microsoft\Windows NT\CurrentVersion(|\.\*) * HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion(|\.\*) |
| Software | * HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432NODE\MICROSOFT\WINDOWS\CURRENTVERSION\UNINSTALL(|\.\*) * HKEY_LOCAL_MACHINE\SOFTWARE\MICROSOFT\WINDOWS\CURRENTVERSION\UNINSTALL(|\.\*) |
| Services | * HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services(|\.\*) * HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services(|\.\*) |
| RemovableMedia | * SYSTEM\CurrentControlSet\Enum |

Consider that audit data for the registry keys themselves will not appear in Netwrix Auditor reports, alerts or search results, as it is only used as one of the sources for the Activity Records formation.

* You can configure these settings automatically using Netwrix Auditor, as described in the [Settings for Data Collection](../../Admin/MonitoringPlans/Create.htm#Settings "Settings for Data Collection") topic. Corresponding audit settings will be also applied automatically after you select a checkbox under **Monitor changes to system components** on the **General** tab in the Windows Server data source properties.

Audit settings will be automatically adjusted only for the keys/subkeys involved in the monitoring of selected components (granular adjustment). For example, if you selected **Services**, the program will adjust the audit settings for the following subkeys:

* HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services(|\\.\*)
* HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services(|\\.\*)
* HKEY_LOCAL_MACHINE\SYSTEM\ControlSet002\Services(|\\.\*)

* To configure the audit settings manually, refer to the [Configure Windows Registry Audit Settings](WindowsRegistry.htm "Configure Windows Registry Audit Settings") topic for additional information.

#### Monitoring Custom Registry Keys

Follow the steps to monitor custom registry keys.

**Step 1 –** On the computer where Auditor Server resides, navigate to *%Netwrix Auditor installation folder%\Windows Server Auditing.*

![](../static/img/Auditor/Images/Auditor/Configuration/WindowsFileServer/CustomRegistryKeyEntry.png)

**Step 2 –** Edit the following parameters of the customregistrykeys.txt file:

`monitoring plan name,server name,registry key name`

For example:

`#*,productionserver1.corp.local,HKEY_LOCAL_MACHINE\\SYSTEM\\RNG`

**Step 3 –** Consider the following:

* Each entry must be a separate line.
* Wildcards (\* and ?) are supported (except for the `registry key name` field). A backslash () must be put in front of (\*), (?), (,), and () if they are a part of an entry value.
* Lines that start with the # sign are treated as comments and are ignored.

![](../static/img/Auditor/Images/Auditor/Configuration/WindowsFileServer/CustomRegistryKey.png)

**NOTE:** In some cases, **Who** will be the system and **When** will be collection time, because there is no necessary event in the Security log with this path.

## VM Template Cloning

While VM cloning is supported by Netwrix Auditor, an additional setup process should be taken into consideration before the deployment process.

Every monitored VM instance gets a unique ID assigned for monitoring and data collection purposes. To ensure proper operation, the VM template must be excluded from the monitoring scope beforehand. Omitting the VM template will allow Netwrix Auditor to assign unique IDs correctly and collect data as intended.

Follow the steps to add the template server to exclusions.

**Step 1 –** In main Netwrix Auditor menu, select **Monitoring plans**.

**Step 2 –** Select your Windows Server monitoring plan and click **Edit**.

**Step 3 –** Choose the AD Container containing the template VM and click **Edit data source** in the right pane.

**Step 4 –** In the left pane, select **Containers and Computers**.

**Step 5 –** Check the **Exclude these objects** checkbox and add the template VM by clicking **Add Computer**.

VM template server is added to exclusions and ready to use.