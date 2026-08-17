from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from app.database import get_database
from app.models.equipment import Equipment

router = APIRouter()

@router.post("/", response_model=Equipment, status_code=status.HTTP_201_CREATED)
async def create_equipment(equipment: Equipment):
    
    """Get DB"""
    db = get_database()
    
    # Check if equipment name already exists
    existing = await db.equipment.find_one({"name": equipment.name, "tenant_id": equipment.tenant_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Equipment with this name already exists"
        )
    
    # Add timestamps
    now = datetime.now(timezone.utc)
    equipment_dict = equipment.model_dump(exclude={"id"}, exclude_none=True)
    equipment_dict["created_at"] = now
    equipment_dict["updated_at"] = now
    
    # Insert into database
    result = await db.equipment.insert_one(equipment_dict)
    
    # Create response with _id as string
    response_dict = equipment.model_dump(exclude={"id"}, exclude_none=True)
    response_dict["_id"] = str(result.inserted_id)
    return Equipment(**response_dict)
    """List all documents for an equipment"""
    db = get_database()
    
    # Verify equipment exists
    equipment = await db.equipment.find_one({"_id": ObjectId(equipment_id)})
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    documents = await db.documents_metadata.find({
        "equipment_id": ObjectId(equipment_id),
        "is_disabled": {"$ne": True}
    }).to_list(length=1000)
    
    # Convert ObjectId and datetime fields to strings for JSON serialization
    serialized_documents = []
    for doc in documents:
        doc_dict = dict(doc)
        if '_id' in doc_dict and isinstance(doc_dict['_id'], ObjectId):
            doc_dict['_id'] = str(doc_dict['_id'])
        if 'equipment_id' in doc_dict and isinstance(doc_dict['equipment_id'], ObjectId):
            doc_dict['equipment_id'] = str(doc_dict['equipment_id'])
        if 'created_at' in doc_dict and isinstance(doc_dict['created_at'], datetime):
            doc_dict['created_at'] = doc_dict['created_at'].isoformat()
        if 'updated_at' in doc_dict and isinstance(doc_dict['updated_at'], datetime):
            doc_dict['updated_at'] = doc_dict['updated_at'].isoformat()
        serialized_documents.append(doc_dict)
    
    return {"documents": serialized_documents, "count": len(serialized_documents)}