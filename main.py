import streamlit as st
import streamlit_authenticator as stauth
from database import sign_up, fetch_users
import streamlit as st
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, LangchainEmbedding, GPTListIndex, GPTSimpleVectorIndex, PromptHelper
from llama_index import LLMPredictor, ServiceContext
import os
from MedEzy import Medezy_app


st.set_page_config(page_title="MedEzy")
st.title('MedEzy :robot_face:')



try:
    
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'WELCOME {username}')
                Authenticator.logout('Log Out', 'sidebar')
                Medezy_app()

                

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    st.success('Refresh Page')