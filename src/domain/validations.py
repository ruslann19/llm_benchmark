from domain import ON_VALIDATION_STATE, QUEUE_STATE, BENCHMARK_STATE, ARCHIVE_STATE


def validate_task_state(state: str) -> str:
    VALID_STATES: list[str] = [
        ON_VALIDATION_STATE,
        QUEUE_STATE,
        BENCHMARK_STATE,
        ARCHIVE_STATE,
    ]

    if state not in VALID_STATES:
        raise ValueError(f"Invalid state: {state!r}")
    return state
