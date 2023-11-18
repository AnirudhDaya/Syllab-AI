# Database connectivity - MongoDB
# ================================
import re
from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Create/connect to the database
database = client['question_database']

# Save the extracted topics based on the questions
def db_questions(all_responses, collection_name):
    # Create/connect to the collection
    collection_list = database.list_collection_names()
    if collection_name in collection_list:
        # print(f"Collection '{collection_name}' already exists.")
        print(" ")
    else:
        # Create a new collection
        database.create_collection(collection_name)
        # print(f"Collection '{collection_name}' created successfully!")
    
    collection = database[collection_name]

    # Extract the topic and question data from the string
    pattern = r'\d+\.\s+(.*?)\s+\((\d+)\s+questions\)'
    matches = re.findall(pattern, all_responses)

    # Iterate over the extracted topics and questions
    for match in matches:
        topic = match[0]
        questions = int(match[1])
        # print("for loop")
        # Check if the topic already exists in the database
        existing_topic = collection.find_one({"topic": topic})

        if existing_topic:
            # Update the number of questions for the existing topic
            # print("existing")
            existing_questions = existing_topic['questions']
            updated_questions = existing_questions + questions

            # Update the document in the collection
            collection.update_one({"topic": topic}, {"$set": {"questions": updated_questions}})
        else:
            # Create a new document for the topic
            # print("new topic")
            new_topic = {"topic": topic, "questions": questions}
            collection.insert_one(new_topic)

    # Print a success message
    # print("\n\nTopics inserted/updated in the database successfully!")


def CheckIfFileExistsInDatabase(filename):
    collection = database['question_papers']
    existing_topic = collection.find_one({"Paper": filename})
    if existing_topic:
        return True
    else:
        collection.insert_one({"Paper": filename})
        return False

def TopTenTopics(collection_name):
    collection = database[collection_name]
    topics = collection.find().sort("questions", -1).limit(10)
    i=0
    topten=""
    for i, topic in enumerate(topics, 1):
        topten += str(i) + ". " + topic['topic'] + "\n"

    return topten