# Now the interface using gradio based on the previous code
# Import libraries
from bs4 import BeautifulSoup
import requests
import re
import cohere
import gradio as gr

# Bible site to scrape
bible_url = "https://www.biblegateway.com/passage/?search={}&version=NIV"

# Scrape the page
page = requests.get(bible_url.format("John")) # sample URL

# Extract the story text
soup = BeautifulSoup(page.content, 'html.parser')

# Extract the story text
story_text = soup.find('div', class_='passage-text').get_text()

# Preprocess the text
story_text = story_text.replace('\n', ' ')
story_text = re.sub(r'\s+', ' ', story_text)
story_text = story_text.strip()

# Set up Cohere API client
co = cohere.Client('q81O6CJT17c7qfSQc7U693xvFwAVf9rDhsjoHv2b')

# Define a function to query text with Cohere
def query_cohere(text, question):
  response = co.generate(
    prompt=f'Text: {text}\n\nQuestion: {question}', 
    max_tokens=500,
    temperature=0.5
  )
  
  return response.generations[0].text

# Sample query
story_text = 'Water into wine.'
question = "What is this story about? What is the moral?"

ai_response = query_cohere(story_text, question)

# Style the interface
def ai_response(story_text, question):
  return query_cohere(story_text, question)

iface = gr.Interface(ai_response,
              [gr.inputs.Text("text"), gr.inputs.Text("text")],
              gr.outputs.Text("text"),
              title="Bible Story Question Answering",
              description="Ask a question about a Bible story",
              theme="huggingface",
              layout="vertical",
              thumbnail="https://www.biblegateway.com/assets/images/logo.png",
              examples=[
                ["Water into wine", "What is this story about?"],
                ["Feeding the 5000", "What is the moral of this story?"],
                ["The Prodigal Son", "Where did it happen?"]
              ]
              )


iface.launch(inline=True)