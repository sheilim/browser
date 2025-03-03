import asyncio

from browser_use.browser.browser import Browser
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use.browser.context import BrowserContext, BrowserContextConfig

config = BrowserContextConfig(
    cookies_file="./cookies.json",
)

browser = Browser()

context = BrowserContext(browser=browser, config=config)

from browser_use import Agent

load_dotenv()

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
task = 'login to facebook with user saddy.madrid@kubernesis.io and teamoDIOS14327! and search Saddy Madrid. after generate report with the results'

agent = Agent(task=task, llm=llm, browser_context=context)


async def main():
	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
