from pathlib import Path

import pandas as pd
import pytest
from giskard import Dataset, Model
from giskard.testing.tests.llm import (
    test_llm_char_injection as llm_char_injection,
    test_llm_correctness as llm_correctness,
    test_llm_ground_truth_similarity as llm_ground_truth_similarity,
    test_llm_output_plausibility as llm_output_plausibility,
    test_llm_single_output_against_requirement as llm_single_output_against_requirement,
)
from loguru import logger

from blueprint.chatbot import Chatbot
from blueprint.settings import (
    IPCC_REPORT_URL,
    PROMPT_TEMPLATE,
    SAMPLE_QA_PATH,
    SAMPLE_VECTORSTORE_PATH,
)

"""
examples = [
    "According to the IPCC report, what are key risks in the Europe?",
    "Is sea level rise avoidable? When will it stop?",
    "What are the main drivers of global warming?",
    "What is the importance of equity in climate action?",
    "What are the benefits of climate action for human health?",
    "How can climate governance support effective climate action?",
    "What is the role of technology in climate mitigation and adaptation?",
    "How can climate education and awareness contribute to climate action?",
]
"""

logger.debug(f"Using {SAMPLE_VECTORSTORE_PATH=}")
logger.debug(f"Using {IPCC_REPORT_URL=}")
logger.debug(f"Using {PROMPT_TEMPLATE=}")


@pytest.fixture
def dataset():
    df = pd.read_csv(SAMPLE_QA_PATH)
    wrapped_dataset = Dataset(name="Test Data Set", df=df, target="reference_answer")
    return wrapped_dataset


@pytest.fixture
def app_entrypoint():
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
    return app_entrypoint


test_cases = [
    ("llm_output_plausibility", llm_output_plausibility(threshold=0.5), True, {}, {}),
    ("llm_char_injection", llm_char_injection(threshold=0.5), True, {}, {}),
    ("llm_ground_truth_similarity", llm_ground_truth_similarity(threshold=0.3), True, {}, {}),
    ("llm_correctness", llm_correctness(threshold=0.5), True, {}, {}),
    (
        "llm_single_output_against_requirement",
        llm_single_output_against_requirement(
            threshold=0.5,
            requirement="The actual answer should be in the same language as the input question.",
        ),
        False,
        {},
        {},
    ),
]


@pytest.mark.parametrize("test_name, test_obj, needs_dataset, extra_kwargs, extra_args", test_cases)
def test_chatbot_llm_tests(app_entrypoint, dataset, test_name, test_obj, needs_dataset, extra_kwargs, extra_args):
    args = {"model": app_entrypoint}
    if needs_dataset:
        args["dataset"] = dataset
    args.update(extra_kwargs)
    args.update(extra_args)
    result = test_obj(**args).execute()
    assert result.passed, f"{test_name} failed: {getattr(result, 'message', '')}"
