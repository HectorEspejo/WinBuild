import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_build_info(url, versions):
    # Send a request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the build information
    table = soup.find('table')

    # Check if a table was found and read it into a DataFrame using StringIO
    if table:
        html_content = StringIO(str(table))
        df = pd.read_html(html_content)[0]

        # Filter rows by specified versions, assuming 'Version' column exists
        filtered_df = df[df['Version'].isin(versions)]
        return filtered_df[['Version', 'Latest build']]  # Assuming 'Build' column exists
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no table is found

def fetch_build_info_WINSERVERS(url, release):
    # Send a request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Parse the response content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the build information
    table = soup.find('table')

    # Check if a table was found and read it into a DataFrame using StringIO
    if table:
        html_content = StringIO(str(table))
        df = pd.read_html(html_content)[0]

        # Filter rows by specified versions, assuming 'Windows Server release' column exists
        filtered_df = df[df['Windows Server release'].isin(release)]
        return filtered_df[['Windows Server release', 'Latest build']]  # Assuming 'Build' column exists
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no table is found


def main():
    urls_versions = {
        "Windows 11": ("https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information", ["23H2", "22H2", "21H2"]),
        "Windows 10": ("https://learn.microsoft.com/en-us/windows/release-health/release-information", ["22H2", "21H2"]),
    }

    url_server = {
        "Windows Server": ("https://learn.microsoft.com/en-us/windows/release-health/windows-server-release-info", ["Windows Server 2022", "Windows Server 2019 (version 1809)", "Windows Server 2016 (version 1607)"])
    }

    for name, (url, versions) in urls_versions.items():
        print(f"\nBuild Information for {name}:")
        try:
            build_info = fetch_build_info(url, versions)
            if not build_info.empty:
                print(build_info)
            else:
                print("No relevant build information found.")
        except Exception as e:
            print(f"Failed to fetch build info for {name}: {e}")

    for name, (url, release) in url_server.items():
        print(f"\nBuild Information for {name}:")
        try:
            build_info = fetch_build_info_WINSERVERS(url, release)
            if not build_info.empty:
                print(build_info)
            else:
                print("No relevant build information found.")
        except Exception as e:
            print(f"Failed to fetch build info for {name}: {e}")

if __name__ == "__main__":
    main()
