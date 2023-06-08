from settings import ApplicationSettings
from site_API.utils.site_api_handler import SiteApiInterface

app_settings = ApplicationSettings()

URL = f'https://{app_settings.site_api_host}'

HEADERS = {
    'content-type': 'application/octet-stream',
    'X-RapidAPI-Key': app_settings.site_api_key.get_secret_value(),
    'X-RapidAPI-Host': app_settings.site_api_host
}

site_api_interface = SiteApiInterface(URL, HEADERS)
