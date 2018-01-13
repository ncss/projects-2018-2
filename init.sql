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


/* EXAMPLE DATA */
INSERT INTO users(id,username,pword,email) VALUES (0, 'foo', 'bar', 'baz@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (1, 'bob', 'abc', 'bob@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (2, 'fred', '1234', 'george@snailmail.com');
INSERT INTO users(id,username,pword,email) VALUES (3, 'percy', 'trident', 'riptide@snailmail.com');

INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (0, 'One Laptop Per Child', 'We aim to provide each child with a rugged, low-cost, low-power, connected laptop. To this end, we have designed hardware, content and software for collaborative, joyful, and self-empowered learning. With access to this type of tool, children are engaged in their own education, and learn, share, and create together. They become connected to each other, to the world and to a brighter future.','http://one.laptop.org/','http://www.graphis.com/media/uploads/cache/d6/e4/d6e4d35422db27b1bb7859ec84944e96.jpg');
INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (1, 'UNICEF Australia', 'UNICEF is the United Nations Children’s Fund, working in 190 countries for the survival, protection and development of every child, with a focus on the lives of children who are the most disadvantaged and excluded.','https://www.unicef.org.au/','https://pbs.twimg.com/profile_images/934936882047098880/TWJOb4cQ.jpg');
INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (2, 'Snail Helpline', 'We help sad snails.','https://hotspicyme.me/','https://i.imgur.com/eg65Bh8.png');
INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (3, 'The Afghan School Project', 'The Afghan School Project is an international volunteer initiative to support the Kandahar Institute of Modern Studies (KIMS), a professional educational institution in Kandahar, Afghanistan. KIMS provides more than 1,500 women and men with the opportunity to receive education in Business Management, Information Technology, English and Communications, while providing members of the community with access to the Internet and online classes from Canadian and international institutions.
The school’s programs provide students with the skills needed to obtain employment to support themselves and their families, improve their communities and participate in the reconstruction of Afghanistan. The skills taught at KIMS are in high demand by international development agencies, local businesses and the Afghan government.
','http://www.theafghanschool.org/aboutus/','https://scontent.fcbr1-1.fna.fbcdn.net/v/t1.0-1/c38.27.336.336/s200x200/229643_10150317761129980_1537552636_n.jpg?oh=3ee8592fba9d3b601729a34cc6be64d8&oe=5AF0933C');
INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (4, 'Oxfam', "When disaster strikes Oxfam's priority is to start saving lives, then to help people come back stronger.
We make sure people can get clean water to drink and decent sanitation. We provide help for people to get food and the essentials they need to survive and ensure the most vulnerable are kept safe from harm.
We support them in being better prepared to cope with shocks and uncertainties and we help rebuild communities to come back stronger from disaster and to face the future on their own terms. We're responding to emergencies around the world right now.
",'https://www.oxfam.org.uk/what-we-do','http://sustainability.ceres.org.au/wp-content/uploads/sites/4/2014/07/oxfam-australia-logo.png');
INSERT INTO charity(id,name,story,charity_website_url,image_src) VALUES (5, "Variety - the Children's Charity", 'All children should be able to follow their dreams and be the best they can be. No matter what life throws at them. No matter what their ability.

Each year, thousands of children who are sick, disadvantaged or have special needs, get support from Variety the Children’s Charity when they need it most.','https://www.variety.org.au/vic/','https://i.vimeocdn.com/portrait/1371430_640x640');