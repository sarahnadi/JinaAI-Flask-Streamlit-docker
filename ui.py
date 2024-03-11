import streamlit as st
import requests

# Define the Flask backend URL
BACKEND_URL = 'http://flask-backend:5000/search'

# Streamlit UI
st.title('GN Vector Search Engine')

# Text input for user query
query_text = st.text_input('Enter your query:', '')

# Search button
if st.button('Search'):
    with st.spinner('Searching...'):
    # ... rest of your logic for handling response
    # Make a POST request to the Flask backend
        response = requests.post(BACKEND_URL, json={'query': query_text})

        if response.status_code == 200:
            # Display the tags returned by the backend
            tags = response.json()
            st.write('Tags for the most similar document:')
            st.write(tags)
        else:
            st.write('Error occurred during search. Please try again later.')
