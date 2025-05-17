---
sidebar_position: 98
title: Flexible Imports Feature
---

# Flexible Imports Feature

Flexible imports allow an Access Information Center user to view reports on permissions, activity, and sensitive content from sources or data not reported in the Access Information Center by default. Access Analyzer users can query any supported system for this type of information and import it into Access Information Center tables to display information in the Access Information Center. With flexible imports, the Access Information Center provides a single view of entitlements across any set of systems and applications.

The flexible imports feature populates the following Access Analyzer database tables, which enable Access Information Center to access the data for reports:

* SA\_AIC\_FlexibleActivityEvents table
* SA\_AIC\_FlexibleHosts table
* SA\_AIC\_FlexibleLocalGroupMembership table
* SA\_AIC\_FlexiblePermissions table
* SA\_AIC\_FlexibleResources table
* SA\_AIC\_FlexibleSddMatches table
* SA\_AIC\_FlexibleSddMatchHits table

Imported data reports are accessed through the Resource Audit interface. Explore the resources by expanding the levels within the Resources pane and selecting the desired resource. These reports identify the following information in the targeted environment:

* Permissions applied to a particular resource
* What trustees are doing with their access
* What potentially sensitive data exists across the targeted environment