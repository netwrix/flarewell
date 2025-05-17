---
sidebar_position: 187
title: Sensitive Content Report
---

# Sensitive Content Report

The Sensitive Content report at the NFS Exports share and subfolder levels provides a list of files and a hit count per file where criteria matches were found on the selected resource. This report includes a table with criteria matches visible to Access Information Center users with either Administrator or Security Team roles. The Matches table requires the **store discovered sensitive data** configuration for the Access Analyzer data collection or it will be blank.

![Sensitive Content report at the NFS Exports share and subfolder levels](../../../../../../../../static/Content/Resources/Images/Access/InformationCenter/ResourceAudit/FileSystem/NFSSensitiveContent.png "Sensitive Content report at the NFS Exports share and subfolder levels")

This report is comprised of the following columns:

* Criteria Name – Type of potentially sensitive criteria matches found
* Path – Location of the file where the criteria matches were found
* Count – Number of criteria matches found within each file

There is one table at the bottom displaying Matches in the files where the selected criterion value were found.

* Prefix – Text just prior to the sensitive data match in the file
* Match – Lists any sensitive data matches found for the highlighted criteria in the top grid of the report
* Suffix – Text just after the sensitive data match in the file
* Sub File – File name if the sensitive data files reside in a PST file or a ZIP file

**NOTE:** Up to five matches per file can be displayed.