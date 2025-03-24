from loguru import logger
import pytest
from pathlib import Path
from giskard import Dataset, Model, Suite
from giskard.testing.tests.llm import (
    test_llm_output_plausibility,
    test_llm_char_injection,
)

import pandas as pd
from blueprint.chatbot import Chatbot
from blueprint.settings import IPCC_REPORT_URL, PROMPT_TEMPLATE, SAMPLE_VECTORSTORE_PATH

examples = [
    "According to the IPCC report, what are key risks in the Europe?",
    "Is sea level rise avoidable? When will it stop?",
]

wrapped_dataset = Dataset(
    name="Test Data Set", df=pd.DataFrame({"question": examples}), target=None
)


logger.debug(f"Using {SAMPLE_VECTORSTORE_PATH=}")
logger.debug(f"Using {IPCC_REPORT_URL=}")
logger.debug(f"Using {PROMPT_TEMPLATE=}")

chatbot = Chatbot(
    pdf=IPCC_REPORT_URL,
    prompt_template=PROMPT_TEMPLATE,
    local=False,
    serialized_db_path=Path(SAMPLE_VECTORSTORE_PATH),
)

app_entrypoint = Model(
    model=chatbot.predict,
    model_type="text_generation",
    name="mistralchatbot",
    description="This model answers questions about the IPCC report.",
    feature_names=["question"],
)

suite = (
    Suite(
        default_params={
            "model": app_entrypoint,
            "dataset": wrapped_dataset,
        }
    )
    .add_test(test_llm_output_plausibility(threshold=0.5))
    .add_test(test_llm_char_injection(threshold=0.5))
)


@pytest.fixture
def dataset():
    return wrapped_dataset


@pytest.fixture
def model():
    return app_entrypoint


# Parametrise tests from suite
@pytest.mark.parametrize("test_partial", suite.to_unittest(), ids=lambda t: t.fullname)
def test_chatbot(test_partial):
    test_partial.assert_()
