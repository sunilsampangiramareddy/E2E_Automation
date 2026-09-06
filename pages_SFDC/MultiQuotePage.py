from decimal import Decimal


class MultiQuotePage:
    def __init__(self, page):
        self.page = page

    def isWithinTolerance(self, expected_value, actual_value, tolerance=Decimal("0.01")) -> bool:
        """Return True when the difference is within tolerance on either side."""
        try:
            expected_decimal = Decimal(str(expected_value))
            actual_decimal = Decimal(str(actual_value))
            return abs(expected_decimal - actual_decimal) <= tolerance
        except Exception:
            return False

    def calculateDealScorePercentages(
        self,
        total_list_price,
        deal_score_to_2,
        deal_score_to_3,
        deal_score_to_4,
        deal_score_to_5,
    ) -> dict:
        """Return the calculated DDS deal score percentages using the Decimal values already passed in."""
        if total_list_price == 0:
            raise ValueError(
                "Total List Price cannot be zero for Deal Score percentage calculation."
            )

        return {
            "Deal_Score_To_2_Percent": round(
                (1 - deal_score_to_2 / total_list_price) * 100, 2
            ),
            "Deal_Score_To_3_Percent": round(
                (1 - deal_score_to_3 / total_list_price) * 100, 2
            ),
            "Deal_Score_To_4_Percent": round(
                (1 - deal_score_to_4 / total_list_price) * 100, 2
            ),
            "Deal_Score_To_5_Percent": round(
                (1 - deal_score_to_5 / total_list_price) * 100, 2
            ),
        }
