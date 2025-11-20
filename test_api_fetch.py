"""
Quick test to fetch data for ONE PR to verify the API works
"""
import requests
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', None)

# Test URL from your data
test_url = "https://github.com/getsentry/sentry/pull/85268"

# Parse URL
parts = test_url.split('/')
owner = parts[-4]  # getsentry
repo = parts[-3]   # sentry
pr_number = parts[-1]  # 85268

print(f"Testing API fetch for: {owner}/{repo}#{pr_number}")
print(f"GitHub token set: {'Yes' if GITHUB_TOKEN else 'No'}")

# Prepare headers
headers = {'Accept': 'application/vnd.github.v3+json'}
if GITHUB_TOKEN:
    headers['Authorization'] = f'token {GITHUB_TOKEN}'

# Fetch
api_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'
print(f"\nFetching: {api_url}")

response = requests.get(api_url, headers=headers, timeout=10)

print(f"Status code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    pr_author = data.get('user', {}).get('login', '')

    print("\n SUCCESS! PR Data:")
    print(f"   Title: {data.get('title', 'N/A')}")
    print(f"   Author: {pr_author}")
    print(f"   Additions: {data.get('additions', 0)}")
    print(f"   Deletions: {data.get('deletions', 0)}")
    print(f"   Changed files: {data.get('changed_files', 0)}")
    print(f"   Commments Total Count: {data.get('comments', 0)}")
    print(f"   Commits Total Count: {data.get('commits', 0)}")
    print(f"   State: {data.get('state', 'N/A')}")


    # Fetch comments breakdown
    comments_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'
    comments_response = requests.get(comments_url, headers=headers, timeout=10)

    if comments_response.status_code == 200:
        comments = comments_response.json()
        author_comments = sum(1 for c in comments if c.get('user', {}).get('login', '') == pr_author)
        reviewer_comments = len(comments) - author_comments

        print(f"\n Comments Breakdown:")
        print(f"   Total comments: {len(comments)}")
        print(f"   Author comments: {author_comments}")
        print(f"   Reviewer comments: {reviewer_comments}")

    # Fetch reviewers total count
    reviews_url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
    reviews_response = requests.get(reviews_url, headers=headers, timeout=10)

    if reviews_response.status_code == 200:
        reviews = reviews_response.json()
        # Get unique reviewers (excluding the PR author)
        unique_reviewers = set()
        for review in reviews:
            reviewer = review.get('user', {}).get('login', '')
            if reviewer and reviewer != pr_author:
                unique_reviewers.add(reviewer)

        print(f"\n👥 Reviewers Total Count:")
        print(f"   Unique reviewers: {len(unique_reviewers)}")
        if unique_reviewers:
            print(f"   Reviewers: {', '.join(list(unique_reviewers))}")
elif response.status_code == 403:
    print("\n Rate limit exceeded or forbidden")
    print("   You need a GitHub token!")
elif response.status_code == 404:
    print("\n PR not found")
else:
    print(f"\n Error: {response.status_code}")
    print(f"   {response.text[:200]}")

# Check rate limit
print("\n" + "="*50)
rate_url = 'https://api.github.com/rate_limit'
rate_response = requests.get(rate_url, headers=headers, timeout=10)
if rate_response.status_code == 200:
    rate_data = rate_response.json()
    core = rate_data['resources']['core']
    print(f" API Rate Limit:")
    print(f"   Remaining: {core['remaining']}/{core['limit']}")
    from datetime import datetime
    reset_time = datetime.fromtimestamp(core['reset'])
    print(f"   Resets at: {reset_time}")
