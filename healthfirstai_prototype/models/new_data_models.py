from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from pgvector.sqlalchemy import Vector


class FoodNutritionVector(SQLModel, table=True):
    __tablename__: str = "food_nutrition_vector"

    food_id: int = Field(foreign_key="food_info.id", primary_key=True)
    embedding: Vector


class FoodInfo(SQLModel, table=True):
    __tablename__: str = "food_info"

    id: int = Field(primary_key=True)
    name: str
    food_group: Optional[str] = Field(default=None)

    food_nutrition_vector: Optional["FoodNutritionVector"] = Relationship(
        back_populates="food"
    )
    nutrients: List["Nutrient"] = Relationship(back_populates="food")


class FoodInfoNutrientLink(SQLModel, table=True):
    __tablename__: str = "food_info_nutrient_link"

    food_id: Optional[int] = Field(
        default=None, foreign_key="food_info.id", primary_key=True
    )
    nutrient_id: Optional[int] = Field(
        default=None, foreign_key="nutrient.id", primary_key=True
    )
    value: Optional[float] = Field(default=0.0)


class Nutrient(SQLModel, table=True):
    __tablename__: str = "nutrient"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str

    food: List[FoodInfo] = Relationship(back_populates="nutrients")
