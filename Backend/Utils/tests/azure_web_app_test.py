from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient
from azure.core.exceptions import AzureError
from Utils.MAL_connection.azure_web_app_handler import AzureWebAppHandler

def test_get_app_settings():
    handler = AzureWebAppHandler()
    settings = handler.get_app_settings()
    
    if settings:
        print(f"App settings retrieved successfully: {settings}")
    else:
        print("Failed to retrieve app settings.")

def test_update_app_setting():
    handler = AzureWebAppHandler()
    key = "API_TOKEN"
    value = "new_test_token_value"
    
    handler.update_app_setting(key, value)

def test_restart_web_app():
    handler = AzureWebAppHandler()
    handler.restart_web_app()

def run_test():
    # Test each method one by one to ensure they work correctly
    print("Testing get_app_settings()")
    test_get_app_settings()

    print("\nTesting update_app_setting()")
    # test_update_app_setting()

    print("\nTesting restart_web_app()")
    # test_restart_web_app()



# if __name__ == '__main__':
#     # Test each method one by one to ensure they work correctly
#     print("Testing get_app_settings()")
#     test_get_app_settings()

#     print("\nTesting update_app_setting()")
#     # test_update_app_setting()

#     print("\nTesting restart_web_app()")
#     # test_restart_web_app()
