import pickle

topics = {1: 'electric car', 2: 'touchscreen display', 3: 'car accident', 4: 'coffee', 5: 'car'}

pickle.dump(topics, open('../test_topics.p', 'wb'))
