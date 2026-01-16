import streamlit as st
import requests
API_URL = 'http://127.0.0.1:8000'


st.title("Welcome to the Dashboard of spam classifier")

email=st.text_input('Enter the email that you want to test')



if st.button('Dectect'):
    input ={
        'user_email': email
    }

    try:
        response = requests.post(f'{API_URL}/predict', json=input)
        if(response.status_code == 200):
            result = response.json()
            
            if result['predicted'] == 1 :
                result = 'spam'
            else :
                result = 'Not spam'
            st.success(f'the email is : { result}')
        else:
            st.error(f'API error: {response.status_code}-{response.text}')

    except requests.exceptions.ConnectionError:
        st.error('Could not connected to the fast api server. Make sure its running on the port 8000')