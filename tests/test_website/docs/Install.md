---
title: "Install Add-On"
sidebar_position: 840
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

# Install Add-On

After downloading the add-on package from Netwrix add-on store, copy it to the a computer where the Auditor Server resides. Unpack the ZIP archive to a folder of your choice; by default, it will be unpacked to the **Netwrix_Auditor_Add-on_for_ITSM** folder.

The main component of the add- on is implemented as a service named Netwrix Auditor **ITSM Integration Service**. This service will run on the computer where the Auditor Server works, and will use the default Integration API port **9699**. Unless specified, the service will run under the **LocalSystem** account.

To use the add-on, you should check the prerequisites and specify configuration settings, as described in the next sections. After that, run the installer that will apply settings and start the service. See the [Deploy the Service](Deployment.htm "Deploy the Service") topic for additional information.