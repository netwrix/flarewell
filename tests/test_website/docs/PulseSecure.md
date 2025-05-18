---
title: "Configure Pulse Secure Devices"
sidebar_position: 1006
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

# Configure Pulse Secure Devices

1. Connect to your Pulse Secure device: launch an Internet browser and enter the IP address or device DNS name in the URL field (`https:///admin).
2. In the Web Interface, navigate to System → Log/Monitoring.
3. Under Log/Monitoring, expand the User Access link.
4. Locate the Settings tab.
5. Under the Select Events to Log, select the following (minimal requirement, select other events if needed):

   * Login/Logout
   * VPN Tunneling

   ![](../static/img/Auditor/Images/Auditor/ManualConfig/Manual_Config_Pulse_1.png)
6. Under the Syslog Servers, complete the following fields:

   | Option | Description |
   | --- | --- |
   | Server nameIP | Specify the IP address of the computer where resides. |
   | Facility | Select desired facility. |
   | Type | Select UDP. |
   | Client Certificate | Use default values. |
   | Filter | Select Standard. |
7. Save your changes.
8. Switch to the Admin Access tab.
9. Under the Select Events to Log, select the following (minimal requirement, select other events if needed):

   * Administrator logins
   * Administrator changes
10. Repeat the step 6 for Syslog Servers configuration.
11. Save your changes.
12. Navigate to System → Configuration → Advanced Networking.
13. Expand the Select the source port to be used for the following features link.
14. Locate the Syslog parameter and set it to *Internal*.

    Netwrix Auditor must be accessible from the selected network interface
15. Save your changes.
16. Start Netwrix Auditor.
17. Navigate to your monitoring plan for Network Devices. See [Monitoring Plans](../../Admin/MonitoringPlans/Overview.htm "Monitoring Plans")
18. Provide the IP address of the interface you specified on the step 14 as the Computer item for your monitoring plan. See [Active Directory](../../Admin/MonitoringPlans/ActiveDirectory/Overview.htm "Active Directory Plans")

## Pulse Secure Devices

Review a full list of object types Netwrix Auditor can collect on Pulse Secure network devices.

| Object Type | Actions |  |
| --- | --- | --- |
| Logon | * Successful logon | * user authenticated successfully * user logged in successfully * administrative login succeeded * SuperAdmin session created using token for administrative logon recovery * Admin logged in successfully through the local console |
| * Failed logon | * Login/authentication failed * Login attempt from the local console failed |
| * Logoff | * user logged out or session timed out * admin logged out or session timed out * SuperAdmin session finished or timed out * Admin logged off from the local console |
| Authentication | * Successful logon | * VPN Tunneling Successful Logon |
| * Logoff | * VPN connection closed |
| Configuration | * Modified | * Server shutdown/reboot/restart requested * Platform administrator account added * Console administrator password is disabled or enabled * IKEv2 settings modified * Global SAML Settings modified * SAML Metadata Provider added * SAML Metadata Provider removed * SAML Metadata Provider updated * authentication server added * authentication server deleted * authentication server modified * Sign-in policy created * Sign-in policy deleted * Sign-in policy modified * Sign-in policy multiple user session limit modified * Sign-in policy multiple user session modified * Sign-in policy multiple user session warning notification modified * Updated the order of the sign-in policies * Sign-in policy user access parameters modified * Sign-in page created * Sign-in page deleted * Sign-in page updated * Sign-in notification created * Sign-in notification deleted * Sign-in notification updated * Sign-in SAML modified |
| User | * Added | * user account added |
| * Modified | * user account password changed * user account disabled or enabled * user account unlocked * user account modified * admin rights granted * admin rights revoked |
| * Removed | * user account removed |
| Role | * Added | * Role is created |
| * Modified | * Role is modified |
| * Removed | * Role is deleted |
| * Copied | * Role is duplicated |
| Session | * Session start | * VPN Tunneling Session started |
| * Session end | * VPN Tunneling Session ended |
| Realm | * Added | * Realm added |
| * Modified | * IP added to allowed IP list in Realm authentication policy * IP removed from allowed IP list * IP setting reordered * Source IP restriction modified * browser restriction set * Browser restriction modified * browser restriction removed * Browser restriction reordered * Client-side certificate requirement modified * Certificate attribute modified * Password restriction modified * Minimum password length modified * Host Checker restriction is updated * User Limit restriction is modified * Guaranteed minimum number of users is modified * Maximum number of sessions is modified * Maximum number of users is modified * Realm is modified |
|  | * Removed | * Realm deleted |
| * Copied | * Realm duplicated |
| * Renamed | * Realm renamed |