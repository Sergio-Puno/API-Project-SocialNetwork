-- Creating our "posts" table
CREATE TABLE users
(
    id serial NOT NULL,
    title character varying NOT NULL,
    content character varying NOT NULL,
    published boolean NOT NULL DEFAULT TRUE,
    read_time integer NOT NULL DEFAULT 5,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);

-- Creating our "users" table
CREATE TABLE users
(
    id serial NOT NULL,
    email character varying NOT NULL UNIQUE,
    password character varying NOT NULL,
    created_at timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);

-- Adding foreign key to posts table: posts[user_id] == users[id]
ALTER TABLE IF EXISTS public.posts
    ADD COLUMN user_id integer NOT NULL;
ALTER TABLE IF EXISTS public.posts
    ADD CONSTRAINT posts_users_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;