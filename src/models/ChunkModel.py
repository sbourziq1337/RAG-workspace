from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_none=True))
        chunk.id = str(result.inserted_id)
        return chunk
    
    async def get_chunk(self, chunk_id: str):
        try:
            oid = ObjectId(chunk_id)
        except Exception:
            return None

        result = await self.collection.find_one({
            "_id" : oid
        })
        if result is None:
            return None
        
        
        
        return DataChunk(**result)
    
    async def insert_many_chunk(self, chunks: list[DataChunk], batch_size: int = 100):
        inserted_chunks = []
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            batch_dicts = [c.model_dump(by_alias=True, exclude_none=True) for c in batch]
            if not batch_dicts:
                continue
            result = await self.collection.insert_many(batch_dicts)
            for chunk, inserted_id in zip(batch, result.inserted_ids):
                chunk.id = str(inserted_id)
                inserted_chunks.append(chunk)
        return inserted_chunks