---
sidebar_position: 19
title: Resource Reviews Overview
---

# Resource Reviews Overview

The Resource Reviews interface is where users with either the Security Team or Administrator role (to be referred to as Review Administrators) can manage reviews. The workflow provides a way for business users or data custodians (to be referred to as Owners) to attest to the access and privileges users have to their resources.

For the purpose of the Access Information Center, a “resource” refers to the file system shared folders, SharePoint sites, Active Directory (AD) groups, AD distribution lists, and/or local Administrators groups. All data available within the Access Information Center is collected by Netwrix Access Analyzer (formerly Enterprise Auditor) according to the targeted environments.

*Remember,* Owners are assigned to resources in the Resource Owners interface. Only resources with assigned Owners can be included in a Resource Review.

Who Can Run Resource Reviews (Review Administrators)?

* Console Users with Administrator role

  * Can complete the Review Administrator's approval process without impacting the visibility into the review created by a Review Administrator with the Security Team role

    **CAUTION:** Visibility into a review created by a Review Administrator with the Security Team role is blocked if a Review Administrator with the Administrator role starts a new instance.
* Console Users with Security Team role

  * Visibility into only those reviews personally created

Who Participates in Resource Reviews?

* Review Administrators — Create / start reviews and approve / process owner recommended changes
* Owners — Perform reviews and recommend changes

Types of Resource Reviews

There are four types of reviews:

* Access – Review user access rights to resources
* Membership – Review group membership
* Permissions – Review trustee permissions to resources
* Sensitive Data – Review files containing potentially sensitive data stored within resources

**NOTE:** The Sensitive Data content within reports and reviews is visible to all users and roles. The Matches table in the report will only be populated for Console User with Security Team and Administrator roles. This is also required for Sensitive Data reviews.

See the [Resource Reviews Interface](Interface "Resource Reviews Interface") topic for additional information.

Ignored Trustees

Trustees added to the SA\_AIC\_ResourceReviewIgnoredTrustees database table are excluded from Access, Membership, and Permissions reviews. For Membership and Permissions reviews, trustees must be directly excluded on an individual basis. Any members of excluded groups not directly referenced will still show in these reviews.

## Workflow of Resource Reviews

Prerequisites:

* Entitlement Reviews License
* The Access Information Center is configured to send Notifications. See the [Notifications Page](../Admin/Configuration/Notifications "Notifications Page") topic for additional information.

  **NOTE:** By default, the application is configured to send notifications only to the primary owner. However, this can be customized on the Configuration > Notifications page to send notifications to all assigned owners.
* Owners assigned to resources within the Resource Owners interface. See the [Resource Owners Overview](../ResourceOwners/Overview "Resource Owners Overview") topic for additional information.
* Sensitive Data reviews have specific requirements for Access Analyzer configuration. See the [Data Collection Prerequisites](Prerequisites#Data "Data Collection Prerequisites") topic for additional information.
* Optional: Access Information Center configured to commit AD changes. See the [Automation Prerequisites](Prerequisites#Automati "Automation Prerequisites ") topic for additional information.

Workflow:

***RECOMMENDED:*** When deploying the Access Information Center in an organization to process reviews, owners should be notified prior to launching the first set of reviews. See the [Notification to Owners](../ResourceOwners/Overview#Notifica "Notification to Owners") topic for additional information.

**Step 1 –** Review Administrator creates a review or starts a new review instance. See the [Create Review Wizard](Wizard/Create "Create Review Wizard") topic for additional information.

**Step 2 –** Owner performs a review. See the [Pending Reviews Page](PendingReviews#Pending "Pending Reviews Page") topic for additional information.

**Step 3 –** Review Administrator approves owner recommendations. See the [Approval Process](ApprovalProcess "Approval Process") topic for additional information.

**Step 4 –** Implement approved changes in your organization:

* Automatically, if the Access Information Center is configured to commit AD changes and access groups are assigned to the resources (limited to Access Information Center functionality)
* Manually, export a list of approved changes and deliver it to your IT department

When desired, the Review Administrator runs another instance of the review and the workflow starts again. See the [Review Instances](ReviewInstances "Review Instances") topic for additional information.