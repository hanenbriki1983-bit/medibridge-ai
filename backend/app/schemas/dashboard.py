from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_cases: int
    emergency_cases: int
    top_predicted_diseases: list[dict[str, int]]
    language_distribution: list[dict[str, int]]
