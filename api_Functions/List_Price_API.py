import base64
from playwright.sync_api import Page


class ListPriceAPI:
    def __init__(self, page: Page):
        self.page = page

    def getListPriceAPI(
        self,
        username: str,
        password: str,
        pricelist: str,
        product: str,
        start_date: str,
        end_date: str,
        min_qty: int,
        max_qty: int,
        min_term: int,
        max_term: int,
    ) -> float:

        # Basic Auth header value
        token = base64.b64encode(f"{username}:{password}".encode()).decode()

        # Use existing request context from the current browser context
        request_context = self.page.context.request

        # Build query string
        query = (
            f"{{$and:[{{Pricelist:{{$eq:'{pricelist}'}}}},"
            f"{{Product:{{$eq:'{product}'}}}},"
            f"{{ EndDate:{{$gte: '{end_date}'}}}},"
            f"{{ StartDate:{{$lte: '{start_date}'}}}},"
            f"{{ MinQty:{{$lte: '{min_qty}'}}}},"
            f"{{ MaxQty:{{$gte: '{max_qty}'}}}},"
            f"{{ MinTerm:{{$lte: '{min_term}'}}}},"
            f"{{ MaxTerm:{{$gte: '{max_term}'}}}}]}}"
        )

        url = (
            "https://netappinctest10.bigmachines.com/rest/v14/adminCustomPriceList"
            f"?q={query}"
        )

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
            raise AssertionError(f"No items returned in response: {data}")

        price = data["items"][0]["Price"]
        print("Price:", price)
        return price
