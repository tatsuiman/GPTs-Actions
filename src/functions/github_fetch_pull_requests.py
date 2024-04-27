import os
import requests


def run(repo_name, github_token, status="open"):
    results = []
    if not github_token:
        return "GITHUB_TOKENが設定されていません。"

    # GitHub APIのURLを組み立てる
    url = f"https://api.github.com/repos/{repo_name}/pulls?state={status}"

    # 認証ヘッダーを設定
    headers = {"Authorization": f"token {github_token}"}

    # GitHub APIを呼び出す
    response = requests.get(url, headers=headers)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        # 成功した場合は、JSONデータを取得して返す
        for resp in response.json():
            assignee = resp["assignee"]["login"] if resp["assignee"] else None
            labels = [label["name"] for label in resp["labels"]]
            results.append(
                {
                    "url": resp["html_url"],
                    "title": resp["title"],
                    "created_at": resp["created_at"],
                    "updated_at": resp["updated_at"],
                    "assignee": assignee,
                    "labels": labels,
                }
            )
        return results
    else:
        # エラーが発生した場合は、エラーメッセージを返す
        return f"APIからエラーが返されました。ステータスコード: {response.status_code}"
