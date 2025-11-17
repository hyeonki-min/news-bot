from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NewsDTO(BaseModel):
    id: int
    title: str
    description: str
    link: str
    topic: str
    pub_date: datetime
    
    model_config = ConfigDict(from_attributes=True)