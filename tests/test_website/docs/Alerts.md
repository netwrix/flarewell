---
title: "Integrate Alerts with Add-On"
sidebar_position: 838
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

# Integrate Alerts with Add-On

The add-on is shipped with a special set of alerts developed by Netwrixindustry experts. These alerts are helpful for handling some routine cases that require service manager's attention, e.g., account lockouts, changes to administrative groups. The alerts have preset filters and can be easily uploaded to Auditor, and then integrated with the add-on and your ServiceNow system. These alerts have ITSM Addon prefix in their names.

Alternatively, you can integrate any default Auditor alert or your custom-built alerts with the addon.

By default, none of the alerts are integrated with add-on. To instruct the add-on to create tickets for alerts, you should enable integration. Netwrix provides a command-line tool for enabling integration with the add-on.

**NOTE:** Make sure to turn on alerting in Auditor. You should manually set the state to "**On**" for all alerts you want to integrate with the add-on.

Perform the following steps to integrate alerts with the add-on:

**Step 1 –** On the computer where the Auditor Server is installed, start the **Command Prompt** and run the **Netwrix.ITSM.AlertsUploaderTool.exe** tool. The tool is located in the add-on folder. For example:

C:\>cd C:\Add-on

C:\Add-on\Netwrix.ITSM.AlertsUploaderTool.exe

**Step 2 –** Execute one of the following commands depending on your task.

| To... | Execute... |
| --- | --- |
| Upload alert set shipped with the addon to Auditor | Netwrix.ITSM.AlertsUploaderTool.exe /UploadTemplates  Once uploaded, the alerts appear in the **All Alerts** list in Auditor, their names start with "*ITSM add-on*". Make sure to set their state to **"On**" (turn them on) manually. |
| Review alert list and their integration status | Netwrix.ITSM.AlertsUploaderTool.exe /List  You will see the full list of Auditor alerts, with an enabled or disabled integration status for each alert. |
| Enable integration | Netwrix.ITSM.AlertsUploaderTool.exe /Update "" Enable  where `` is the name of the alert you want to integrate with the add-on. Provide alert names as they appear in Auditor.  **NOTE:** You can enable integration with one alert at a time.  For example:  Netwrix.ITSM.AlertsUploaderTool.exe /Update "ITSM Add-On: User Account Locked Out" Enable |
| Disable integration | Netwrix.ITSM.AlertsUploaderTool.exe /Update "" Disable  where `` is the name of the alert for which you want to disable integration.  **NOTE:** You can disable integration with one alert at a time.  For example: Netwrix.ITSM.AlertsUploaderTool.exe /Update "ITSM Add-On: User Account Locked Out" Disable |