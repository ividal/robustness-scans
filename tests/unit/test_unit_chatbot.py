import pytest
from unittest.mock import patch, MagicMock
from blueprint.chatbot import Chatbot
import pandas as pd

# Mock paths and constants
fake_pdf_path = "fake_report.pdf"
fake_prompt_template = "Answer the question: {question}. Context: {context}"
fake_output_folder = "/fake/output"

# Sample questions DataFrame
sample_df = pd.DataFrame({"question": ["Is sea level rise avoidable?"]})

# Mock environment settings
@pytest.fixture
def mock_settings(monkeypatch):
    monkeypatch.setattr("src.blueprint.chatbot.IPCC_REPORT_URL", fake_pdf_path)
    monkeypatch.setattr("src.blueprint.chatbot.PROMPT_TEMPLATE", fake_prompt_template)
    monkeypatch.setattr("src.blueprint.chatbot.OUTPUT_FOLDER", fake_output_folder)

@pytest.fixture
def chatbot(mock_settings):
    with patch('src.blueprint.chatbot.FAISS', autospec=True) as mock_FAISS:
        mock_faiss = MagicMock()
        mock_faiss.as_retriever.return_value = MagicMock()
        mock_FAISS.load_local.return_value = mock_faiss
        mock_FAISS.from_documents.return_value = mock_faiss

        with patch('src.blueprint.chatbot.PyPDFLoader') as MockPyPDFLoader:
            mock_loader_instance = MockPyPDFLoader.return_value
            mock_loader_instance.load_and_split.return_value = ["dummy_docs"]

            return Chatbot(pdf=fake_pdf_path, prompt_template=fake_prompt_template, local=False, serialized_db_path=None)

def test_initialize_context_storage(chatbot):
    assert chatbot.context_db is not None

def test_create_chain(chatbot):
    assert chatbot.chain is not None
    assert callable(chatbot.chain.invoke)

def test_predict(chatbot):
    mock_response = [{"answer": "No, it is inevitable due to current trends."}]
    
    with patch.object(chatbot.chain, 'invoke', return_value=mock_response) as mock_invoke:
        response = chatbot.predict(sample_df)
        mock_invoke.assert_called()
        assert response == [mock_response]

# The following is a simple illustration
def test_hallucination_detection(chatbot):
    with patch.object(chatbot.chain, 'invoke') as mock_invoke:
        mock_invoke.side_effect = [{"answer": "Unicorn sightings indicate climate change."}]
        response = chatbot.predict(sample_df)
        
        assert "Unicorn" not in response[0]["answer"], "Detected hallucination in response."