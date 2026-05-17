from playwright.sync_api import Locator


def wait_for_element(locator: Locator, state: str = "visible", timeout: int = 60000):
    """
    Waits for an element to be in a specific state.

    :param locator: The Playwright Locator object.
    :param state: The state to wait for (default is 'visible').
    :param timeout: The time to wait for the element (default is 60 seconds).
    :raises Exception: If the element does not reach the desired state within the timeout.
    """
    try:
        locator.wait_for(state=state, timeout=timeout)
    except Exception as e:
        raise Exception(
            f"Failed to wait for element to be '{state}' within {timeout}ms: {e}"
        )
