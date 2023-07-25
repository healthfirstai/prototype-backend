CREATE TABLE "user"
(
    id         serial
        PRIMARY KEY,
    height     numeric(5, 2) NOT NULL,
    weight     numeric(5, 2) NOT NULL,
    gender     varchar(10)   NOT NULL
        CONSTRAINT user_gender_check
            CHECK ((gender)::text = ANY
                   (ARRAY [('Male'::character varying)::text, ('Female'::character varying)::text, ('Other'::character varying)::text])),
    country_id integer       NOT NULL
        REFERENCES country
            ON DELETE CASCADE,
    city_id    integer       NOT NULL
        REFERENCES city
            ON DELETE CASCADE,
    first_name varchar(50),
    last_name  varchar(50),
    username   varchar(50),
    password   varchar(100),
    dob        date
);

ALTER TABLE "user"
    OWNER TO root;

INSERT INTO public."user" (id, height, weight, gender, country_id, city_id, first_name, last_name, username, password, dob) VALUES (1, 180.50, 75.20, 'Male', 1, 3, 'John', 'Doe', 'johndoe123', 'password123', '1990-07-22');
