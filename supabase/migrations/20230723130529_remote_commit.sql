create table "public"."message" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone default now(),
    "user_id" character varying not null,
    "message" text not null,
    "target_response_id" uuid
);


alter table "public"."message" enable row level security;

create table "public"."response" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone default now(),
    "target_user_id" character varying not null,
    "response" text,
    "action" json,
    "target_message_response" uuid
);


alter table "public"."response" enable row level security;

create table "public"."user_info" (
    "id" uuid not null default gen_random_uuid(),
    "created_at" timestamp with time zone default now(),
    "user_id" character varying not null,
    "height" numeric,
    "weight" numeric,
    "age" smallint
);


alter table "public"."user_info" enable row level security;

CREATE UNIQUE INDEX message_pkey ON public.message USING btree (id);

CREATE UNIQUE INDEX response_pkey ON public.response USING btree (id);

CREATE UNIQUE INDEX user_info_pkey ON public.user_info USING btree (id);

CREATE UNIQUE INDEX user_info_user_id_key ON public.user_info USING btree (user_id);

alter table "public"."message" add constraint "message_pkey" PRIMARY KEY using index "message_pkey";

alter table "public"."response" add constraint "response_pkey" PRIMARY KEY using index "response_pkey";

alter table "public"."user_info" add constraint "user_info_pkey" PRIMARY KEY using index "user_info_pkey";

alter table "public"."message" add constraint "message_target_response_id_fkey" FOREIGN KEY (target_response_id) REFERENCES response(id) ON DELETE SET NULL not valid;

alter table "public"."message" validate constraint "message_target_response_id_fkey";

alter table "public"."response" add constraint "response_target_message_response_fkey" FOREIGN KEY (target_message_response) REFERENCES message(id) ON DELETE SET NULL not valid;

alter table "public"."response" validate constraint "response_target_message_response_fkey";

alter table "public"."user_info" add constraint "user_info_user_id_key" UNIQUE using index "user_info_user_id_key";


