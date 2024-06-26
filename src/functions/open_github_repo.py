import os
import requests


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def run(repo_name: str) -> str:
    """README.mdとレポジトリのdescriptionを取得します"""
    if not GITHUB_TOKEN:
        return "GITHUB_TOKENが設定されていません。"

    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    repo_response = requests.get(
        f"https://api.github.com/repos/{repo_name}", headers=headers
    )
    readme_response = requests.get(
        f"https://api.github.com/repos/{repo_name}/readme", headers=headers
    )

    if repo_response.status_code == 200 and readme_response.status_code == 200:
        repo_data = repo_response.json()
        readme_data = readme_response.json()
        description = repo_data.get("description", "説明はありません。")
        readme_content = requests.get(readme_data["download_url"]).text
        return {
            "description": description,
            "readme": readme_content,
        }
    else:
        return "Repository not found."
