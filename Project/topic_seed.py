import tabledef
from tabledef import Topic

TOPICS = {1: "Arts & Crafts",
		2: "Career & Business",
		3: "Community & Environment",
		4: "Education & Learning",
		5: "Fitness",
		6: "Food & Drinks",
		7: "Health & Well Being",
		8: "Language & Ethnic Identity",
		9: "Life Experiences",
		10: "Literature & Writing",
		11: "Motivation",
		12: "New Age & Spirituality",
		13: "Outdoors & Adventure",
		14: "Parents & Family",
		15: "Peer Pressure",
		16: "Pets & Animals",
		17: "Religion & Beliefs",
		18: "Self-improvement/Growth",
		19: "Sports & Recreation",
		20: "Support",
		21: "Tech",
		22: "Women"}

def seed_topic_table():
	topics = []
	for items in TOPICS:
		topics.append(Topic(title=TOPICS[items]))
	print "~~~~~ TOPICS ~~~~~~~"
	print topics
	tabledef.dbsession.add_all(topics)
	tabledef.dbsession.commit()

seed_topic_table()