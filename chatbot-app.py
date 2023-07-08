import streamlit as st
import requests

headers = {
    'x-api-key': 'sec_HiWgPDHRsm58hPgLuRzU01GVMYeT0FUs',
    "Content-Type": "application/json",
}

pdf_urls = [
    "https://dyrassa.com/wp-content/uploads/2022/08/Reactions-responsables-de-la-Liberation-de-lenergie-emmagasinee-dans-la-matiere-organique-PDF-5.pdf"
]

add_url_endpoint = 'https://api.chatpdf.com/v1/sources/add-url'
chat_endpoint = 'https://api.chatpdf.com/v1/chats/message'

def process_question(pdf_url):
    # Step 1: Add PDF via URL
    add_url_payload = {"url": pdf_url}

    add_url_response = requests.post(add_url_endpoint, headers=headers, json=add_url_payload)
    if add_url_response.status_code == 200:
        source_id = add_url_response.json().get('sourceId')
    else:
        st.error('Failed to add PDF via URL: {}'.format(pdf_url))
        st.error('Status: {}'.format(add_url_response.status_code))
        st.error('Error: {}'.format(add_url_response.text))
        return

    # Step 2: Chat with the PDF
    st.subheader("Ask a Question for PDF: {}".format(pdf_url))
    question = st.text_input("Enter your question", "")

    if st.button("Submit"):
        if question.lower() == 'exit':
            return

        data = {
            'referenceSources': True,
            'sourceId': source_id,
            'messages': [
                {
                    'role': "user",
                    'content': question,
                }
            ]
        }

        response = requests.post(chat_endpoint, headers=headers, json=data)

        if response.status_code == 200:
            answer = response.json()['content']
            st.success('Response: {}'.format(answer))
        else:
            st.error('Failed to send the chat message for PDF: {}'.format(pdf_url))
            st.error('Status: {}'.format(response.status_code))
            st.error('Error: {}'.format(response.text))

def main():
    st.title("Chatbot SVT :book:")

    for pdf_url in pdf_urls:
        process_question(pdf_url)

if __name__ == '__main__':
    main()
