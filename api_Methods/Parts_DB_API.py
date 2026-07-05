import base64
from playwright.sync_api import Page


class PartsDBAPI:
    def __init__(self, page: Page):
        self.page = page

    def getPartsDBAPI(
        self,
        username: str,
        password: str,
        part_number: str,
    ) -> str:

        # Basic Auth header value
        token = base64.b64encode(f"{username}:{password}".encode()).decode()

        # Use existing request context from the current browser context
        request_context = self.page.context.request

        # Build query string
        query = f"{{partNumber:'{part_number}'}}"

        url = "https://netappinctest10.bigmachines.com/rest/v16/parts" f"?q={query}"

        # Make GET request using Playwright's request context
        response = request_context.get(
            url,
            headers={
                "Authorization": f"Basic {token}",
                "Accept": "*/*",
            },
        )

        print("Status:", response.status)
        print("Text:", response.text())
        assert response.status == 200, f"Unexpected status code: {response.status}"

        data = response.json()

        # Defensive check if items is empty
        if not data.get("items"):
            raise AssertionError(
                f"No items returned for partNumber '{part_number}'. Response: {data}"
            )

        # Extract _part_custom_field25
        custom_field_25 = data["items"][0].get("_part_custom_field25")
        print("Part details:", custom_field_25)
        return custom_field_25
