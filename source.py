# Import Spellchecker
from spellchecker import SpellChecker

# Import mysqlconnector
import mysql.connector

# variables
spell = SpellChecker()

correct = None

word = input("Enter the word: ")

# function to connect to db
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            user = "ardit700_student",
            password = "ardit700_student",
            host = "108.167.140.122",
            database = "ardit700_pm1database"
        )
        print("\nMySQL Database connection successful!!!\n")
    except mysql.connector.Error as err:
        print(err)
    return connection

# function to query the db
def read_query(connection,word):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute("SELECT Definition FROM Dictionary WHERE Expression='%s'" % word)
        results = cursor.fetchall()
        if cursor.rowcount is 0:
            global correct
            correct = spell.correction(word)
    except mysql.connector.errors as err:
        print(err)
    return results

# function to check the results
def check_results():
    connection = create_db_connection()
    results = read_query(connection,word)
    if results:
        print("The word " + word + " means:\n")
        for result in results:
            print("\033[1m" + result[0] + "\033[0m") 
    return results 
 
# check and return the result or spell the word and return the result
if check_results():
    pass
elif correct is not None:
    i = 1
    while i > 0:
        confirm = input('Did you mean' +" "+ correct + '?' + " " + "[Yes/No]").lower()
        if confirm in ['yes','y']:
            word = correct
            corrected_answer = check_results()
            if not corrected_answer:
                print('This word was not found in the database')
            i = 0
        elif confirm in ['no','n']:
            print('\nWe did not understand your query')
            i = 0
        else:
            continue