---
sidebar_position: 13
title: Getting Started
---

# Getting Started

The Access Information Center is installed with a Builtin Administrator account used to enable console access. Launch the Access Information Center using the desktop icon for the first time and set the password for the Builtin Administrator account. Then log in with that account. See the [First Launch](FirstLaunch "First Launch") topic for additional information.

## Initial Configuration

Next, configure the Access Information Center for your environment:

* Console Users — Grant users access to the application starting with an Administrator account. There are five levels of access: Administrator, Security Team, Reader, Data Privacy, and User Access Administrator. See the [Console Access Page](Configuration/ConsoleAccess "Console Access Page") topic for information.

  * Optionally, disable the Builtin Administrator account. See the [Modify the Builtin Administrator Account](Configuration/ConsoleAccess#Modify "Modify the Builtin Administrator Account") topic for additional information.
* Active Directory Service Account — Provide the service account to be used for accessing Active Directory. Optionally, enable the application to make group membership changes. See the [Active Directory Page](Configuration/ActiveDirectory "Active Directory Page") topic for information.
* Notification — Configure the Notification settings required in order for the application to send email. See the [Notifications Page](Configuration/Notifications "Notifications Page") topic for information.

## Enable Console Users

Access Information Center users granted one of the available roles should be notified.

***RECOMMENDED:*** The notification should include:

* Why your organization is using the Access Information Center
* What they will be doing in the Access Information Center
* How to log into the Access Information Center, specifically what URL and credentials to use

You should also provide links to the appropriate topics based on the user's role:

* Reader and Data Privacy — Send the URL link for the [Resource Audit Overview](../ResourceAudit/Overview "Resource Audit Overview") topic
* Security Team — Need topics that align to the work the will be doing in the Access Information Center:

  * Accessing Resource Audits — Send the URL link for the [Resource Audit Overview](../ResourceAudit/Overview "Resource Audit Overview") topic
  * Ownership Administrator — Send the URL link for the [Resource Owners Overview](../ResourceOwners/Overview "Resource Owners Overview") topic
  * Review Administrator — Send the URL link for the [Resource Reviews Overview](../ResourceReviews/Overview "Resource Reviews Overview") topic
  * Request Administrator — Send the URL link for the [Access Requests Overview](../AccessRequests/Overview "Access Requests Overview") topic
* Administrator — Send the URL link for the [Administrator Overview](Overview "Administrator Overview") topic
* User Access Administrator — Send the URL link for the [Console Access Page](Configuration/ConsoleAccess "Console Access Page") topic

## Resource Ownership Configuration

It is possible to enable business owners and data custodians to manage their resources through the application. Also, ownership of resources must be assigned in order to use the Resource Reviews and Access Requests workflows.

* Resource Ownership — Assign ownership for resources to be managed through the application. See the [Resource Owners Interface](../ResourceOwners/Interface "Resource Owners Interface") topic for additional information.
* Enable Owners — Send a notification to your owners about resource ownership with the application. See the [Notification to Owners](../ResourceOwners/Overview#Notifica "Notification to Owners") topic for additional information.

## Resource Review Workflow

The Access Information Center can be configured to run Resource Reviews, or attestations. All resources to be included in reviews must be assigned owners on the Resource Owners interface. The workflow consists of:

* Resource Reviews — Configure reviews for Access, Membership, Permissions, or Sensitive Data
* Owner Performs Review — Owners process the review, potentially recommending changes
* Review Administrator Approval — Review and process owner recommended changes

***RECOMMENDED:*** Set expectations for response time from owners.

Reviews can be run multiple times, maintaining a historical record for each instance. See the [Resource Reviews Overview](../ResourceReviews/Overview "Resource Reviews Overview") topic for additional information.

## Access Requests Workflow

The Access Information Center can be configured for access request by domain users. All resources to be available for requests must be assigned owners on the Resource Owners interface. The workflow consists of:

* Enable Domain Users — Send a notification to your domain users about access requests with the Access Information Center. See the [Notification to Domain Users](../AccessRequests/Overview#Notifica "Notification to Domain Users") topic for additional information.
* Owner Response — Set expectations for response time from owners

See the [Access Requests Overview](../AccessRequests/Overview "Access Requests Overview") topic for additional information.