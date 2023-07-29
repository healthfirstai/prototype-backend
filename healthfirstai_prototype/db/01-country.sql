CREATE TABLE country
(
    id        serial
        PRIMARY KEY,
    name      varchar(255) NOT NULL,
    continent varchar(255) NOT NULL
);

ALTER TABLE country
    OWNER TO root;

INSERT INTO public.country (id, name, continent) VALUES (1, 'United States', 'North America');
