# streamlit code 
import streamlit as st 
from database import init_database , get_all_reviews , create_code_review
from config import PROGRAMMING_LANGUAGES
from ai import perform_code_review_with_ollama
import time 
from utils import extract_code_quality_score

def sidebar_menu():
    st.sidebar.title("Review History")

    reviews = get_all_reviews()
    st.session_state['is_active'] = False

    for review in reviews[:5]:
        text = review['question'][:33]
        if st.sidebar.button(text , key=review['id']):
            display_json_review(review['answer'])


def display_json_review(review_data):
    st.markdown(review_data)


def main():
    st.set_page_config(page_title="AI Code Review Assistant",page_icon="🤖")

    # start db
    init_database()

    # add sidbar
    sidebar_menu()

    st.title("AI Code Review Assistant")

    language = st.selectbox("Programming Language" , options=PROGRAMMING_LANGUAGES)
    code_input = st.text_area("Code to Review" , height=200 )
    if st.button("Review Code"):
        with st.spinner("Analyzing Code..."):
            time.sleep(1)
            review_data = perform_code_review_with_ollama(code_input,language)
            display_json_review(review_data)

            score = extract_code_quality_score(review_data)

            # save data in db 
            create_code_review(
                question=code_input , 
                answer=review_data,
                language=language , 
                score=score
            )

            # trigger app rerun to update sidbar 
            # close_connection()
            # st.rerun()



if __name__ == "__main__":
    main()