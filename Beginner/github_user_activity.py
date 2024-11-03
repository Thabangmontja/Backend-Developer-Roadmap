import sys
import json
import urllib.request

def fetch_Github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = json.loads(response.read())
                print(f"Recent activity for Github user '{username}':")

                for event in data[:5]:  # Limit to recent 5 activities for simplicity
                    event_type = event.get("type")
                    repo_name = event["repo"]["name"]
                    print(f"- {event_type.replace('Event', '')} in {repo_name}")

            else:
                print(f"Failed to fetch data :( Please try again.")
    except urllib.error.HTTPError as e:
        print(f"Error: {e.reason} (Status Code: {e.code})")
    except urllib.error.URLError:
        print("Network error. Please check your connection.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: github-activity <username>")
        return

    username = sys.argv[1]
    fetch_Github_activity(username)

if __name__ == "__main__":
    main()