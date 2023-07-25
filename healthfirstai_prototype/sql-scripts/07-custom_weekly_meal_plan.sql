CREATE TABLE custom_weekly_meal_plan
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    description text         NOT NULL
);

ALTER TABLE custom_weekly_meal_plan
    OWNER TO root;

