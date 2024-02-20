# Use gradio to create a simple UI to query the stories ie a chatbot kids can easily interact with and learn from. We will call it BibleBot
# Import libraries
import gradio as gr
import cohere

co = cohere.Client('q81O6CJT17c7qfSQc7U693xvFwAVf9rDhsjoHv2b')

# Define a function to query text with Cohere
def query_cohere(text, question):
  response = co.generate(
    prompt=f'Text: {text}\n\nQuestion: {question}', 
    max_tokens=500,
    temperature=0.5
  )
  
  return response.generations[0].text

# Create a Gradio interface
def biblebot(story, question):
  return query_cohere(story, question)

# Now we can use the BibleBot to query the stories and get responses
# to run it on the terminal, use the command below
# python3 biblebot.py

# We can style our app a bit more by adding a title and description
iface = gr.Interface(
    fn=biblebot, 
    inputs=["text", "text"], 
    outputs="text",
    title="BibleBot",
    description="A chatbot kids can easily interact with and learn from."
    )

iface.launch()

# Now we can run the app and interact with it on the browser
# python3 app.py
