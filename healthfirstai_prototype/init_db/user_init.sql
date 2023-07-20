DROP TABLE IF EXISTS "custom_weekly_meal_plan_and_custom_daily_meal_plan";
DROP TABLE IF EXISTS "custom_daily_meal_plan_and_meal";
DROP TABLE IF EXISTS "weekly_meal_plan_and_daily_meal_plan";
DROP TABLE IF EXISTS "daily_meal_plan_and_meal";
DROP TABLE IF EXISTS "meal_ingredient";
DROP TABLE IF EXISTS "unit_of_measurement";
DROP TABLE IF EXISTS "meal";
DROP TABLE IF EXISTS "personalized_weekly_meal_plan";
DROP TABLE IF EXISTS "personalized_daily_meal_plan";
DROP TABLE IF EXISTS "custom_weekly_meal_plan";
DROP TABLE IF EXISTS "custom_daily_meal_plan";
DROP TABLE IF EXISTS base_daily_meal_plan;
DROP TABLE IF EXISTS base_weekly_meal_plan;
DROP TABLE IF EXISTS "goals";
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS "city";
DROP TABLE IF EXISTS "country";

CREATE TABLE "country"
(
    "id"        SERIAL PRIMARY KEY,
    "name"      VARCHAR(255) NOT NULL,
    "continent" VARCHAR(255) NOT NULL
);

CREATE TABLE "city"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       VARCHAR(255) NOT NULL,
    "country_id" INT          NOT NULL,
    FOREIGN KEY ("country_id") REFERENCES "country" ("id") ON DELETE CASCADE
);

CREATE TABLE "user"
(
    "id"         SERIAL PRIMARY KEY,
    "height"     DECIMAL(5, 2) NOT NULL,
    "weight"     DECIMAL(5, 2) NOT NULL,
    "gender"     VARCHAR(10)   NOT NULL CHECK ("gender" IN ('Male', 'Female', 'Other')),
    "age"        INT           NOT NULL,
    "country_id" INT           NOT NULL,
    "city_id"    INT           NOT NULL,
    FOREIGN KEY ("country_id") REFERENCES "country" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("city_id") REFERENCES "city" ("id") ON DELETE CASCADE
);

CREATE TABLE "goals"
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "description" TEXT         NOT NULL
);


CREATE TABLE base_weekly_meal_plan
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "description" TEXT         NOT NULL,
    "link"        VARCHAR(255)
);

CREATE TABLE base_daily_meal_plan
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "description" TEXT         NOT NULL,
    "link"        VARCHAR(255)
);

CREATE TABLE custom_weekly_meal_plan
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "description" TEXT         NOT NULL
);

CREATE TABLE custom_daily_meal_plan
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "description" TEXT         NOT NULL
);

CREATE TABLE personalized_daily_meal_plan
(
    "id"                     SERIAL PRIMARY KEY,
    "user_id"                INT  NOT NULL,
    "custom_daily_meal_plan" INT  NOT NULL,
    "start_date"             DATE NOT NULL,
    "end_date"               DATE NOT NULL,
    "goal_id"                INT  NOT NULL,
    FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("custom_daily_meal_plan") REFERENCES "custom_daily_meal_plan" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("goal_id") REFERENCES "goals" ("id") ON DELETE CASCADE
);

CREATE TABLE "personalized_weekly_meal_plan"
(
    "id"                      SERIAL PRIMARY KEY,
    "user_id"                 INT  NOT NULL,
    "custom_weekly_meal_plan" INT  NOT NULL,
    "start_date"              DATE NOT NULL,
    "end_date"                DATE NOT NULL,
    "goal_id"                 INT  NOT NULL,
    FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("custom_weekly_meal_plan") REFERENCES "custom_weekly_meal_plan" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("goal_id") REFERENCES "goals" ("id") ON DELETE CASCADE
);

CREATE TABLE "meal"
(
    "id"          SERIAL PRIMARY KEY,
    "name"        VARCHAR(255) NOT NULL,
    "meal_type"   VARCHAR(10)  NOT NULL CHECK ("meal_type" IN
                                               ('Breakfast', 'Lunch', 'Dinner', 'Snack', 'Drink', 'Other')),
    "description" TEXT
);

CREATE TABLE "unit_of_measurement"
(
    "unit" VARCHAR(255) PRIMARY KEY
);

CREATE TABLE "meal_ingredient"
(
    "meal_id"           INT           NOT NULL,
    "ingredient_id"     INT           NOT NULL,
    unit_of_measurement VARCHAR(255)  NOT NULL,
    "quantity"          DECIMAL(5, 2) NOT NULL,
    PRIMARY KEY ("meal_id", "ingredient_id"),
    FOREIGN KEY ("meal_id") REFERENCES "meal" ("id") ON DELETE CASCADE,
    FOREIGN KEY ("ingredient_id") REFERENCES "food" ("id") ON DELETE CASCADE,
    FOREIGN KEY (unit_of_measurement) REFERENCES "unit_of_measurement" ("unit") ON DELETE CASCADE
);

CREATE TABLE "daily_meal_plan_and_meal"
(
    "base_daily_meal_plan_id" INT NOT NULL,
    "meal_id"                 INT NOT NULL,
    PRIMARY KEY ("base_daily_meal_plan_id", "meal_id"),
    FOREIGN KEY ("base_daily_meal_plan_id") REFERENCES base_daily_meal_plan ("id") ON DELETE CASCADE,
    FOREIGN KEY ("meal_id") REFERENCES "meal" ("id") ON DELETE CASCADE
);

CREATE TABLE "weekly_meal_plan_and_daily_meal_plan"
(
    "base_weekly_meal_plan_id" INT NOT NULL,
    "base_daily_meal_plan_id"  INT NOT NULL,
    PRIMARY KEY ("base_daily_meal_plan_id", "base_weekly_meal_plan_id"),
    FOREIGN KEY ("base_daily_meal_plan_id") REFERENCES base_daily_meal_plan ("id") ON DELETE CASCADE,
    FOREIGN KEY ("base_weekly_meal_plan_id") REFERENCES base_weekly_meal_plan ("id") ON DELETE CASCADE
);

CREATE TABLE "custom_daily_meal_plan_and_meal"
(
    "custom_daily_meal_plan_id" INT NOT NULL,
    "meal_id"                   INT NOT NULL,
    PRIMARY KEY ("custom_daily_meal_plan_id", "meal_id"),
    FOREIGN KEY ("custom_daily_meal_plan_id") REFERENCES custom_daily_meal_plan ("id") ON DELETE CASCADE,
    FOREIGN KEY ("meal_id") REFERENCES "meal" ("id") ON DELETE CASCADE
);

CREATE TABLE "custom_weekly_meal_plan_and_custom_daily_meal_plan"
(
    "custom_weekly_meal_plan_id" INT NOT NULL,
    "custom_daily_meal_plan_id"  INT NOT NULL,
    PRIMARY KEY ("custom_daily_meal_plan_id", "custom_weekly_meal_plan_id"),
    FOREIGN KEY ("custom_daily_meal_plan_id") REFERENCES custom_daily_meal_plan ("id") ON DELETE CASCADE,
    FOREIGN KEY ("custom_weekly_meal_plan_id") REFERENCES custom_weekly_meal_plan ("id") ON DELETE CASCADE
);
