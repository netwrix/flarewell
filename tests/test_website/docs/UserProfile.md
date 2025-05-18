---
title: "Review User Profiles and Process Anomalies"
sidebar_position: 893
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

# Review User Profiles and Process Anomalies

The user profile enables you to investigate user behavior and take a closer look at anomalies.

To view a user profile

* On the Behavior Anomalies assessment dashboard, locate a user and click View Profile next to his or her name.

[![](../static/img/Auditor/Images/Auditor/BehaviorAnomalies/UserProfile_thumb_0_0.png)](../../../Resources/Images/Auditor/BehaviorAnomalies/UserProfile.png)

The user profile page contains the following sections:

* User data with the name and the total risk score. Click Show user activity below the total risk score, to launch the Interactive Search in a new window. Use it to see all user actions, including those that were not treated as anomalies.
* The Risk score timeline that demonstrates anomalous activity surges. Modify the timeframe to narrow down the results.
* The Risk score by top five alerts chart that outlines the most frequent anomalies provoked by user. To see the chart, click the pie chart icon in the upper left corner of the page.
* The anomalies list displays details for each anomaly: the alert that was triggered, the date and time, the risk score and anomaly status.

  Double-click an entry to see more details: who did what, when and where the action was made, etc. Navigate to Linked actions and click Show user activity or Show this activity record to invoke Interactive Search and see all user actions or a specific action correspondingly.

Netwrix Auditor shows only the top 2,000 anomalies. Modify the timeframe or hide reviewed anomalies, and then click Refresh to see more anomalies.

## Process Anomalies and Reduce Risk Score

By default, the anomaly status is active and it indicates that the incident still requires some examination or is kept for further investigation. As you inspect anomalies and respond to threats, update statuses and add comments.

To change an anomaly status

1. Specify an anomaly from the list and click the Active link in the Status column.
2. In the Change Status dialog, set the status to *"reviewed"* and provide a justification.

   You can add comments without changing a status. This might be helpful if the anomaly remains active for a long period of time and you need even more time to examine it closely.

[![](../static/img/Auditor/Images/Auditor/BehaviorAnomalies/ChangeStatus_thumb_0_0.png)](../../../Resources/Images/Auditor/BehaviorAnomalies/ChangeStatus.png)

Once the anomaly is reviewed, it disappears from the timeline and chart, and its associated risk score is taken from user's total score. The reviewed anomalies supplement the status with the reviewer name and date (e.g., *Reviewed by CORP\Administrator (10/02/2017 10:12:03 AM)*).

You can always revert changes and assign the Active status back.

To process all anomalies

* In the Actions section, select Mark all as reviewed.

In this case, all anomalies that are currently in view will be set to *"reviewed"*. Perform this operation only with a proper justification. Since Netwrix Auditor shows only the top 2,000 anomalies, make sure to click Refresh to check if there are more anomalies to be reviewed.

The anomalies that are excluded from view by filters are not affected by the Mark all as reviewed action.

## Customize Anomalies List

By default, all anomalies are in view. The Filters section helps you show or hide anomalies.

Click Customize view and clear the checkboxes next to alert names, if you do not want to see anomalies associated with them.

When you hide an alert from view, its associated anomalies will no longer be displayed on a timeline, chart, or in the list but the user total score will remain unchanged. Note that hidden anomalies cannot be reviewed in bulk with the Mark all as reviewed action.

Hide reviewed anomalies enables you to modify the anomalies list so that you can focus on active anomalies only. To see reviewed anomalies, click Show reviewed anomalies.