import pickle

TOP_TAG = '<top>'
TOP_CLOSE_TAG = '</top>'
NUMBER_TAG = '<num>'
TITLE_TAG = '<title>'
RESTRICTED_TOPICS = [416, 423, 437, 444, 447]

topics = {}
with open('../topics.401-450.txt', mode='rt') as f:
    new_topic = False
    number = 0
    title = ''

    for line in f:
        if TOP_TAG in line:
            new_topic = True

        elif NUMBER_TAG in line and new_topic:
            # Line format: <num> Number: DDD
            number = int(line.split(" ")[2])

        elif TITLE_TAG in line and new_topic:
            # Line format: <title> {title}
            title = line[8:]

        elif TOP_CLOSE_TAG in line:
            if number not in RESTRICTED_TOPICS:
                topics[number] = title

            # Clear document-specific data
            new_topic = False

pickle.dump(topics, open('../topics.p', 'wb'))

