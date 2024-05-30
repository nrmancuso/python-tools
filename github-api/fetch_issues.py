import requests
import json

# Replace with your own GitHub repository details
owner = 'checkstyle'
repo = 'checkstyle'
# Number of issues per page (max 100)
per_page = 30
# Starting page
page = 1
# Label to filter issues
label = 'your-label'

# Optional: If you want to use authentication (recommended for higher rate limits)
# Create a GitHub personal access token at https://github.com/settings/tokens
token = 'your-github-personal-access-token'

headers = {
    # Authorization header with personal access token
    # 'Authorization': f'token {token}'
}


# Function to fetch issues from GitHub
def fetch_issues(repo_owner, repo_name, issues_per_page, start_page, filter_label):
    issues_json_pages = []
    current_page = start_page
    while True:
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
        params = {
            # State of issues ('open', 'closed', or 'all')
            'state': 'all',
            # Number of issues per page
            'per_page': issues_per_page,
            # Current page number
            'page': current_page,
            # Filter by label
            # 'labels': filter_label
            'pulls': 'false'
        }
        response = requests.get(url, headers=headers, params=params)
        # log response
        print(f'response json: {json.dumps(response.json(), indent=2)}')
        if response.status_code != 200:
            # Print an error message if the request fails
            print(f"Failed to fetch issues: {response.status_code}")
            break
        page_issues = response.json()
        if not page_issues:
            # Break the loop if there are no more issues
            break
        # Extend the issues list with the issues from the current page
        issues_json_pages.extend(page_issues)
        # Move to the next page
        current_page += 1
    return issues_json_pages


# Fetch the issues
issues = fetch_issues(owner, repo, per_page, page, label)

# Print the issues in JSON format
print(json.dumps(issues, indent=2))
