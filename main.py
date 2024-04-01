import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Streamlit web app with sidebar
st.sidebar.header('AI-Enhanced Virtual Writing Assistant')

with st.sidebar:
    st.subheader('Writing Details')
    title = st.text_input('Enter the title of the writing:', key="title")
    essay_type = st.selectbox('Select the type of writing:',
                               ['Essay', 'Email', 'Meeting Minutes', 'Report', 'Formal Letter', 'Poem'], key="essay_type")
    writing_style = st.selectbox('Select the writing style:', ['Formal', 'Informal', 'Creative'], key="writing_style")
    word_count = st.slider('Select the number of words to generate:', min_value=200, max_value=1000, value=300, step=50, key="word_count")
    tone_sentiment = st.selectbox('Select the desired tone:', ['Informative', 'Persuasive', 'Neutral', 'Humorous', 'Enthusiastic'], key="tone")
    keywords = st.text_input('Enter keywords or a short description of the topic (optional):', key="keywords")
    generate_button = st.button("Generate")

# Main content area
st.image('ai.png', use_column_width=True)  # Assuming 'image.png' is your logo
st.subheader('Generated Writing')

if generate_button:
    if title:
        prompt = f"Write a {essay_type.lower()} titled '{title}' in a {writing_style.lower()} style with a {tone_sentiment.lower()} tone. "
        if keywords:
            prompt += f"Include the following keywords or phrases: {keywords}"
        prompt += " Adhere to the following criteria:"

        # Call the OpenAI API using openai.Completion.create
        response = openai.chat.Completions.create(
            engine="gpt-3.5-turbo-instruct",  # Adjust the engine as needed
            prompt=prompt,
            max_tokens=word_count,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Display generated text with word count and download option
        st.write(response.choices[0].text)
        st.write(f"Word count: {len(response.choices[0].text.split())}")
        st.download_button('Download Text', response.choices[0].text, 'generated_text.txt')
