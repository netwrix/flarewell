---
sidebar_position: 149
title: Sensitive Content Report
---

# Sensitive Content Report

The Sensitive Content report at the site collection, site, list, library, and folder levels provides a list of files and a hit count per file where criteria matches were found on the selected resource. This report includes a Matches table.

![Sensitive Content report at the site collection, site, list, library, and folder levels](../../../../../../../../static/Content/Resources/Images/Access/InformationCenter/ResourceAudit/SharePoint/SiteSensitiveContent.png "Sensitive Content report at the site collection, site, list, library, and folder levels")

This report is comprised of the following columns:

* Criteria Name – Type of potentially sensitive criteria matches found
* Criteria Type – Pattern for pattern based matches (System Criteria), and subject type based on Subject Profile matches (for example, Customer, Employee, and so on)
* Path – Location of the file where the criteria matches were found
* Sub File – File name if the sensitive data files reside in a PST file or a ZIP file
* Count – Number of criteria matches found within each file
* Attributes – Comma separated list of Attributes found for the identity

There is one table at the bottom displaying Matches in the files where the selected criterion value were found:

* Prefix – Text just prior to the sensitive data match in the file
* Match – Lists any sensitive data matches found for the highlighted criteria in the top grid of the report
* Suffix – Text just after the sensitive data match in the file
* Sub File – File name if the sensitive data files reside in a PST file or a ZIP file

**NOTE:** Up to five matches per file can be displayed.