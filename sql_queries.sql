CREATE TABLE user (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(255) NOT NULL,
  password text NOT NULL,
  email varchar(255) NOT NULL,
  first_name varchar(255) DEFAULT NULL,
  last_name varchar(255) DEFAULT NULL,
  bio text,
  avatar_url text,
  last_seen datetime DEFAULT NULL,
  created_at datetime DEFAULT CURRENT_TIMESTAMP,
  updated_at datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY username (username),
  UNIQUE KEY email (email)
);

CREATE TABLE places (
    id int NOT NULL AUTO_INCREMENT,
    country varchar(255) NOT NULL,
    state varchar(255),
    city varchar(255) NOT NULL,
    placename varchar(255) NOT NULL,
    lat float NOT NULL,
    lng float NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE routes (
    id int NOT NULL AUTO_INCREMENT,
	routename varchar(255) NOT NULL,
	usersid int,
	placesid int,
	PRIMARY KEY (id),
    CONSTRAINT FK_routes_user FOREIGN KEY (usersid) REFERENCES user(id),
    CONSTRAINT FK_routes_places FOREIGN KEY (placesid) REFERENCES places(id)
);

CREATE TABLE comments (
    id int NOT NULL AUTO_INCREMENT,
    comment_text text,
    routestatus varchar(4),
	usersid int,
	placesid int,
	PRIMARY KEY (id),
    CONSTRAINT FK_comments_user FOREIGN KEY (usersid) REFERENCES user(id),
    CONSTRAINT FK_comments_places FOREIGN KEY (placesid) REFERENCES places(id)
);


INSERT INTO comments(comment_text,routestatus,usersid,placesid) 
VALUES ("comentario 1","Done",1,1);
INSERT INTO comments(comment_text,routestatus,usersid,placesid) 
VALUES ("comentario 2","Done",1,2);
INSERT INTO comments(comment_text,routestatus,usersid,placesid) 
VALUES ("comentario 3","Done",3,3);
INSERT INTO comments(comment_text,routestatus,usersid,placesid) 
VALUES ("comentario 4","Done",4,4);
INSERT INTO comments(comment_text,routestatus,usersid,placesid) 
VALUES ("comentario 5","Done",5,5);