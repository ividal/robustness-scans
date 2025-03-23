from loguru import logger
import pytest
from pathlib import Path
from giskard import Dataset, Model
from giskard.testing.tests.llm import (
    test_llm_output_plausibility,
    test_llm_char_injection,
)

from giskard import Dataset, Model
import pandas as pd
from blueprint.chatbot import Chatbot
from blueprint.settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, SAMPLE_VECTORSTORE_PATH


@pytest.fixture
def dataset():
    examples = [
        "According to the IPCC report, what are key risks in the Europe?",
        "Is sea level rise avoidable? When will it stop?",
    ]

    wrapped_dataset = Dataset(pd.DataFrame({"question": examples}), target=None)
    return wrapped_dataset


@pytest.fixture
def model():
    logger.debug(f"Using {SAMPLE_VECTORSTORE_PATH=}")
    logger.debug(f"Using {IPCC_REPORT_URL=}")
    logger.debug(f"Using {PROMPT_TEMPLATE=}")

    chatbot = Chatbot(
        pdf=IPCC_REPORT_URL,
        prompt_template=PROMPT_TEMPLATE,
        local=False,
        serialized_db_path=Path(SAMPLE_VECTORSTORE_PATH),
    )

    wrapped_model = Model(
        model=chatbot.predict,
        model_type="text_generation",
        name="mistralchat",
        description="This model answers questions about the IPCC report.",
        feature_names=["question"],
    )

    return wrapped_model


def test_chain(dataset, model):
    assert (
        "MISTRAL_API_KEY" in os.environ
    ), "Please set the MISTRAL_API_KEY environment variable"
    assert (
        "OPENAI_API_KEY" in os.environ
    ), "Please set the OPENAI_API_KEY environment variable"
    test_llm_output_plausibility(model=model, dataset=dataset).assert_()
    test_llm_char_injection(model=model, dataset=dataset).assert_()
