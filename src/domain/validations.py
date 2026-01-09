def validate_task_state(state: str) -> str:
    VALID_STATES: list[str] = ["on validation", "queue", "benchmark", "archive"]

    if state not in VALID_STATES:
        raise ValueError(f"Invalid state: {state!r}")
    return state
