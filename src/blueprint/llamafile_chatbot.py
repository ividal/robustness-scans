import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Llamafile
from langchain_community.embeddings import LlamafileEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
from blueprint.settings import IPCC_REPORT_URL, OUTPUT_FOLDER

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logger.add(OUTPUT_FOLDER / "chatbot.log", rotation="10 MB")


def create_llamafile_chain(
    llamafile_url="http://localhost:8080/v1",
    document_path=IPCC_REPORT_URL,
    serialised_embeddings=None,
) -> RetrievalQA:
    """Create a QA chain using a local Llamafile API endpoint."""
    logger.info(f"Creating QA chain with Llamafile at {llamafile_url}")

    if serialised_embeddings:
        db = FAISS.load_local(OUTPUT_FOLDER / "vectorstore", LlamafileEmbeddings())
    else:
        # Create text splitter for document chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100, add_start_index=True
        )

        # Load and split document
        logger.info(f"Loading document from {document_path}")
        docs = PyPDFLoader(document_path).load_and_split(text_splitter)

        # Initialize LlamaCpp for embeddings
        embeddings = LlamafileEmbeddings()
        # embeddings = OpenAIEmbeddings()

        # Create vector store
        logger.info("Creating vector store from document chunks")
        db = FAISS.from_documents(docs[:2], embeddings)
        db.save_local(OUTPUT_FOLDER / "vectorstore")

    # Create the LLM
    llm = Llamafile()

    # Create prompt template
    prompt_template = """Answer the question based on the context provided.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["question", "context"]
    )

    # Create the chain
    qa_chain = RetrievalQA.from_llm(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        prompt=prompt,
    )

    logger.info("Llamafile QA chain created successfully")
    return qa_chain


if __name__ == "__main__":
    # Example usage
    chain = create_llamafile_chain(
        llamafile_url="http://localhost:8080/v1", document_path=IPCC_REPORT_URL
    )

    response = chain.invoke({"query": "What is the main topic of this document?"})
    logger.info(f"Response: {response}")
