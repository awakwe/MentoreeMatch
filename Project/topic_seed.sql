BEGIN TRANSACTION;
CREATE TABLE topics (
	topic_id SERIAL NOT NULL, 
	title VARCHAR(100),
	PRIMARY KEY (topic_id)
);
INSERT INTO "topics" VALUES(1,"Arts & Crafts");
INSERT INTO "topics" VALUES(2,"Career & Business");
INSERT INTO "topics" VALUES(3,"Community & Environment");
INSERT INTO "topics" VALUES(4,"Education & Learning");
INSERT INTO "topics" VALUES(5,"Fitness");
INSERT INTO "topics" VALUES(6,"Food & Drinks");
INSERT INTO "topics" VALUES(7,"Health & Well Being");
INSERT INTO "topics" VALUES(8,"Language & Ethnic Identity");
INSERT INTO "topics" VALUES(9,"Life Experiences");
INSERT INTO "melons" VALUES(10,"Literature & Writing");
INSERT INTO "melons" VALUES(11,"Motivation");
INSERT INTO "melons" VALUES(12,"New Age & Spirituality");
INSERT INTO "melons" VALUES(13,"Outdoors & Adventure");
INSERT INTO "melons" VALUES(14,"Parents & Family");
INSERT INTO "melons" VALUES(15,"Peer Pressure");
INSERT INTO "melons" VALUES(16,"Pets & Animals");
INSERT INTO "melons" VALUES(17,"Religion & Beliefs");
INSERT INTO "melons" VALUES(18,"Self-improvement/Growth");
INSERT INTO "melons" VALUES(19,"Sports & Recreation");
INSERT INTO "melons" VALUES(20,"Support");
INSERT INTO "melons" VALUES(21,"Tech");
INSERT INTO "melons" VALUES(22,"Women");
COMMIT;