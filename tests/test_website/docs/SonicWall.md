---
title: "Configure SonicWall Devices"
sidebar_position: 1002
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

# Configure SonicWall Devices

Netwrix Auditor relies on native logs for collecting audit data. Therefore, successful change and access auditing requires a certain configuration of native audit settings in the audited environment and on the Auditor console computer. Configuring your IT infrastructure may also include enabling certain built-in Windows services, etc. Proper audit configuration is required to ensure audit data integrity, otherwise your change reports may contain warnings, errors or incomplete audit data.

**CAUTION:** Folder associated with Netwrix Auditor must be excluded from antivirus scanning. See the [Antivirus Exclusions for Netwrix Auditor](`https://helpcenter.netwrix.com/bundle/z-kb-articles-salesforce/page/kA04u0000000HirCAE.html` "Antivirus Exclusions for Netwrix Auditor") knowledge base article for additional information.

You can configure your IT Infrastructure for monitoring in one of the following ways:

* Automatically through a monitoring plan – This is a recommended method. If you select to automatically configure audit in the target environment, your current audit settings will be checked on each data collection and adjusted if necessary.
* Manually – Native audit settings must be adjusted manually to ensure collecting comprehensive and reliable audit data. You can enable Auditor to continually enforce the relevant audit policies or configure them manually:

  + Configure log settings, depending on your device type.

To configure your SonicWall devices, do the following:

To configure SonicWall Web Application Firewall

1. Connect to your SonicWall device. Launch an Internet browser and enter the following in the URL field: *`https://:84443*, where IP address is the IP of the device and 84443 is the default connection port.
2. Log in to the device.
3. In the Web Interface, navigate to Log → Settings and configure the following:

   | Parameter | Description |
   | --- | --- |
   | * Log Level * Alert Level * Syslog Level | Set to "Info". |
   | * Enable Audit Log * Send to Syslog Server in Audit Log Settings * Send to Syslog Server in Access Log Settings | Select these checkboxes. |
   | Primary Syslog Server | Enter the address of your Netwrix Auditor Server. |
   | Primary Syslog Server Port | Provide the name of the UDP port used to listen to network devices (514 port used by default). |
4. Click Accept.
5. Navigate to Log → Categories.
6. Select the following checkboxes:

   * Authentication
   * Authorization & Access
   * System
   * Web Application Firewall
   * Geo IP & Botnet Filter In Log Categories (Standard)
7. Click Accept.

To configure SonicWall SMA

1. Connect to your SonicWall device. Launch an Internet browser and enter the following in the URL field: *`https://:8443*, where IP address is the IP of the device and 8443 is the default connection port.
2. Log in to the device.
3. In the Web Interface, navigate Log → Settings and configure the following:

   | Parameter | Description |
   | --- | --- |
   | * Log Level * Alert Level * Syslog Level | Set to "Info". |
   | * Enable Audit Log * Send to Syslog Server in Audit Log Settings * Send to Syslog Server in Access Log Settings | Select these checkboxes. |
   | Primary Syslog Server | Enter the address of your Netwrix Auditor Server. |
   | Primary Syslog Server Port | Provide the name of the UDP port used to listen to network devices (514 port used by default). |
4. Click Accept.
5. Navigate to Log → Categories.
6. Select the following checkboxes:

   * Authentication
   * Authorization & Access
   * System
   * Web Application Firewall
   * Geo IP & Botnet Filter In Log Categories (Standard)
7. Click Accept.

To configure SonicWall NS series

1. Connect to your SonicWall device. Launch an Internet browser and enter the following in the URL field: *`https://:443*, where IP address is the IP of the device and 443 is the default connection port.
2. Log in to the device.
3. In the Web Interface, navigate to Manage → Log Settings → Base Setup.
4. Select all checkboxes in the Syslog column.
5. Click Accept.
6. Navigate to Manage → Log Settings → Syslog.
7. Set the Syslog Format to Default.
8. Click Add.
9. In the dialog appears, select Create new address object option in the Name or IP Address combo box.
10. Provide name and IP address of the new object.
11. Click OK.
12. In the Add Syslog Server dialog, find the IP address you specified on the step 10 in the Name or IP Address list.
13. Click OK.
14. Click Save.

## SonicWall Devices

Review a full list of object types Netwrix Auditor can collect on SonicWall network devices.

| Object type | Actions | Event ID |
| --- | --- | --- |
| Logon | * Successful logon | * User login from an internal zone allowed * User login successful * XAUTH Succeeded with VPN * VPN zone remote user login allowed * WAN zone remote user login allowed * PPP: Authentication successful * Local Authentication Success * RADIUS/LDAP Authentication Success * Successful authentication received for Remotely Triggered * IKEv2 Authentication successful * SSL VPN zone remote user login allowed |
| * Failed logon | * User login denied * User login failed * XAUTH Failed with VPN * L2TP PPP Authentication Failed * check username / password * RADIUS/LDAP reports Authentication Failure * Local Authentication Failure * User login to Administration Portal denied * User login failure rate exceeded * User Name authentication Failure locally * ISAKMP_AUTH_FAILED * Guest service limit reached * Guest login denied * Incorrect authentication received for Remotely Triggered * Authentication Timeout during Remotely Triggered * Problem occurred during user group membership retrieval * An error has occurred while sending your * IPsec Authentication Failed |
| * Logoff | * User logged out * logged out * Guest Session Timeout * Guest Account Timeout * Guest Idle Timeout * Guest traffic quota exceeded |
| Authentication | * Successful Logon | * Administrator login allowed * CLI administrator login allowed * VPN zone administrator login allowed * WAN zone administrator login allowed * Configuration mode administration session started * Read-only mode GUI administration session started * Non-config mode GUI administration session started * User login successful * Session Start: * EventMessage: Session Start Success |
| * Failed Logon | * Administrator login denied * CLI administrator login denied due to bad credentials * User login failed * The account has been disabled for * is not permitted for this Web App * Authentication for user * Authentication failed * maximum authentication attempts exceeded for * EventMessage: Session Start Failed |
| * Logoff | * Administrator logged out * CLI administrator logged out * Configuration mode administration session ended * GUI administration session ended * Logged out * Session End: * EventMessage: Session End * Command='Tunnel' |
| Configuration | * Add / Added (Failed attempt) | * m=1333 * Scheduled settings generated * A new default Self-Signed certificate was generated successfully * Scheduled Tech Support Report generated * Restarted Tech Support Report generated |
| * Modified / Modify (Failed attempt) | * Mail attachment disabled * Watch and report possible SYN floods * Watch and proxy WAN connections when under attack * Always proxy WAN connections * SYN Flood blacklisting enabled by user * SYN Flood blacklisting disabled by user * Administrator name changed * VPN disabled by administrator * VPN enabled by administrator * WLAN disabled by administrator * WLAN enabled by administrator * WLAN disabled by schedule * WLAN enabled by schedule * is added into Group * is removed from Group * m=1334 * Update administrator/user lockout params * Settings imported * Critical Operating System Update failed * msg="WAF restarted * HTTP(S) Cache settings were updated * database has been updated * Web Server Fingerprint Protection enforced * About to reconfigure service: * Finished applying configuration changes * Started * Start failed * Stopped |
| * Read / Read (Failed attempt) | * m=1203 * m=1204 * Problem loading the URL list * Registration Update Needed, Please restore your existing security service subscriptions * Failed to synchronize license information with Licensing Server * Current settings exported * Error sending * settings sent successfully * Automated scheduled settings successful * Scheduled settings downloaded * Tech Support Report * Tech Support Report sent successfully * Loaded WAF signature database successfully * Error sending * logs sent out successfully |
|  | * Remove / Removed (Failed attempt) | * Scheduled settings deleted * Oldest scheduled Tech Support Report deleted * has been deleted * Event Logs cleared * Audit Logs cleared * Access Logs cleared * Deleting log files * Deleting core files * Deleting snapshots older |
| Device state | * Modified / Modify (Failed attempt) | * Registration Update Needed, Please restore your existing security service subscriptions * Intrusion Prevention (IDP) subscription has expired * Failed to synchronize license information with Licensing Server |
| Folder | * Add / Added (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=9&Arg1= |
| * Read / Read (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=16&Arg1= |
| * Remove / Removed (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=13&Arg1= |
| File | * Add / Added (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=31&Arg1= |
| * Read / Read (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=25&Arg1= |
| * Rename / Renamed (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=14&Arg1= |
| * Remove / Removed (Failed attempt) | * Request='GET /cgi-bin/sonicfiles?RacNumber=12&Arg1= |
| Host | * Read / Read (Failed attempt) | * Received AV Alert * The loaded content URL List has expired * CFS Alert * Mail Filter Alert * Mail attachment deleted * Intrusion Prevention (IDP) subscription has expired * Smurf Amplification attack dropped * TCP Xmas Tree dropped * Source routed IP packet dropped * Mail fragment dropped * PASV response spoof attack dropped * PORT bounce attack dropped * PASV response bounce attack dropped * Spank attack multicast packet dropped * IPS Detection Alert * IPS Prevention Alert * Drop WLAN traffic * IDP Detection Alert * IDP Prevention Alert * Ping of death dropped * IP spoof dropped * Possible SYN flood attack detected * Land attack dropped |
| Rule | * Activated | * will be denied * msg="WAF threat detected * Ping of death dropped * IP spoof dropped * Possible SYN flood attack detected * Land attack dropped * Smurf Amplification attack dropped * Possible port scan detected * Probable port scan detected * Probable TCP FIN scan detected * Probable TCP XMAS scan detected * Probable TCP NULL scan detected * Mail attachment deleted * TCP Xmas Tree dropped * Source routed IP packet dropped * Mail fragment dropped * PASV response spoof attack dropped * PORT bounce attack dropped * PASV response bounce attack dropped * Spank attack multicast packet dropped * IPS Detection Alert * IPS Prevention Alert * Drop WLAN traffic * IDP Detection Alert |
| Session | * Add / Added (Failed attempt) | * msg="New HTTP Request to * msg="New HTTPS Request to * msg="New HTTP Session for * msg="New HTTPS Session for |
| * Read / Read (Failed attempt) | * msg="WAF threat detected: * will be denied * Access to proxy server denied * Website found in blacklist |
| * Logoff | * Connection Closed |
| User | * Add / Added (Failed attempt) | * Guest account |
| * Modified / Modify (Failed attempt) | * Administrator name changed * out user logins allowed * Guest account * User login disabled from * User account |
| * Remove / Removed (Failed attempt) | * Guest account * m=1335 |