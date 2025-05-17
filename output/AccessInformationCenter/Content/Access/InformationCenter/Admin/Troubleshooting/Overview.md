---
sidebar_position: 295
title: Troubleshooting
---

# Troubleshooting

The following are several troubleshooting tips which can assist with diagnosing trouble with the Access Information Center. If engaging with [Netwrix Support](https://www.netwrix.com/support.html "Netwrix Support"), it will be useful to be aware of these.

Service Account Delegation

Delegation can be used to grant the Active Directory service account the minimal rights necessary to allow the Access Information Center to commit changes in Active Directory. See the [Service Account Delegation](Delegation "Service Account Delegation") topic for additional information.

Log File

By default the Access Information Center is configured to log at the Error level. When requested by Netwrix Support, you can enable Debug level from the Diagnostics page of the Configuration interface. See the [Diagnostics Page](../Configuration/Diagnostics "Diagnostics Page") topic for additional information.

If a different log level is needed or desired, the `aic.log` file can be modified. See the [Change Log Level](LogLevel "Change Log Level") topic for additional information.

Credential Password Changes

The Access Information Center uses several different types of service accounts. If a credential password for one of these accounts is no longer valid, it will impact application functionality. Additionally, if the Builtin Administrator account remains enabled, it may be necessary to reset the password. See the [Update Credential Passwords](CredentialPasswords "Update Credential Passwords") topic for additional information.