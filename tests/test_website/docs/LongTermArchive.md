---
title: "Long-Term Archive"
sidebar_position: 861
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

# Long-Term Archive

The Long-Term Archive is configured by default, irrespective of your subscription plan and settings you specified when configuring a monitoring plan. To review and update your Long-Term Archive settings, navigate to **Settings** \> **Long-Term Archive** and click Modify.

[![](../static/img/Auditor/Images/Auditor/Settings/LTA_Settings_thumb_0_0.png)](../../../Resources/Images/Auditor/Settings/LTA_Settings.png)

Review the following for additional information:

| Option | Description |
| --- | --- |
| Long-Term Archive settings | |
| Write audit data to | Specify the path to a local or shared folder where your audit data will be stored. By default, it is set to *"C:\ProgramData\Netwrix Auditor\Data"*.  By default, the LocalSystem account is used to write data to the local-based Long-Term Archive and computer account is used for the file share-based storage.  Subscriptions created in the Auditor client are uploaded to file servers under the Long-Term Archive service account as well.  It is not recommended to store your Long-Term Archive on a system disk. If you want to move the Long-Term Archive to another location, refer to the following Netwrix Knowledge base article: [How to move Long-Term Archive to a new location](`https://helpcenter.netwrix.com/bundle/z-kb-articles-salesforce/page/kA00g000000H9SSCA0.html` "How to move Long-Term Archive to a new location"). |
| Keep audit data for (in months) | Specify how long data will be stored. By default, it is set to 120 months. |
| Use custom credentials (for the file share-based Long-Term Archive only) | Select the checkbox and provide user name and password for the Long-Term Archive service account.  You can specify a custom account only for the Long-Term Archive stored on a file share.  The custom Long-Term Archive service account can be granted the following rights and permissions:   * Advanced permissions on the folder where the Long-term Archive is stored:   + List folder / read data   + Read attributes   + Read extended attributes   + Create files / write data   + Create folders / append data   + Write attributes   + Write extended attributes   + Delete subfolders and files   + Read permissions * On the file shares where report subscriptions are saved:    + Change share permission   + Create files / write data folder permission Subscriptions created in the Auditor client  are uploaded to file servers under the Long-Term Archive service account as well. See the [Subscriptions](../Subscriptions/Overview.htm "Subscriptions") topic for additional information. |

Setting Recording Settings

![](../static/img/Auditor/Images/Auditor/Settings/UserSessions_storage.png)

|  |  |
| --- | --- |
| Configure custom location of session recordings | Default location for storing session recordings is set to *"\\\\Netwrix_UAVR$"*. However, storing extra files on the Auditor  Server may produce additional load on it, so consider using this option to specify another location where session recordings will be stored. |
| Enter UNC path to shared folder: | Specify UNC path to the shared folder where user session video recordings will be stored. You can use server name or IP address, for example:  *\\172.28.6.33\NA_UserSessions*  Using a local folder for that purpose is not recommended, as storing extra files on the Auditor  Server will produce additional load on it.  Make sure the specified shared folder has enough capacity to store the video files.  Retention period for the video files can be adjusted in the related monitoring plan settings (targeted at User Activity data source); default retention is 7 days. See the [User Activity](../MonitoringPlans/UserActivity/Overview.htm "User Activity Plans") topic for additional information.  After you specify and save settings for session recordings, it is recommended that you leave them unchanged. Otherwise — if you change the storage location while using Netwrix Auditor for User Activity — please be aware of possible data loss, as Auditor  will not automatically move session recordings to a new location. |
| User name / Password | Provide user name and password for the account that will be used to store session recordings to the specified shared folder.  Make sure the account has at least the Write permission for that folder. |

Auditor  informs you if you are running out of space on a system disk where the Long-Term Archive is stored by default. You will see events in the Netwrix Auditor **System Health** log once the free disk space starts approaching minimum level. When the free disk space is less than 3 GB, the Netwrix services responsible for audit data collection will be stopped.