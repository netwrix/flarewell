---
title: "Prerequisites"
sidebar_position: 701
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

# Prerequisites

Netwrix Auditor Integration API uses HTTPS for communication with the automatically generated certificate. The default communication port is 9699.

Refer to the [Security](Security.htm "Security") topic for detailed instructions on how
to disable HTTPS and manage other API settings.

## Configure Integration API Settings

Follow the steps to change the port.

**Step 1 –** In the Netwrix Auditor main window, navigate to the Integration tile.

**Step 2 –** Make sure the Leverage Integration API option is enabled.

**Step 3 –**  Click Modify under the API settings section and specify a port number. Windows firewall rule will be automatically created.

**Step 4 –** If you use a third-party firewall, you must create a rule for inbound connections manually.

[![Integration API Settings](../static/img/Auditor/Images/Auditor/Settings/Integrations_thumb_0_0.png "Integration API Settings")](../../Resources/Images/Auditor/Settings/Integrations.png)

## Configure Audit Database Settings

When you first configure the Audit Database settings in Netwrix Auditor, the product also creates several databases for special purposes, including Netwrix_Auditor_API. This database is designed to store data imported from the other sources using Netwrix Auditor Integration API.

Make sure that the Audit Database settings are configured in Netwrix Auditor. To check or configure these settings, navigate to the **Settings \> Audit Database**.

You cannot use Netwrix Auditor Integration API without configuring the Audit Database.

Refer to the [Audit Database](../Admin/Settings/AuditDatabase.htm "Audit Database") topic for detailed instructions on how to configure SQL Server settings.