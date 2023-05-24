from pydantic import BaseModel, Field

class Item(BaseModel):
    message: str = Field(..., title='Message', max_length=4096)