from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_task_table_omits_completion_status():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run()
    app.button(key="FormSubmitter:add_pet_form-Add pet").click().run()
    app.button(key="FormSubmitter:add_task_form-Add task").click().run()

    assert not app.exception
    table = app.table[0].value
    assert list(table.columns) == [
        "pet",
        "task",
        "time",
        "duration (min)",
        "priority",
        "frequency",
    ]
    assert table.iloc[0]["task"] == "Morning walk"
