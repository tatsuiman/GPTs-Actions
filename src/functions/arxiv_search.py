import arxiv
import json


def run(query):
    results = {}
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 10 most recent articles matching the keyword "quantum."
    search = arxiv.Search(
        query=query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate
    )

    results = []
    for r in client.results(search):
        results.append(
            {
                "title": str(r.title),
                "summary": str(r.summary),
                "authors": [author.name for author in r.authors],
                "published": str(r.published),
                "updated": str(r.updated),
                "links": [link.href for link in r.links],
                "categories": r.categories,
            }
        )
    return json.dumps(results)


if __name__ == "__main__":
    print(run("AutoDev"))
