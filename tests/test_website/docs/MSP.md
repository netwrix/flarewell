---
title: "MSP Usage Example"
sidebar_position: 852
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

# MSP Usage Example

Consider a situation when a password is reset for a user, computer, or **inetOrgPerson** account.

After deploying and configuring the add-on as described in this guide, the MSP (Managed Service Providers) staff member enabled Auditor integration feature:

[![Integration API Settings](../static/img/Auditor/Images/Auditor/Settings/Integrations_thumb_0_0.png "Integration API Settings")](../../../Resources/Images/Auditor/Settings/Integrations.png)

Also, she enabled the ‘**Password Reset**’ alert from the Auditor predefined set of alerts and specified the add-on launch as response action.

![](../static/img/Auditor/Images/Auditor/Alerts/ResponseAction/Addon.png)

Then a new ticket is automatically created shortly after any account password is reset.

All necessary details about the case are automatically entered into the ConnectWise ticket (*Initial Description* ﬁeld), including the name of the workstation, the name of the account in question, and the time when the event occurred:

![](../static/img/Auditor/Images/Auditor/Addon/ConnectWise/ServiceBoard.png)