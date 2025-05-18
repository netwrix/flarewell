---
title: "Configure Removable Storage Media for Monitoring"
sidebar_position: 1043
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

# Configure Removable Storage Media for Monitoring

You can configure IT infrastructure for monitoring removable storage media both locally and remotely.

Review the following:

To configure removable storage media monitoring on the local server

1. On the target server, create the following catalog: *“%ALLUSERSPROFILE%\Netwrix Auditor\Windows Server Audit\ETS\”* to store event logs. [To review Event Trace Session objects' configuration](#Review_Configuration)how to modify the root directory.

   If you do not want to use the Netwrix Auditor for Windows Server Compression Service for data collection, make sure that this path is readable via any shared resource.

   After environment variable substitution, the path shall be as follows:

   *C:\ProgramData\Netwrix Auditor\Windows Server Audit\ETS*

   If your environment variable accesses another directory, update the path.
2. Run the Command Prompt as Administrator.
3. Execute the commands below.

   * To create the Event Trace Session object:

     `logman import -n "Session\NetwrixAuditorForWindowsServer" -xml ""`
   * To start the Event Trace Session object automatically every time the server starts:

     `logman import -n "AutoSession\NetwrixAuditorForWindowsServer" -xml ""`

     where:

     + `NetwrixAuditorForWindowsServer`—Fixed name the product uses to identify the Event Trace Session object. The name cannot be changed.
     + ``—Path to the Event Trace Session template file that comes with Netwrix Auditor. The default path is *"C:\Program Files (x86)\Netwrix Auditor\Windows Server Auditing\EventTraceSessionTemplate.xml"*.

To configure removable storage media monitoring remotely

1. On the target server, create the following catalog: *“%ALLUSERSPROFILE%\Netwrix Auditor\Windows Server Audit\ETS\”* to write data to. [To review Event Trace Session objects' configuration](#Review_Configuration)how to modify the root directory.

   If you do not want to use the Netwrix Auditor for Windows Server Compression Service for data collection, make sure that this path is readable via any shared resource.

   After environment variable substitution, the path shall be as follows:

   *\\\\c$\ProgramData\Netwrix Auditor\Windows Server Audit\ETS*

   If your environment variable accesses another directory, update the path.
2. Run the Command Prompt under the target server Administrator's account.
3. Execute the commands below.

   * To create the Event Trace Session object:

     `logman import -n "Session\NetwrixAuditorForWindowsServer" -xml "" -s `
   * To create the Event Trace Session object automatically every time the server starts:

     `logman import -n "AutoSession\NetwrixAuditorForWindowsServer" -xml "" -s `

     where:

     + `NetwrixAuditorForWindowsServer`—Fixed name the product uses to identify the Event Trace Session object. The name cannot be changed.
     + ``—Path to the Event Trace Session template file that comes with Netwrix Auditor. The default path is *"C:\Program Files (x86)\Netwrix Auditor\Windows Server Auditing\EventTraceSessionTemplate.xml"*.
     + ``—Name of the target server. Provide a server name by entering its FQDN, NETBIOS or IPv4 address.

To review Event Trace Session objects' configuration

An Administrator can only modify the root directory and log file name. Other configurations are not supported by Netwrix Auditor.

1. On the target server, navigate to Start → Administrative Tools → Performance Monitor.
2. In the Performance Monitor snap-in, navigate to Performance → Data Collectors Set → Event Trace Sessions.
3. Stop the NetwrixAuditorForWindowsServer object.
4. Locate the NetwrixAuditorForWindowsServer object, right-click it and select Properties. Complete the following fields:

   | Option | Description |
   | --- | --- |
   | Directory → Root Directory | Path to the directory where event log is stored. If you want to change root directory, do the following:  1. Under the Root directory option, click Browse and select a new root directory. 2. Navigate to *C:\ProgramData\Netwrix Auditor\Windows Server Audit* and copy the ETS folder to a new location. |
   | File → Log file name | Name of the event log where the events will be stored. |
5. Start the NetwrixAuditorForWindowsServer object.
6. In the Performance Monitor snap-in, navigate to Performance → Data Collectors Set → Startup Event Trace Sessions.
7. Locate the NetwrixAuditorForWindowsServer object, right-click it and select Properties. Complete the following fields:

   | Option | Description |
   | --- | --- |
   | Directory → Root Directory | Path to the directory where event log is stored. Under the Root directory option, click Browse and select a new root directory. |
   | File → Log file name | Name of the event log where the events will be stored. |