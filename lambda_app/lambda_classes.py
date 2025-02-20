from pydantic import BaseModel, Field
from typing import Literal

class LambdaEvent(BaseModel):
    SearchTerm: str = Field(min_length=2)
    FromDate: str = Field(default='', pattern=r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
    queue: Literal["guardian_content"]