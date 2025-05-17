---
sidebar_position: 7
title: Install Agent
---

Filter: 

* All Files

Submit Search

# Install Agent

This topic describes an installation of the agent for collecting the data from your sources. Prior to installing the agent, ensure that all installation requirements have been met. See the [Netwrix Cloud Agent Software Requirements](../Requirements/CloudAgentRequirements "Agent Software Requirements") topic for additional information.

## Configure Netwrix Cloud Agent

To collect the data from the Computer and Active Directory you will need to install and configure the Netwrix Cloud Agent.

Follow the steps to configure an agent.

**Step 1 –** In the Netwrix 1Secure Website, go to Home page and select the Add organization icon to add an organization. Specify the name of the organization, timezone, country, and tags.

**Step 2 –** Click **Save**.

**Step 3 –** On the Agent Config panel, select **Download Agent** to start downloading agent for analyzing your data.

**Step 4 –**  Complete the [Install the Agent](#Install "Install the Agent") steps. Ensure you tick Launch Netwrix Cloud Agent Configuration tool and click Finish.

![](../../Resources/Images/1Secure/Organization_CloudAgent.png)

**Step 5 –** On the displayed Netwrix Cloud Agent Configuration screen, select Configure to configure with Netwrix Cloud Agent.

![](../../Resources/Images/1Secure/InstallAgent_CopyAgent.png)

**Step 6 –**  Go back to your Netwrix 1Secure configuration panel and copy the agent connection details by selecting Copy Connection String. This information will be used for agent deployment.

![](../../Resources/Images/1Secure/CloudAgent_CopyAgent.png)

**Step 7 –**  Paste the information in the Netwrix Cloud Agent Configuration that you copied earlier and save settings.

**NOTE:** The agent status has changed to **Connected** (green).

**Step 8 –** Go back to the Netwrix 1Secure configuration panel and select **Retry connecting to the client**. The agent status shall change to Healthy.

## Install the Agent

Follow the steps to install the agent.

**Step 1 –** Check the prerequisites.

**Step 2 –** Download the agent installer while adding the organization.

![](../../Resources/Images/1Secure/Organization_CloudAgentSetup1.png)

**Step 3 –** Click **Next** to continue.

![](../../Resources/Images/1Secure/InstallNetwrixCloudAgent.png)

**Step 4 –** Specify the installation folder and click **Next** to continue.

![](../../Resources/Images/1Secure/InstallAgentNetwrixCloudAgentReady.png)

**Step 5 –** Click **Install**. The agent starts the installation process.

![](../../Resources/Images/1Secure/InstallAgentNetwrixCloudAgentInstalling.png)

![](../../Resources/Images/1Secure/InstallAgentNetwrixCloudAgentFinish.png)

**Step 6 –** Keep the **Launch Netwrix Cloud Agent Configuration** tool checkbox selected and click Finish to complete the setup.