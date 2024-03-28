import os
import logging
from github import Github, GithubException

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def run(keyword: str, lang: str = None, org: str = None) -> str:
    g = Github(GITHUB_TOKEN)
    try:
        # IssueやPRとソースコードを検索
        if org is not None:
            org_query = f"org:{org}"
        else:
            org_query = ""
        lang_query = f"language:{lang}" if lang is not None else ""
        issue_query = f"{keyword} in:title,body {lang_query} {org_query}".strip()
        pr_query = f"{keyword} in:title,body,type:pr {lang_query} {org_query}".strip()
        code_query = f"{keyword} in:file {lang_query} {org_query}".strip()
        logging.info(f"Issue query: {issue_query}")
        logging.info(f"PR query: {pr_query}")
        logging.info(f"Code query: {code_query}")
        issue_results = list(g.search_issues(issue_query, state="all").get_page(0))
        pr_results = list(g.search_issues(pr_query, state="all").get_page(0))
        code_results = list(g.search_code(code_query).get_page(0))

        results = "# Githubの検索結果\n"
        # Issueの結果を追加
        for issue in issue_results:
            results += f"* [{issue.title}]({issue.html_url})\n"
        # PRの結果を追加
        for pr in pr_results:
            results += f"* [{pr.title}]({pr.html_url})\n"
        # コードの結果を追加
        for code in code_results:
            results += f"* [{code.repository.full_name}/{code.path}]({code.html_url})\n"

        if len(issue_results) == 0 and len(pr_results) == 0 and len(code_results) == 0:
            return "Githubの検索結果は何も見つかりませんでした。"
        else:
            results += "※URLやレポジトリの概要を確認してください。"
            return results
    except GithubException as e:
        return f"Github APIエラー: {e.data['message']}"


if __name__ == "__main__":
    keyword = "openai"
    print(run(keyword))
