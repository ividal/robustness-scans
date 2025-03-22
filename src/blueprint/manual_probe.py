from loguru import logger
import giskard
import pandas as pd
from blueprint.chatbot import Chatbot
from blueprint.settings import OUTPUT_FOLDER, IPCC_REPORT_URL, PROMPT_TEMPLATE

if __name__ == "__main__":
    bot = Chatbot(
        pdf=IPCC_REPORT_URL,
        prompt_template=PROMPT_TEMPLATE,
        local=False,
        output_folder=OUTPUT_FOLDER,
    )
    giskard_model = giskard.Model(
        model=bot.predict,
        model_type="text_generation",
        name="Climate Change Question Answering",
        description="This model answers any question about climate change based on IPCC reports",
        feature_names=["question"],
    )

    # Optional: let’s test that the wrapped model works
    examples = [
        "According to the IPCC report, what are key risks in the Europe?",
        # "Is sea level rise avoidable? When will it stop?",
    ]
    giskard_dataset = giskard.Dataset(pd.DataFrame({"question": examples}), target=None)

    answers = giskard_model.predict(giskard_dataset).prediction
    logger.info([f"\n{q}: {a}" for q, a in zip(examples, answers)])

    full_report = giskard.scan(giskard_model, giskard_dataset, only="hallucination")

    # full_report = giskard.scan(giskard_model, giskard_dataset)

    html_path = OUTPUT_FOLDER / "scan_report.html"
    full_report.to_html(filename=html_path, embed=True)
    logger.info(f"Exported to {html_path}")

    json_path = OUTPUT_FOLDER / "scan_report.json"
    full_report.to_json(filename=html_path)
    logger.info(f"Exported to {html_path}")

    md_path = OUTPUT_FOLDER / "scan_report.md"
    full_report.to_markdown(filename=md_path, template="huggingface")
    logger.info(f"Exported to {md_path}")

    """## Generate comprehensive test suites automatically for your model
    The objects produced by the scan can be used as fixtures to generate a test suite
    that integrates all detected vulnerabilities. Test suites allow you to evaluate
    and validate your model's performance, ensuring that it behaves as expected on a
    set of predefined test cases, and to identify any regressions or issues that might
    arise during development or updates.
    """

    # test_suite = full_report.generate_test_suite(name="Test suite generated by scan")
    # test_suite.run()
