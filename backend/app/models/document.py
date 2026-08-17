from pydantic import BaseModel, ConfigDict, field_serializer
from typing import Optional
from bson import ObjectId
from datetime import datetime


class Document(BaseModel):
    equipment_id: ObjectId
    tenant_id: str
    file_name: str
    content_type: str
    size: int
    storage_key: str
    uploaded_by: str
    description: Optional[str] = None
    embedding_status: str = "pending"  # pending, processing, completed, failed
    embedding_error: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer("equipment_id")
    def serialize_objectid(self, value: ObjectId) -> str:
        return str(value)

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        if value is None:
            return None
        return value.isoformat()