---
sidebar_position: 15
title: SharePoint Online
---

Filter: 

* All Files

Submit Search

# SharePoint Online

You can use the SharePoint Online integration for the report (Activity and Risk Assessment Dashboard) subscriptions. This way, the required reports shall be delivered to a specific folder in SharePoint Online.

| Icon | Description |
| --- | --- |
|  | Edit Icon. Click the Edit Icon to edit the settings of the integration type. |
|  | Bin Icon. Click the Bin icon to delete the SharePoint Online integration. |

## Add a SharePoint Online Integration in a System

Follow the steps to add the SharePoint Online integration in Netwrix 1Secure.

**Step 1 –** Go to Configuration > **Integrations** and click the **Add** icon to add the SharePoint integration.

![Integration type pane](../../Resources/Images/1Secure/IntegrationTypeWindow.png "Integration type pane")

**Step 2 –** In the displayed Integration type window, click **SharePoint Online** and click **Next**.

![Configure connection pane](../../Resources/Images/1Secure/IntegrationConfigureConnectionSharePoint.png "Configure connection pane")

**Step 3 –** In the Configure connection window, specify the required fields:

* Client ID – The client ID of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.
* Tenant ID – The tenant ID of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.
* Client Secret – The client secret of the app registered in Microsoft Entra ID. See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.

See the [App Registration and Configuration in Microsoft Entra ID](../Configuration/EntraID/RegisterConfig "App Registration and Configuration in Microsoft Entra ID") topic for additional information.

**Step 4 –** Click **Finish**.

**NOTE:** You must firstly add a Sites.ReadWrite.All permission in your Microsoft Entra admin center. See the  [Microsoft 365 Permissions](../Configuration/EntraID/Permissions#Grant%20Permissions%20to%20the%20Registered%20Application "Microsoft 365 Permissions") topic for additional information.

The SharePoint Online integration is added now. The status displays "Ok" in green.

![Integrations list](../../Resources/Images/1Secure/IntegrationsSharePointOnline.png "Integrations list")

You can click the **Edit** icon or the **Bin** icon to edit or delete the integration.

See the [Subscriptions](../Admin/SearchAndReports/Subscriptions "Subscriptions") and [Risk Assessment Dashboard](../Admin/RiskProfiles/RiskAssessmentDashboard "Risk Assessment Dashboard") topics to learn how to add subscriptions and deliver it to SharePoint Online folder.