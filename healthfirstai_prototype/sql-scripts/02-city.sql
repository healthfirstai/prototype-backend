CREATE TABLE city
(
    id         serial
        PRIMARY KEY,
    name       varchar(255) NOT NULL,
    country_id integer      NOT NULL
        REFERENCES country
            ON DELETE CASCADE
);

ALTER TABLE city
    OWNER TO root;

INSERT INTO public.city (id, name, country_id) VALUES (3, 'New York City', 1);
