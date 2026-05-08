from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str

    original_filename: str
    stored_filename: str
    status: str
    