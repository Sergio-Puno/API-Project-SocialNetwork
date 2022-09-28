-- SQL queries / commands that I used as I worked through the project
-- *Note* Some of these could have been aggregated / implemented at once rather
--   than in sequential order, this is simply how I updated and managed the DB as
--   I developed the application

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

-- Creating our "votes" table (more constraints on this table)
CREATE TABLE votes (
    post_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (post_id, user_id),
    CONSTRAINT votes_posts_fk
        FOREIGN KEY (post_id)
            REFERENCES posts(id)
            ON UPDATE NO ACTION
            ON DELETE CASCADE,
    CONSTRAINT votes_users_fk
        FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON UPDATE NO ACTION
            ON DELETE CASCADE
);