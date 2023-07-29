CREATE TABLE base_weekly_meal_plan
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    description text         NOT NULL,
    link        varchar(255)
);

ALTER TABLE base_weekly_meal_plan
    OWNER TO root;

