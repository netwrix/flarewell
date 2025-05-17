---
sidebar_position: 79
title: Add a Source and Connectors for Exchange Online
---

Filter: 

* All Files

Submit Search

# Add a Source and Connectors for Exchange Online

Follow the steps to add an Exchange Online data source and connector(s) to your organization.

**Step 1 –** Click **Configuration** in the top bar. The Managed organizations page is displayed, that lists the managed organizations defined in 1Secure.

**Step 2 –** Click an organization to define a data source and connector(s) for it. The properties page for the organization is displayed with the Sources tab selected by default.

**Step 3 –** On the Sources tab, click **Add** to add a source. The Select Data Source (Step 1 of 3) pane is displayed.

![Select Data Source (Step 1 of 3) pane](../../../../Resources/Images/1Secure/AddSources_Exchange.png "Select Data Source (Step 1 of 3) pane")

**Step 4 –** Select **Exchange Online** and click **Next**.

![Configure Source Details (Step 2 of 3) pane](../../../../Resources/Images/1Secure/ExchangeOnline_ConfigSourceDetails.png "Configure Source Details (Step 2 of 3) pane")

**Step 5 –** On the Configure source details (Step 2 of 3) pane, specify the following settings:

* Source Group – Specify a name for the group to which the data source will belong. Grouping sources, such as computers, allows them to share a common configuration and makes it easier to manage related sources together.
* Tenant ID – The tenant ID of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../../../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.
* Crawl Source – Toggle this option to ON to enable data collection for the source
* Credentials – Displays the crdentials that have already been added, while also providing the option to add new credentials. Netwrix 1Secure uses these credentials to connect to the data source. You can select existing credentials or add new ones. To add new credentials, select **Add new Credentials** from the drop-down menu or click the **Add** icon, then specify the following:

  * Client ID – The client ID of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../../../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.
  * Client Secret – The client secret of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../../../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.
  * Download Certificate – For certain connectors, such as SharePoint Online State, authentication requires a certificate instead of a client secret. Download this certificate and then upload it to the app registered in Microsoft Entra ID. See the [Upload a Certificate](../../../Configuration/EntraID/RegisterConfig#Upload "Upload a Certificate") topic for additional information.
  * Display Name – Specify a name you want to show for your credentials. It will be displayed on the Credentials tab of the Managed Organizations page.

**Step 6 –** Click **Next**.

![Choose new connector (Step 3 of 3) pane](../../../../Resources/Images/1Secure/AddSources_Exchange3.png "Choose new connector (Step 3 of 3) pane")

**Step 7 –** The Choose new connector pane (Step 3 of 3) lists one connector for Exchange Online. Specify the following:

* Exchange Online Activity – Toggle the **Exchange Online Activity** switch to ON to collect and monitor data for this connector. With this, you can generate activity reports on Exchange Online data. See the [Exchange Online](../../SearchAndReports/Activity#Exchange "Exchange Online") topic for additional information.

  * Collect non-owner mailbox audit data – Select this checkbox to collect data for the All Exchange Online Non-Owner Mailbox Access Events report. See the [Exchange Online](../../SearchAndReports/Activity#Exchange "Exchange Online") topic for additional information.

    **NOTE:** To collect the data for this report, you need to set up non-owner mailbox access auditing. See the [Settings for Non-Owner Mailbox Access Audit: Using Application](../../../Configuration/ExchangeOnlineNonOwner "Settings for Non-Owner Mailbox Access Audit: Using Application") topic for additional information.

**Step 8 –** Click **Finish**.

The Exchange Online data source and connector have been configured.