---
title: "Security"
sidebar_position: 705
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

# Security

By default, Netwrix Auditor API uses HTTPS for sending requests to its endpoints. Netwrix encrypts data with a self-signed automatically generated SSL certificate and strongly recommends you to replace it with a new secured certificate acquired from any reliable source.

The automatically generated Netwrix API certificate is located in the Personal store. To enable trust on remote computers, install this certificate in the Trusted Root Certification Authorities store.

[![](../static/img/Auditor/Images/Auditor/API/CertificateStore_thumb_0_0.png)](../../Resources/Images/Auditor/API/CertificateStore.png)

To manage API security settings with APIAdminTool.exe

Netwrix provides a command-line tool for managing Integration API. The tool allows switching between HTTP and HTTPS, assigning new certificates, etc.

1. On the computer where Auditor Server resides, start the Command Prompt and run the tool. The tool is located in the *Netwrix Auditor installation folder*, inside the *Audit Core* folder. For example:

   `C:\>cd C:\Program Files (x86)\Netwrix Auditor\Audit Core`

   `C:\Program Files (x86)\Netwrix Auditor\Audit Core>APIAdminTool.exe`
2. Execute one of the following commands depending on your task. Review the tips for running the tool:

   * Some commands require parameters. Provide parameters with values (parameter= value) if you want to use non-default. E.g., `APIAdminTool.exe api http port= 4431`.
   * Append `help` to any command to see available parameters and sub-commands. E.g., `APIAdminTool.exe api help`.

| To... | Execute... |
| --- | --- |
| Disable API | `APIAdminTool.exe api disable`  This command duplicates the checkbox on the Integrations page in Netwrix Auditor. |
| Switch to HTTP | `APIAdminTool.exe api http`  Netwrix recommends switching to HTTP only in safe intranet environments.  To use a non-default port (9699), append a parameter port with value to the command above (e.g., `port= 4431`). |
| Switch to HTTPS | `APIAdminTool.exe api https`  Run this command if you want to continue using Netwrix-generated certificate.  To use a non-default port (9699), append a parameter port with value to the command above (e.g., `port= 4431`). |
| Assign a new SSL certificate | `APIAdminTool.exe api https certificate`  Run this command if you want to apply a new certificate and use it instead default. You must add a certificate to the store before running this command.  Provide parameters to specify a certificate:   * For a certificate exported to a file:    + path—Mandatory, defines certificate location.   + store—Optional, defines the store name where certificate is located. By default, Personal. For example: `APIAdminTool.exe api https certificate path= C:\SecureCertificate.cef store= Personal` * For a self-signed certificate:    + subject—Mandatory, defines certificate name.   + validFrom—Optional, defines a certificate start date. By default, today.   + validTo—Optional, defines a certificate expiration date. By default, 5 years after a validFrom date. For example: `APIAdminTool.exe api https certificate subject= New validTo= 01/01/2024`  If you want to create a new self-signed certificate for a default period of 5 years from the current date: `APIAdminTool.exe api https certificate subject= "Netwrix Integration API"` * For a certificate specified using thumbprint:    + store—Optional, defines the store name where certificate is located. By default, Personal.   + thumbprint—Mandatory, defines a thumbprint identifier for a certificate. For example: `APIAdminTool.exe api https certificate thumbprint= 3478cda8586675e420511dc0fdf59078093eeeda` |