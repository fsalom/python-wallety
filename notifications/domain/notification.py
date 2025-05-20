from typing import Any, Dict, Optional
from pydantic import Field, BaseModel


class Notification(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    data: Optional[Dict[str, Any]] = Field(default=None)
    created_by_user_id: int
