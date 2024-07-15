import streamlit as st
import pickle
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


#sidebar contents
with st.sidebar:
    st.title('LLM Chat App')
    st.markdown('''
       ## About
       This is a LLM Power Chatbot build using:
        [streamlit]
        [LangChain]
        [openAI]''')
    
    
    st.write('Made by Pankaj')

def main():
    st.title('Chat with PDF')

    load_dotenv()

    #upload the pdf file
    pdf = st.file_uploader("Upload your PDF",type='pdf')
    st.write(pdf.name)
    if pdf is not None:
        pdfreader = PdfReader(pdf)
        #st.write(pdfreader)
        text = ''
        for page in pdfreader.pages:
            text += page.extract_text()
        #st.write(text)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )
        chunks = text_splitter.split_text(text=text)

        # embeddings chunks
        
        store_name = pdf.name[:-4]

        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl","rb") as f:
                vectorstore = pickal.load(f)
        else:
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_texts(chunks,embeddings=embeddings)
            with open(f"{store_name}.pkl","wb") as f:
                pickal.dump(vectorstore,f)

        # Accept your Query/Question
        query = st.text_input("Ask Question about your PDF file:")
        st.write(query)

        if query:
            docs = vectorstore.similarity_search(query=query,k=3)

            llm = OpenAI(model_name='gpt-3.5-turbo')

            chain = load_qa_chain(llm=llm,chain_type="stuff")
            responce = chain.run(input_documents=docs,question=query)
            st.write(responce)


if __name__ == '__main__':
    main()