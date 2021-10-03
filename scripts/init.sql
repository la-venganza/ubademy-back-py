CREATE TABLE IF NOT EXISTS course(
	id serial PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	length INTEGER NOT NULL,
    year INTEGER NOT NULL,
	teacher VARCHAR(40) NOT NULL,
    subject VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_account(
	id serial PRIMARY KEY,
	user_id VARCHAR(255) UNIQUE NOT NULL,
	first_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NULL,
    email VARCHAR(255) NOT NULL,
	role VARCHAR(40) NULL,
    is_admin BOOLEAN NOT NULL
);

CREATE INDEX IF NOT EXISTS user_account_user_id_idx ON user_account USING btree (user_id);
CREATE INDEX IF NOT EXISTS user_account_email_idx ON user_account USING btree (email);