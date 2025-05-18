---
title: "Access Reviews"
sidebar_position: 657
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

# Access Reviews

Netwrix Auditor supports integration with Netwrix Auditor Access Reviews, which enables business owners to conduct resource and group reviews and recommend changes. The integration is available for the following data sources:

* Active Directory
* Dell Data Storage (only Unity family)
* NetApp
* Nutanix Files
* Qumulo
* SharePoint Online
* Synology
* Windows File Servers

## Getting Started

This workflow assumes you already have Netwrix Auditor installed with configured monitoring plans for a supported data source.

**NOTE:** Access Reviews is a separately licensed product and is not included with Netwrix Auditor. Make sure that you have the Access Reviews license enabled in Auditor.

See the [Licenses](Admin/Settings/Licenses.htm "Licenses") topic for additional information.

*Remember,* there is one single Access Review license for all data sources that can send data to the application.

Follow the steps to use Netwrix Auditor Access Reviews in conjuction with Auditor.

**Step 1 –** Install Access Reviews on the same computer where Netwrix Auditor is installed. See the [Installation Overview](../Access/Reviews/Installation/Overview.htm "Installation Overview") topic for prerequisites and additional information.

**Step 2 –** Configure Access Reviews. The Configuration interface is only available to users with the Administrator role. See the [Administrator Overview](../Access/Reviews/Admin/Overview.htm "Administrator Overview") topic for configuration settings and enabling user access.

**Step 3 –** Use the Access reviews configuration tool to setup the data flow from the Auditor database to the Access Reviews database. See the [Select Data Sources](AccessReviewsConfiguration.htm "Access Review Configuration Tool") topic for additional information.

**NOTE:** Data upload speed depends on the amount of collected data and Auditor collectors configuration.

**Step 4 –** Configure resource ownership through the Access Reviews Console. The Resource Owners interface is available to users with either the Security Team or Administrator role. Managing ownership is core component for the Access Reviews workflow. See the [Resource Owners Overview](../Access/Reviews/ResourceOwners/Overview.htm "Resource Owners Overview") topic for additional information.

**NOTE:** The [Owners & Access Reviews](../Access/Reviews/ResourceOwners/OwnerOverview.htm "Owners & Access Reviews") topic and subtopics are written for the assigned owners. You can distribute the URL to this topic or download a PDF to be distributed to your assigned resource owners.

**Step 5 –** Configure and run reviews. The Entitlement Reviews interface is available to users with either the Security Team or Administrator role. See the [Reviews Overview](../Access/Reviews/EntitlementReviews/Overview.htm "Reviews Overview") topic for additional information.

Netwrix Auditor Access Reviews is now configured and ready to use.

## Considerations & Limitations

Review the following considerations:

1. Enabling State-in-Time data collection for your monitoring plans option is not required for the integration works properly.
2. The data collected by Auditor is updated at least once a day.
3. If a monitoring plan or a data source with enabled integration is deleted, all collected data will be removed from the Access Reviews database.
4. If there are errors in upload of data to the Access Reviews database, these errors are reflected in the Netwrix Auditor Health Log and text log files; status of items and data sources in Auditor is not affected by these errors.
5. Permissions-related considerations:

   * For Windows File Servers, permission data for all items in this data source is sent to the Access Reviews application;
   * Only effective top-level permissions are sent (share+NTFS);
   * Permission data is sent per file server (entirely for each server);
   * Transfer of permission data to the Access Reviews application is started when you enable the integration for a data source.

   ## Initial Configuration

   Next, configure the Access Reviews for your environment:

   * Console Users — Grant users access to the application starting with an Administrator account. There are two levels of access: Administrator and Security Team. See the [Console Access Page](../Access/Reviews/Admin/Configuration/ConsoleAccess.htm "Console Access Page") topic for information.

     + Optionally, disable the Builtin Administrator account. See the [Modify the Builtin Administrator Account](../Access/Reviews/Admin/Configuration/ConsoleAccess.htm#Modify "Modify the Builtin Administrator Account") topic for additional information.
   * Notification — Configure the Notification settings required in order for the application to send email. See the [Notifications Page](../Access/Reviews/Admin/Configuration/Notifications.htm "Notifications Page") topic for information.

   ## Enable Console Users

   Access Reviews Console users granted one of the available roles should be notified.

   ***RECOMMENDED:*** The notification should include:

   * Why your organization is using Netwrix Auditor Access Reviews.
   * What they will be doing in the Access Reviews Console.
   * How to log into the Access Reviews Console, specifically what URL and credentials to use.

   You should also provide links to the appropriate topics based on the user's role:

   * Security Team — Need topics that align to the work the will be doing in the Access Reviews Console:

     + Ownership Administrator — Send the URL link for the [Resource Owners Overview](../Access/Reviews/ResourceOwners/Overview.htm "Resource Owners Overview") topic.
     + Review Administrator — Send the URL link for the [Reviews Overview](../Access/Reviews/EntitlementReviews/Overview.htm "Reviews Overview") topic.
   * Administrator — Send the URL link for the [Administrator Overview](../Access/Reviews/Admin/Overview.htm "Administrator Overview") topic.

   ## Resource Ownership Configuration

   Ownership of resources must be assigned in order to use the Access Reviews workflow:

   * Resource Ownership — Assign ownership for resources to be managed through the application. See the [Resource Owners Interface](../Access/Reviews/ResourceOwners/Interface.htm "Resource Owners Interface") topic for additional information.
   * Enable Owners — Send a notification to your owners about resource ownership with the application. See the [Notification to Owners](../Access/Reviews/ResourceOwners/Overview.htm#Notifica "Notification to Owners") topic for additional information.

   ## Access Reviews Workflow

   The Access Reviews applicaton runs attestations on resources and groups with the assigned owners. The workflow consists of:

   * Reviews — Configure reviews for resource Access or group Membership .
   * Owner Performs Review — Owners process the review, potentially recommending changes
   * Review Administrator Approval — Review and process owner recommended changes

   ***RECOMMENDED:*** Set expectations for response time from owners.

   Reviews can be run multiple times, maintaining a historical record for each instance. See the [Reviews Overview](../Access/Reviews/EntitlementReviews/Overview.htm "Reviews Overview") topic for additional information.