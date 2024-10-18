from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
import os
from dotenv import load_dotenv

class AzureWebAppHandler:
    def __init__(self):
        """Initialize with Azure Web App details and set up authentication."""
        load_dotenv()
        self.subscription_id = os.getenv('SUBSCRIPTION_ID')
        self.resource_group = os.getenv('RESOURCE_GROUP')
        self.web_app_name = os.getenv('WEB_APP_NAME')
        
        # Authenticate using Managed Identity or credentials from environment variables
        self.credential = DefaultAzureCredential()
        
        # Create the WebSiteManagementClient for interacting with Azure App Service
        self.client = WebSiteManagementClient(self.credential, self.subscription_id)

    def get_app_settings(self):
        """Retrieve the App Settings for the specified Azure Web App."""
        try:
            settings = self.client.web_apps.list_application_settings(self.resource_group, self.web_app_name)
            return settings.properties  # Returns the current app settings as a dictionary
        except Exception as e:
            print(f"Error retrieving App Settings: {e}")
            return None

    def update_app_setting(self, key, value):
        """Update a specific app setting (e.g., API_TOKEN) with a new value."""
        try:
            # Get the current app settings
            app_settings = self.client.web_apps.list_application_settings(self.resource_group, self.web_app_name)
            
            # Update the specific setting
            app_settings.properties[key] = value
            
            # Push the updated settings back to Azure
            self.client.web_apps.update_application_settings(self.resource_group, self.web_app_name, app_settings)
            print(f"Successfully updated {key} in App Settings.")
        except Exception as e:
            print(f"Error updating App Settings: {e}")

    def restart_web_app(self):
        """Restart the Azure Web App to apply any configuration changes."""
        try:
            self.client.web_apps.restart(self.resource_group, self.web_app_name)
            print("Successfully restarted the Azure Web App.")
        except Exception as e:
            print(f"Error restarting the Azure Web App: {e}")

if __name__ == '__main__':
    pass
