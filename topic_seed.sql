BEGIN TRANSACTION;
CREATE TABLE topics (
	topic_id SERIAL NOT NULL, 
	title VARCHAR(100),
	PRIMARY KEY (topic_id)
);
INSERT INTO "topics" VALUES(1,'Arts & Crafts');
INSERT INTO "topics" VALUES(2,'Career & Business');
INSERT INTO "topics" VALUES(3,'Community & Environment');
INSERT INTO "topics" VALUES(4,'Education & Learning');
INSERT INTO "topics" VALUES(5,'Fitness');
INSERT INTO "topics" VALUES(6,'Food & Drinks');
INSERT INTO "topics" VALUES(7,'Health & Well Being');
INSERT INTO "topics" VALUES(8,'Language & Ethnic Identity');
INSERT INTO "topics" VALUES(9,'Life Experiences');
INSERT INTO "topics" VALUES(10,'Literature & Writing');
INSERT INTO "topics" VALUES(11,'Motivation');
INSERT INTO "topics" VALUES(12,'New Age & Spirituality');
INSERT INTO "topics" VALUES(13,'Outdoors & Adventure');
INSERT INTO "topics" VALUES(14,'Parents & Family');
INSERT INTO "topics" VALUES(15,'Peer Pressure');
INSERT INTO "topics" VALUES(16,'Pets & Animals');
INSERT INTO "topics" VALUES(17,'Religion & Beliefs');
INSERT INTO "topics" VALUES(18,'Self-improvement/Growth');
INSERT INTO "topics" VALUES(19,'Sports & Recreation');
INSERT INTO "topics" VALUES(20,'Support');
INSERT INTO "topics" VALUES(21,'Tech');
INSERT INTO "topics" VALUES(22,'Women');


COMMIT;