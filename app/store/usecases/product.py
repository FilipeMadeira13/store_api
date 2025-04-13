from datetime import datetime
from fastapi import HTTPException, status
from store.models.product import ProductModel
import pymongo
from typing import List, Optional
from uuid import UUID
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())

        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(
        self, min_price: Optional[float] = None, max_price: Optional[float] = None
    ) -> List[ProductOut]:
        try:
            query_filter = {}

            if min_price is not None or max_price is not None:
                price_filter = {}

                if min_price is not None:
                    price_filter["$gt"] = min_price

                if max_price is not None:
                    price_filter["$lt"] = max_price

                if price_filter:
                    query_filter["price"] = price_filter

            return [
                ProductOut(**item) async for item in self.collection.find(query_filter)
            ]
        except Exception as err:
            print(f"Error in filter_by_price endpoint: {str(err)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao filtrar produtos por preço: {str(err)}",
            )

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        update_data = body.model_dump(exclude_none=True)

        update_data["updated_at"] = datetime.now()

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        # Cria uma condição caso o resultado seja None
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found with filter: {id}",
            )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})

        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
