import asyncio
from playwright.async_api import async_playwright
from prompt import get_hint_from_huggingface
from email_sender import send_email, clean_html

async def get_leetcode_potd():
    query = {
        "operationName": "questionOfToday",
        "variables": {},
        "query": """
            query questionOfToday {
              activeDailyCodingChallengeQuestion {
                date
                link
                question {
                  acRate
                  difficulty
                  freqBar
                  frontendQuestionId: questionFrontendId
                  isFavor
                  isPaidOnly
                  status
                  title
                  titleSlug
                  hasVideoSolution
                  hasSolution
                  topicTags {
                    name
                    id
                    slug
                  }
                }
              }
            }
        """
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to any page to initialize the browser session
        await page.goto("https://leetcode.com/problemset/all/", wait_until="domcontentloaded")

        # Send the GraphQL request using browser context
        response = await page.evaluate("""
        async (query) => {
            const res = await fetch("https://leetcode.com/graphql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(query)
            });
            return res.ok ? await res.json() : { error: res.status };
        }
        """, query)

        await browser.close()

    if "data" in response:
        data = response["data"]["activeDailyCodingChallengeQuestion"]
        return data["question"]["titleSlug"]
    else:
        print("❌ Error:", response)
        return None


async def get_problem_description(title_slug):
    query = {
        "operationName": "getQuestionDetail",
        "variables": {"titleSlug": title_slug},
        "query": """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            content
            codeSnippets {
              lang
              langSlug
              code
            }
            sampleTestCase
            metaData
            title
            titleSlug
            difficulty
            topicTags {
              name
              slug
            }
          }
        }
        """
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(f"https://leetcode.com/problems/{title_slug}/", wait_until="domcontentloaded", timeout=10000)

        response = await page.evaluate("""
        async (query) => {
            const res = await fetch("https://leetcode.com/graphql", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(query),
            });
            return res.ok ? await res.json() : {error: res.status};
        }
        """, query)

        await browser.close()

    if "data" in response:
        data = response["data"]["question"]
        return data
    else:
        print("❌ Error fetching problem:", response)
        return None


# Main async function that runs both tasks sequentially
async def main():
    # Get the problem of the day and its titleSlug
    title_slug = await get_leetcode_potd()
    
    if title_slug:
        print(f"\nFetching detailed information for the problem: {title_slug}...\n")
        problem = await get_problem_description(title_slug)
        if problem:
            hint = get_hint_from_huggingface(title_slug, clean_html(problem["content"]))
            send_email(problem, hint, recipient_email="aamirbaugwala@gmail.com")

# Run the entire flow
asyncio.run(main())
