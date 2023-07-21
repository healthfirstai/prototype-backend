CREATE TABLE unit_of_measurement
(
    unit varchar(255) NOT NULL
        PRIMARY KEY
);

ALTER TABLE unit_of_measurement
    OWNER TO root;

INSERT INTO public.unit_of_measurement (unit) VALUES ('cups');
INSERT INTO public.unit_of_measurement (unit) VALUES ('units');
INSERT INTO public.unit_of_measurement (unit) VALUES ('tbsp');
INSERT INTO public.unit_of_measurement (unit) VALUES ('scoops');
INSERT INTO public.unit_of_measurement (unit) VALUES ('leaves');
INSERT INTO public.unit_of_measurement (unit) VALUES ('oz');
INSERT INTO public.unit_of_measurement (unit) VALUES ('slices');
INSERT INTO public.unit_of_measurement (unit) VALUES ('bar');
INSERT INTO public.unit_of_measurement (unit) VALUES ('cubes');
