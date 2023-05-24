from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.agents import AgentType
from langchain.utilities.zapier import ZapierNLAWrapper
from langchain.callbacks import get_openai_callback

import os
from dotenv import load_dotenv

load_dotenv()

# get from https://platform.openai.com/
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# get from https://nla.zapier.com/demo/provider/debug (under User Information, after logging in): 
os.environ["ZAPIER_NLA_API_KEY"] = os.getenv('ZAPIER_NLA_API_KEY')

llm = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(toolkit.get_tools(), llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def get_prompt(email, name, review):
    prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer {name} whose email id is {email}.
Given the customer email delimited by triple backticks, \
Generate a reply to thank the customer for their review.
If the review is positive or neutral, thank them for \
their review.
If the review is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.

Format email in standard format.

Customer review: ```{review}```
"""
    return prompt

email = "harshkesharwani777@gmail.com"
name = "harsh"
review = "After 48 hours of usage,i really love it, top notch display,battery, performance and UI. Beautiful and gorgeous design especially from the back. Just a bit weak camera but the pro mode and 50MP does the job! Video filiming is also very good.With latest MiUi 13 update. Many bugs have been fixed. Only small warming issue after charging but that's okay enough. Highly recommended to buy this phone,but if better budget,go for poco M4 5g Pro or Poco X4 and if small budget go for Poco M4 5G!Very good phone!"

def send_email(email, name, review):
   with get_openai_callback() as cb:
       try:
          response = agent.run(get_prompt(email, name, review))
       except ValueError as e:
          response = str(e)
          if not response.startswith("Could not parse LLM output: `"):
            raise e
          response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
       print(response)
       print(f"Total Tokens: {cb.total_tokens}")
       print(f"Prompt Tokens: {cb.prompt_tokens}")
       print(f"Completion Tokens: {cb.completion_tokens}")
       print(f"Total Cost (USD): ${cb.total_cost}")