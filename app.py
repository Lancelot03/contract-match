import streamlit as st
from streamlit_option_menu import option_menu
from openai import AzureOpenAI
import docx2txt
import PyPDF2
import os
from pdfminer.high_level import extract_text
class OpenaiAPI():
  def __init__(self) -> None:

      self.client = AzureOpenAI(
          api_key = os.environ["API"],
          api_version="2023-07-01-preview",
          azure_endpoint=os.environ["URL"],
      )

  def get_response(self,prompt,) -> str:
      try:

          completion = self.client.chat.completions.create(
              model="GPT-4o",  # e.g. gpt-35-instant
              messages=prompt,
              temperature=0,)
          return completion.choices[0].message.content

      except Exception as e:
          print("An error occurred while generate prompt from openai api: %s", e)

  def docx_to_text(self,docx_path):
      text = docx2txt.process(docx_path)
      return text

  def pdf_to_text_pypdf2(self,pdf_file):
      text = extract_text(pdf_file)
      return text

st.markdown("""
      <style>
      h1#contract-ai {
      text-align: center;
      }
      header.st-emotion-cache-12fmjuu.ezrtsby2{
        background-color: rgb(234 237 240);
        color: rgb(0, 0, 0);
      }
      .st-emotion-cache-1mi2ry5{
        background:url('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftheindustryspread.com%2Fwp-content%2Fuploads%2F2019%2F05%2FBroadridge-1.png') no-repeat;
        background-size: 250px 50px;
        background-position: center;
      }
      </style>
  """, unsafe_allow_html=True)
with st.sidebar:
    selected = option_menu("CONTRACT AI", ['Home','Tags','Clauses',
                                           'Summarizer','Headings','Extract Date',
                                           'Pdf to Json','Key Values','Incorrent Sentences',
                                           'Incompleted Sentences','Agressive Content',
                                           'Compare Contract','Find Contract',"Contract Generator"
                                           ],
                           icons=['arrow-right-circle-fill','arrow-right-circle-fill','arrow-right-circle-fill',
                                                    'arrow-right-circle-fill','arrow-right-circle-fill','arrow-right-circle-fill',
                                                    'arrow-right-circle-fill','arrow-right-circle-fill','arrow-right-circle-fill',
                                                    'arrow-right-circle-fill','arrow-right-circle-fill','arrow-right-circle-fill',
                                                    'arrow-right-circle-fill','arrow-right-circle-fill'],
                           menu_icon="house-gear-fill",
                           default_index=0)
    uploaded_file=st.file_uploader("Upload a Docs")
openai = OpenaiAPI()
if selected == 'Home':
  st.title('Contract AI')
  # Dictionary containing the topics and their descriptions
  topics = {
    "None": "Default option with no specific action.",
    "Tags": "Extract tags or keywords from the document.",
    "Clauses": "Identify and extract specific clauses from contracts.",
    "Summarizer": "Generate a concise summary of the document.",
    "Headings": "Extract and display headings from the document.",
    "Extract Date": "Find and extract dates from the document.",
    "Pdf to Json": "Convert PDF documents to JSON format.",
    "Key Values": "Extract key-value pairs from the document.",
    "Incorrect Sentences": "Identify and highlight incorrect sentences.",
    "Incomplete Sentences": "Detect and list incomplete sentences.",
    "Aggressive Content": "Identify and flag aggressive or inappropriate content.",
    "Compare Contract": "Compare two contracts to find differences.",
    "Find Contract": "Search and locate specific contracts.",
    "Contract Generator": "Generate a contract based on provided inputs."
  }

  # Custom CSS for the gray background
  st.markdown("""
      <style>
      h1#contract-ai {
      text-align: center;
      }
      .topic-box {
          background-color: #f0f0f0;
          padding: 10px;
          border-radius: 5px;
          margin-bottom: 10px;
      }
      .topic-box:hover{
        background-color: #000080;
        box-shadow: 6px 1px 12px gray;
        color:#fff;
      }
      .topic-title {
          font-weight: bold;
      }
      .st-emotion-cache-ocqkz7 {
        gap: 1.5rem;
        }
      </style>
  """, unsafe_allow_html=True)

  # Split topics into groups of three for a 3-column layout
  topic_items = list(topics.items())
  for i in range(0, len(topic_items), 3):
      cols = st.columns(3)
      for col, (title, description) in zip(cols, topic_items[i:i+3]):
          col.markdown(f"""
          <div class="topic-box">
              <div class="topic-title">{title}</div>
              <div>{description}</div>
          </div>
          """, unsafe_allow_html=True)
elif selected == 'Contract Generator':
  st.markdown(
      """
  <style>
      h1,#contract-generator,#extract-date,#pdf-to-json,#key-values {
        text-align: center;
      }
  </style>
  """,
      unsafe_allow_html=True,)
  st.title(selected)
  contract_info=st.text_input("Enter Contract info")
  conversation = [{"role": "system", "content": """You are a helpful assistant. Your task is creating a complete contract with important terms and condiations based on the contract information and type.
                  the contract type given by user.
                  generate a contract :
                  """},
                  {"role": "user", "content": f"```content: {contract_info}```"}]
  get_response = openai.get_response(conversation)
  st.write(get_response)

elif selected == 'Extract Date':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful assistant.
                  Your task is Identify Dates and Durations Mentioned in the contract and extract that date and duration in key-value pair.
                  format:
                  date:
                  -extracted date
                  -
                  Durations:
                  -extracted Durations
                  -
                  - """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
      st.write('Upload File')
elif selected == 'Pdf to Json':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful assistant.
                  Your task is Get the text and analyse and split it into Topics and Content in json format.Give Proper Name to Topic dont give any Numbers and Dont Give any empty Contents.The Output Format Should Be very good."""},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')
elif selected == 'Key Values':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful Keywords Extracter..
                  analyze the given contract and Extract Keywords for following contract in triple backticks. tags should be bullet points.contract :
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Tags':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful Tags Extracter.
                  analyze the given contract to extract tags for following contract in triple backticks.
                  tags should be bullet points.contract :
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Clauses':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful Cluases and SubCluases Extracter From Given Content
                  Extract clauses and sub-clauses from the provided contract PDF
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Headings':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful document assistant.
                  Extract Headings from given paragraph do not generate jsu extract the headings from paragraph.
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Incorrent Sentences':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful Error sentence finder.
                  list out the grammatical error sentence in the given text:
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Incompleted Sentences':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                      You are a helpful incomplete sentences finder.
                      list out the incomplete sentences in the following text:
                      """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Agressive Content':
  st.title(selected)
  if uploaded_file is not None:
    print('File Name : ',uploaded_file.name)
    ftype=uploaded_file.name.split('.')
    if ftype[-1]=='pdf':
      docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
    elif ftype[-1]=='docx':
      docs_data = openai.docx_to_text(uploaded_file)
    conversation = [{"role": "system", "content": """
                  You are a helpful Keywords Extracter..
                  analyze the given contract and Extract Keywords for following contract in triple backticks. tags should be bullet points.contract :
                  """},
                  {"role": "user", "content": f"```contract: {docs_data}```"}]
    get_response = openai.get_response(conversation)
    st.write(get_response)
  else:
    st.write('Upload File')

elif selected == 'Compare Contract':
    st.title(selected)
    uploaded_file2 = st.file_uploader("Upload a Second Contract for Comparison")
    if uploaded_file is not None and uploaded_file2 is not None:
        print('File Name : ', uploaded_file.name)
        print('File Name : ', uploaded_file2.name)
        ftype1 = uploaded_file.name.split('.')
        ftype2 = uploaded_file2.name.split('.')
        if ftype1[-1] == 'pdf' and ftype2[-1] == 'pdf':
            docs_data1 = openai.pdf_to_text_pypdf2(uploaded_file)
            docs_data2 = openai.pdf_to_text_pypdf2(uploaded_file2)
        elif ftype1[-1] == 'docx' and ftype2[-1] == 'docx':
            docs_data1 = openai.docx_to_text(uploaded_file)
            docs_data2 = openai.docx_to_text(uploaded_file2)
        conversation = [{"role": "system", "content": """
                        You are a helpful contract comparison assistant.
                        Compare the following two contracts and highlight any differences or similarities.
                        """},
                        {"role": "user", "content": f"```contract 1: {docs_data1}``` ```contract 2: {docs_data2}```"}]
        get_response = openai.get_response(conversation)
        st.write(get_response)
    else:
        st.write('Upload Both Files')

elif selected == 'Find Contract':
    st.title(selected)
    contract_search = st.text_input("Enter Contract Information to Search")
    if contract_search:
        conversation = [{"role": "system", "content": """
                        You are a helpful contract finder.
                        Search and locate the specific contract based on the following information:
                        """},
                        {"role": "user", "content": f"```search: {contract_search}```"}]
        get_response = openai.get_response(conversation)
        st.write(get_response)
    else:
        st.write('Enter Information to Search')

elif selected == 'Summarizer':
    st.title(selected)
    if uploaded_file is not None:
        print('File Name : ', uploaded_file.name)
        ftype = uploaded_file.name.split('.')
        if ftype[-1] == 'pdf':
            docs_data = openai.pdf_to_text_pypdf2(uploaded_file)
        elif ftype[-1] == 'docx':
            docs_data = openai.docx_to_text(uploaded_file)
        conversation = [{"role": "system", "content": """
                        You are a helpful summarizer.
                        Write a concise summary of the following contract:
                        """},
                        {"role": "user", "content": f"```contract: {docs_data}```"}]
        get_response = openai.get_response(conversation)
        st.write(get_response)
    else:
        st.write('Upload File')
