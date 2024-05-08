# dependencies
import os
import yaml
import logging
import tempfile
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import load_prompt
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcq-generator")

# function to initialize web app for the first time
def initialize_app():
    """Performs processing that should happen upon loading of the web app and
    sets all session state variables to their desired initial state.
    """
    # set status flags to their desired initial state
    st.session_state.p01_pdf_pages = None
    st.session_state.p01_pdf_text = None
    st.session_state.p01_llm_response = None
    st.session_state.p01_generate_mcqs_disabled = True

    # set the flag that indiciates initialization is done
    # this flag is crucial and should be done as the very last step in this function as
    # the web app invokes this function only when this variable is not set
    st.session_state.p01_init_complete = True

# function to load pdf content
def load_pdf_content():
    if st.session_state.p01_source_data_file is not None:
        # get file name and extension of the uploaded file 
        file_name, file_extn = os.path.splitext(st.session_state.p01_source_data_file.name)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file_obj:
            # create a temporary file and write the contents of uploaded file to it
            temp_file_name = temp_file_obj.name
            temp_file_obj.write(st.session_state.p01_source_data_file.getvalue())
            temp_file_obj.close()

            # read the uploaded file content from the temporary file
            loader = PyPDFLoader(temp_file_name)
            st.session_state.p01_pdf_pages = loader.load()
            st.session_state.p01_pdf_text = \
                ''.join(page.page_content for page in st.session_state.p01_pdf_pages[:])
    else:
        st.session_state.p01_pdf_pages = None
        st.session_state.p01_pdf_text = None

# function to generate MCQs
def generate_mcqs():
    """Reads the uploaded file and invokes the LLM to generate MCQs
    """
    # load contents of uploaded file to session state variable
    load_pdf_content()

    # load prompt template from json file
    st.session_state.p01_prompt_template = load_prompt('./templates/prompt_5.json')

    # load api keys or access tokens from env file
    load_dotenv(find_dotenv())

    # initialize LLM and LLM Chain
    # llm = \
    #     HuggingFaceEndpoint(
    #         repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    #         temperature=0.1, 
    #         )
    
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", 
        temperature=0.1, 
        )

    # llm_chain = LLMChain(prompt=st.session_state.p01_prompt_template, llm=llm)
    llm_chain = st.session_state.p01_prompt_template | llm

    # generate response from LLM
    st.session_state.p01_llm_response = llm_chain.invoke(
        {
            'mcq_source': st.session_state.p01_pdf_text, 
            'mcq_difficulty_level': st.session_state.p01_difficulty_level, 
            'mcq_count': st.session_state.p01_questions_count, 
            }
    )

# function for rendering the main web application
def run_web_app():
    """Renders the web application, captures user actions and
    invokes appropriate event specific callbacks.
    """
    # page or window title - this shows up as browser window title
    st.set_page_config(page_title="MCQ Generator")

    # call initialization function (only for the first time)
    if "p01_init_complete" not in st.session_state:
        initialize_app()

    # setup sidebar
    # siderbar title
    st.sidebar.markdown(
        "<h4 style='color: orange;'>MCQ Generator</h4>",
        unsafe_allow_html=True,
    )

    # widget to upload source data file
    source_data_file = \
        st.sidebar.file_uploader(
            label="Source Data File", 
            type=['pdf'], 
            key='p01_source_data_file', 
            )
    
    # widget to select difficulty level
    difficulty_level_options = ['Easy', 'Medium', 'Hard']
    difficulty_level = st.sidebar.selectbox(
        label="Difficulty Level",
        placeholder="Select a difficulty level",
        options=difficulty_level_options,
        key="p01_difficulty_level",
    )

    # widget to specify number of questions
    questions_count = st.sidebar.number_input(
        label="Number of MCQs",
        placeholder="Enter number of questions", 
        min_value=1, 
        max_value=20, 
        key="p01_questions_count",
    )

    # enable MCQ generation button if all inputs are filled in
    inputs_filled = (
        st.session_state.p01_source_data_file is not None and 
        st.session_state.p01_difficulty_level is not None and 
        st.session_state.p01_questions_count is not None
        )
    if inputs_filled:
        st.session_state.p01_generate_mcqs_disabled = False
    else:
        st.session_state.p01_generate_mcqs_disabled = True

    # button to start MCQ generation
    st.sidebar.button(
        label="Generate MCQs",
        on_click=generate_mcqs, 
        disabled=st.session_state.p01_generate_mcqs_disabled, 
        key="p01_generate_mcqs",
    )

    # render uploaded file content on screen
    if st.session_state.p01_pdf_text is not None:
        # st.write(st.session_state.p01_pdf_text)
        # st.write(st.session_state.p01_prompt_template)
        # st.write(st.session_state.p01_llm_response)
        # st.write(st.session_state.p01_llm_response.content[:100])
        # st.write(st.session_state.p01_llm_response.content)
        # print(type(st.session_state.p01_llm_response.content))

        temp_file_obj = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml')
        temp_file_name = temp_file_obj.name

        with open(temp_file_name, 'w') as temp_file_obj:
            temp_file_obj.write(st.session_state.p01_llm_response.content)

        # open yaml file and load all the contents into a dictionary
        with open(temp_file_name, 'r') as file_handle:
            mcq_dict = yaml.safe_load(file_handle)

        # print(mcq_dict)

        for mcq_id, mcq_details in mcq_dict.items():
            st.write(f"{mcq_id}. {mcq_details['question']}")
            st.write(f"A: {mcq_details['choice_A']}")
            st.write(f"B: {mcq_details['choice_B']}")
            st.write(f"C: {mcq_details['choice_C']}")
            st.write(f"D: {mcq_details['choice_D']}")
            st.success(f"Correct Choice: {mcq_details['correct_choice']}", icon=None)
            st.write("")

        st.write("LLM & Token Usage Details")
        st.write(st.session_state.p01_llm_response.response_metadata)

# call the function to render the main web application
if __name__ == "__main__":
    run_web_app()