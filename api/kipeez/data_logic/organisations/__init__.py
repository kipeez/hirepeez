from datetime import datetime
from pydantic import BaseModel
from typing import List
from typing import Optional
from pydantic import BaseModel


class Organisation(BaseModel):
    id: str
    name: str
    slug: str
    owner_id: str
    users_ids: List[str]


class OrganisationConfigAnalysis(BaseModel):
    sales_labels: List[str]
    upsales_comparison_step: str = "month"
    downsales_comparison_step: str = "month"
