CREATE TABLE "user"
(
    id         serial
        PRIMARY KEY,
    height     numeric(5, 2) NOT NULL,
    weight     numeric(5, 2) NOT NULL,
    gender     varchar(10)   NOT NULL
        CONSTRAINT user_gender_check
            CHECK ((gender)::text = ANY
                   ((ARRAY ['Male'::character varying, 'Female'::character varying, 'Other'::character varying])::text[])),
    age        integer       NOT NULL,
    country_id integer       NOT NULL
        REFERENCES country
            ON DELETE CASCADE,
    city_id    integer       NOT NULL
        REFERENCES city
            ON DELETE CASCADE
);

ALTER TABLE "user"
    OWNER TO root;

INSERT INTO public."user" (id, height, weight, gender, age, country_id, city_id) VALUES (1, 165.50, 68.20, 'Male', 25, 1, 3);
