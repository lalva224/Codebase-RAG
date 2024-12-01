import streamlit as st
from store_codebases import store_codebase, get_codebases, remove_codebase,get_codebase
from codebase_rag import perform_rag
import requests


st.markdown('# Codebase RAG')
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.session_state['codebases'] = get_codebases()
st.session_state['selected_codebase'] = st.session_state['codebases'][0] if len(st.session_state['codebases'])>0 else None


prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

# response = f"Echo: {prompt}"
# # Display assistant response in chat message container

    with st.chat_message("assistant"):
        print(st.session_state['selected_codebase']['codebase_path'])
        response = perform_rag(prompt,st.session_state['selected_codebase']['codebase_path'])
        st.markdown(response)
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False

def show_form():
    st.session_state['show_form']=True
def hide_form():
    st.session_state['show_form']=False

with st.sidebar:
    button = st.button('Add codebase')
    if button:
        show_form()

    if st.session_state['show_form']==True:
        with st.form('codebase_form',clear_on_submit=True):
            codebase_name = st.text_input('Codebase name')
            codebase_path = st.text_input('Codebase path')
            

            submit_button = st.form_submit_button('Submit')
            if submit_button:
                store_codebase(codebase_name, codebase_path)
                st.success('Codebase information stored successfully!')
                # hide_form()
                
    selected_codebase_name = st.selectbox('Select a codebase', [codebase['codebase_name'] for codebase in st.session_state['codebases']])
    selected_codebase = get_codebase(selected_codebase_name)
    
    st.session_state['selected_codebase'] = selected_codebase
    remove_button = st.button('Remove codebase')
    if remove_button:
        remove_codebase(selected_codebase[0]['codebase_path'])
        st.session_state['selected_codebase'] = None
        st.success('Codebase removed successfully!')

