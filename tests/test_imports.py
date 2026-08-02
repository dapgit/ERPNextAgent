import sys


def test_app_and_assistant_import_without_module_errors():
    sys.modules.pop("app", None)
    sys.modules.pop("agent.assistant", None)

    import app
    from agent.assistant import create_agent

    assert callable(create_agent)
    assert hasattr(app, "main")
