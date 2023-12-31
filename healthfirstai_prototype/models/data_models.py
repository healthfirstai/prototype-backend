from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from typing import List
from datetime import date
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field, Relationship, Float
from pgvector.sqlalchemy import Vector

Base = declarative_base()


class NutritionVector(Base):
    __tablename__: str = "nutrition_vector"
    food_id = Column("food_id", Integer, primary_key=True)
    embedding = Column("embedding", Vector(95))


class Food(Base):
    __tablename__: str = "food"

    id = Column("id", Integer, primary_key=True)
    Name = Column(String)
    Food_Group = Column("Food Group", String)
    Calories = Column(Integer)
    Fat_g = Column("Fat (g)", Float)
    Protein_g = Column("Protein (g)", Float)
    Carbohydrate_g = Column("Carbohydrate (g)", Float)
    Sugars_g = Column("Sugars (g)", String)
    Fiber_g = Column("Fiber (g)", String)
    Cholesterol_mg = Column("Cholesterol (mg)", String)
    Saturated_Fats_g = Column("Saturated Fats (g)", String)
    Calcium_mg = Column("Calcium (mg)", String)
    Iron_Fe_mg = Column("Iron, Fe (mg)", String)
    Potassium_K_mg = Column("Potassium, K (mg)", String)
    Magnesium_mg = Column("Magnesium (mg)", String)
    Vitamin_A_IU_IU = Column("Vitamin A, IU (IU)", String)
    Vitamin_A_RAE_mcg = Column("Vitamin A, RAE (mcg)", String)
    Vitamin_C_mg = Column("Vitamin C (mg)", String)
    Vitamin_B_12_mcg = Column("Vitamin B-12 (mcg)", String)
    Vitamin_D_mcg = Column("Vitamin D (mcg)", String)
    Vitamin_E_Alpha_Tocopherol_mg = Column("Vitamin E (Alpha-Tocopherol) (mg)", String)
    Added_Sugar_g = Column("Added Sugar (g)", String)
    Net_Carbs_g = Column("Net-Carbs (g)", Float)
    Water_g = Column("Water (g)", Float)
    Omega_3s_mg = Column("Omega 3s (mg)", String)
    Omega_6s_mg = Column("Omega 6s (mg)", String)
    PRAL_score = Column("PRAL score", String)
    Trans_Fatty_Acids_g = Column("Trans Fatty Acids (g)", String)
    Soluble_Fiber_g = Column("Soluble Fiber (g)", String)
    Insoluble_Fiber_g = Column("Insoluble Fiber (g)", String)
    Sucrose_g = Column("Sucrose (g)", String)
    Glucose_Dextrose_g = Column("Glucose (Dextrose) (g)", String)
    Fructose_g = Column("Fructose (g)", String)
    Lactose_g = Column("Lactose (g)", String)
    Maltose_g = Column("Maltose (g)", String)
    Galactose_g = Column("Galactose (g)", String)
    Starch_g = Column("Starch (g)", String)
    Total_sugar_alcohols_g = Column("Total sugar alcohols (g)", String)
    Phosphorus_P_mg = Column("Phosphorus, P (mg)", String)
    Sodium_mg = Column("Sodium (mg)", Integer)
    Zinc_Zn_mg = Column("Zinc, Zn (mg)", String)
    Copper_Cu_mg = Column("Copper, Cu (mg)", String)
    Manganese_mg = Column("Manganese (mg)", String)
    Selenium_Se_mcg = Column("Selenium, Se (mcg)", String)
    Fluoride_F_mcg = Column("Fluoride, F (mcg)", String)
    Molybdenum_mcg = Column("Molybdenum (mcg)", String)
    Chlorine_mg = Column("Chlorine (mg)", String)
    Thiamin_B1_mg = Column("Thiamin (B1) (mg)", String)
    Riboflavin_B2_mg = Column("Riboflavin (B2) (mg)", String)
    Niacin_B3_mg = Column("Niacin (B3) (mg)", String)
    Pantothenic_acid_B5_mg = Column("Pantothenic acid (B5) (mg)", String)
    Vitamin_B6_mg = Column("Vitamin B6 (mg)", String)
    Biotin_B7_mcg = Column("Biotin (B7) (mcg)", String)
    Folate_B9_mcg = Column("Folate (B9) (mcg)", String)
    Folic_acid_mcg = Column("Folic acid (mcg)", String)
    Food_Folate_mcg = Column("Food Folate (mcg)", String)
    Folate_DFE_mcg = Column("Folate DFE (mcg)", String)
    Choline_mg = Column("Choline (mg)", String)
    Betaine_mg = Column("Betaine (mg)", String)
    Retinol_mcg = Column("Retinol (mcg)", String)
    Carotene_beta_mcg = Column("Carotene, beta (mcg)", String)
    Carotene_alpha_mcg = Column("Carotene, alpha (mcg)", String)
    Lycopene_mcg = Column("Lycopene (mcg)", String)
    Lutein_Zeaxanthin_mcg = Column("Lutein + Zeaxanthin (mcg)", String)
    Vitamin_D2_ergocalciferol_mcg = Column("Vitamin D2 (ergocalciferol) (mcg)", String)
    Vitamin_D3_cholecalciferol_mcg = Column(
        "Vitamin D3 (cholecalciferol) (mcg)", String
    )
    Vitamin_D_IU_IU = Column("Vitamin D (IU) (IU)", String)
    Vitamin_K_mcg = Column("Vitamin K (mcg)", String)
    Dihydrophylloquinone_mcg = Column("Dihydrophylloquinone (mcg)", String)
    Menaquinone_4_mcg = Column("Menaquinone-4 (mcg)", String)
    Fatty_acids_total_monounsaturated_mg = Column(
        "Fatty acids, total monounsaturated (mg)", String
    )
    Fatty_acids_total_polyunsaturated_mg = Column(
        "Fatty acids, total polyunsaturated (mg)", String
    )
    ccc_ALA_mg = Column("18:3 n-3 c,c,c (ALA) (mg)", String)
    EPA_mg = Column("20:5 n-3 (EPA) (mg)", String)
    DPA_mg = Column("22:5 n-3 (DPA) (mg)", String)
    DHA_mg = Column("22:6 n-3 (DHA) (mg)", String)
    Tryptophan_mg = Column("Tryptophan (mg)", String)
    Threonine_mg = Column("Threonine (mg)", String)
    Isoleucine_mg = Column("Isoleucine (mg)", String)
    Leucine_mg = Column("Leucine (mg)", String)
    Lysine_mg = Column("Lysine (mg)", String)
    Methionine_mg = Column("Methionine (mg)", String)
    Cystine_mg = Column("Cystine (mg)", String)
    Phenylalanine_mg = Column("Phenylalanine (mg)", String)
    Tyrosine_mg = Column("Tyrosine (mg)", String)
    Valine_mg = Column("Valine (mg)", String)
    Arginine_mg = Column("Arginine (mg)", String)
    Histidine_mg = Column("Histidine (mg)", String)
    Alanine_mg = Column("Alanine (mg)", String)
    Aspartic_acid_mg = Column("Aspartic acid (mg)", String)
    Glutamic_acid_mg = Column("Glutamic acid (mg)", String)
    Glycine_mg = Column("Glycine (mg)", String)
    Proline_mg = Column("Proline (mg)", String)
    Serine_mg = Column("Serine (mg)", String)
    Hydroxyproline_mg = Column("Hydroxyproline (mg)", String)
    Alcohol_g = Column("Alcohol (g)", String)
    Caffeine_mg = Column("Caffeine (mg)", String)
    Theobromine_mg = Column("Theobromine (mg)", String)
    Serving_Weight_1_g = Column("Serving Weight 1 (g)", Float)
    Serving_Description_1_g = Column("Serving Description 1 (g)", String)
    Serving_Weight_2_g = Column("Serving Weight 2 (g)", Float)
    Serving_Description_2_g = Column("Serving Description 2 (g)", String)
    Serving_Weight_3_g = Column("Serving Weight 3 (g)", Float)
    Serving_Description_3_g = Column("Serving Description 3 (g)", String)
    Serving_Weight_4_g = Column("Serving Weight 4 (g)", Float)
    Serving_Description_4_g = Column("Serving Description 4 (g)", String)
    Serving_Weight_5_g = Column("Serving Weight 5 (g)", Float)
    Serving_Description_5_g = Column("Serving Description 5 (g)", String)
    Serving_Weight_6_g = Column("Serving Weight 6 (g)", Float)
    Serving_Description_6_g = Column("Serving Description 6 (g)", String)
    Serving_Weight_7_g = Column("Serving Weight 7 (g)", Float)
    Serving_Description_7_g = Column("Serving Description 7 (g)", String)
    Serving_Weight_8_g = Column("Serving Weight 8 (g)", Float)
    Serving_Description_8_g = Column("Serving Description 8 (g)", String)
    Serving_Weight_9_g = Column("Serving Weight 9 (g)", Float)
    Serving_Description_9_g = Column("Serving Description 9 (g)", String)


class Country(SQLModel, table=True):
    __tablename__: str = "country"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    continent: str

    users: List["User"] = Relationship(back_populates="country")
    cities: List["City"] = Relationship(back_populates="country")


class City(SQLModel, table=True):
    __tablename__: str = "city"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    country_id: int = Field(foreign_key="country.id")

    country: Country = Relationship(back_populates="cities")
    users: List["User"] = Relationship(back_populates="city")


class User(SQLModel, table=True):
    __tablename__: str = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str = Field(unique=True)
    password: str
    height: float
    weight: float
    gender: str
    dob: date
    country_id: int = Field(foreign_key="country.id")
    city_id: int = Field(foreign_key="city.id")

    country: Country = Relationship(back_populates="users")
    city: City = Relationship(back_populates="users")
    personalized_daily_meal_plans: List["PersonalizedDailyMealPlan"] = Relationship(
        back_populates="user"
    )
    personalized_weekly_meal_plans: List["PersonalizedWeeklyMealPlan"] = Relationship(
        back_populates="user"
    )


class Goal(SQLModel, table=True):
    __tablename__: str = "goals"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str


class BaseWeeklyMealPlan(SQLModel, table=True):
    __tablename__: str = "base_weekly_meal_plan"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    link: str


class BaseDailyMealPlan(Base):
    __tablename__: str = "base_daily_meal_plan"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    link = Column(String(255))


class CustomWeeklyMealPlan(Base):
    __tablename__: str = "custom_weekly_meal_plan"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)


class CustomDailyMealPlan(Base):
    __tablename__: str = "custom_daily_meal_plan"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)


class PersonalizedDailyMealPlan(SQLModel, table=True):
    __tablename__: str = "personalized_daily_meal_plan"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    custom_daily_meal_plan: int = Field(foreign_key="custom_daily_meal_plan.id")
    start_date: date
    end_date: date
    goal_id: int = Field(foreign_key="goal.id")

    user: Optional[User] = Relationship(back_populates="personalized_daily_meal_plans")


class PersonalizedWeeklyMealPlan(SQLModel, table=True):
    __tablename__: str = "personalized_weekly_meal_plan"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    custom_weekly_meal_plan: int = Field(foreign_key="custom_weekly_meal_plan.id")
    start_date: date
    end_date: date
    goal_id: int = Field(foreign_key="goal.id")

    user: Optional[User] = Relationship(back_populates="personalized_weekly_meal_plans")


class Meal(Base):
    __tablename__: str = "meal"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    meal_type = Column(String(10), nullable=False)
    description = Column(Text)

    __table_args__ = (
        CheckConstraint(
            meal_type.in_(["Breakfast", "Lunch", "Dinner", "Snack", "Drink", "Other"]),
            name="meal_type_check",
        ),
    )


class UnitOfMeasurement(Base):
    __tablename__: str = "unit_of_measurement"
    unit = Column(String(255), primary_key=True)


class MealIngredient(Base):
    __tablename__: str = "meal_ingredient"
    meal_id = Column(Integer, ForeignKey("meal.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("food.id"), primary_key=True)
    unit_of_measurement = Column(
        String(255), ForeignKey("unit_of_measurement.unit"), nullable=False
    )
    quantity = Column(Float(precision=5), nullable=False)


class DailyMealPlanAndMeal(Base):
    __tablename__: str = "daily_meal_plan_and_meal"
    base_daily_meal_plan_id = Column(
        Integer, ForeignKey("base_daily_meal_plan.id"), primary_key=True
    )
    meal_id = Column(Integer, ForeignKey("meal.id"), primary_key=True)


class WeeklyMealPlanAndDailyMealPlan(Base):
    __tablename__: str = "weekly_meal_plan_and_daily_meal_plan"
    base_weekly_meal_plan_id = Column(
        Integer, ForeignKey("base_weekly_meal_plan.id"), primary_key=True
    )
    base_daily_meal_plan_id = Column(
        Integer, ForeignKey("base_daily_meal_plan.id"), primary_key=True
    )


class CustomDailyMealPlanAndMeal(Base):
    __tablename__: str = "custom_daily_meal_plan_and_meal"
    custom_daily_meal_plan_id = Column(
        Integer, ForeignKey("custom_daily_meal_plan.id"), primary_key=True
    )
    meal_id = Column(Integer, ForeignKey("meal.id"), primary_key=True)


class CustomWeeklyMealPlanAndCustomDailyMealPlan(Base):
    __tablename__: str = "custom_weekly_meal_plan_and_custom_daily_meal_plan"
    custom_weekly_meal_plan_id = Column(
        Integer, ForeignKey("custom_weekly_meal_plan.id"), primary_key=True
    )
    custom_daily_meal_plan_id = Column(
        Integer, ForeignKey("custom_daily_meal_plan.id"), primary_key=True
    )
