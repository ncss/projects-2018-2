CREATE TABLE users (
  id INTEGER NOT NULL,
  username TEXT NOT NULL,
  pword TEXT NOT NULL,
  fname TEXT,
  sname TEXT,
  email TEXT NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE charity (
  id INTEGER NOT NULL,
  name TEXT NOT NULL,
  category TEXT,
  story TEXT,
  charity_website_url TEXT,
  image_src TEXT,
  admin_id INTEGER, 
  FOREIGN KEY (admin_id) REFERENCES users (id),
  PRIMARY KEY (id)
);

CREATE TABLE charity_followers (
  charity_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (charity_id) REFERENCES charity (id),
  PRIMARY KEY (user_id,charity_id)
);

CREATE TABLE friends (
  user_id1 INTEGER NOT NULL,
  user_id2 INTEGER NOT NULL,
  FOREIGN KEY (user_id1) REFERENCES users (id),
  FOREIGN KEY (user_id2) REFERENCES users (id),
  PRIMARY KEY (user_id1, user_id2)
);


/* FAKE DATA */
INSERT INTO users(id,username,pword,email) VALUES (0, 'foo', 'bar', 'baz@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (1, 'bob', 'abc', 'bob@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (2, 'fred', '1234', 'george@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (3, 'percy', 'trident', 'riptide@snailmail.com');

INSERT INTO charity(id, name, story) VALUES (4, 'snail helpline', 'we help sad snails');
INSERT INTO charity(id, name, category, admin_id) VALUES (5, 'abc', 'we help sad snails',1);