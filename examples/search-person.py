import asyncio

from browser_use.browser.browser import Browser
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from openai import OpenAI

config = BrowserContextConfig(
    cookies_file="./cookies.json",
)

browser = Browser()

context = BrowserContext(browser=browser, config=config)

from browser_use import Agent

load_dotenv()
#extend_system_message = "Your job is to generate a report including all the information obtained from the user.\nName, contacts, search snnipets (title, url, description) of each search performed"

# Initialize the model
llm = ChatOpenAI(
	model='gpt-4o',
	temperature=0.0,
)
# task = 'search in google site:facebook.com \"Saddy Madrid\", site:linkedin.com \"Saddy Madrid\", site:instagram.com \"Saddy Madrid\" and check person information and generate a report including all the information obtained from the user.\nName, contacts, search snippets (title, url, description) of each search performed'
task = 'search in google site:facebook.com \"Saddy Madrid\", site:linkedin.com \"Saddy Madrid\", site:instagram.com \"Saddy Madrid\" and check person information and generate a report including all the information obtained from the user.\nName, contacts, search snippets (title, url, description) of each search performed'

#agent = Agent(task=task, llm=llm, browser_context=context, extend_system_message=extend_system_message)
agent = Agent(task=task, llm=llm, browser_context=context)


async def main():
	try:
		result = await agent.run()
		content = result.extracted_content()
		print("Extracted content:")
		print(content)
		print("Final result:")
		finish_result = result.final_result()
		print(finish_result)
		client = OpenAI()
		completion = client.chat.completions.create(
			model="o3-mini",
			messages=[
				{"role": "user", "content": f"generame un perfil completo en markdown del usuario con esta infirmación, tambien determina que tan activo es en las redes sociales, cuando pasa mas activo, como contactarlo, relaciones con personas\n{content}\n{finish_result}"}
			],
			reasoning_effort="high"
		)
		print(completion.choices[0].message)
		# save the content in a file
		with open("profile.md", "w") as f:
			f.write(completion.choices[0].message.content)
		print("Profile saved to profile.md")
	finally:
		await browser.close()


if __name__ == '__main__':
	asyncio.run(main())
