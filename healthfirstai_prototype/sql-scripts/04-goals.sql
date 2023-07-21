CREATE TABLE goals
(
    id          serial
        PRIMARY KEY,
    name        varchar(255) NOT NULL,
    description text         NOT NULL
);

ALTER TABLE goals
    OWNER TO root;

INSERT INTO public.goals (id, name, description) VALUES (1, 'Lose Fat', 'For people who are trying to lost fat mainly for aesthetic reasons');
INSERT INTO public.goals (id, name, description) VALUES (2, 'Gain Muscle', 'For people who are trying to gain muscle mainly for aesthetic reasons');
INSERT INTO public.goals (id, name, description) VALUES (3, 'Get Healthy', 'For people who are trying to maintain their current weight and get healthy');
