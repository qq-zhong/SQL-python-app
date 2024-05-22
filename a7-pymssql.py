# Dear TA:
#     this assignment was originally written and tested on my m1 mac, upon testing on a csil linux machine, i found pyodbc was not implementable, and 
#     had to swtich over to using pymssql, i hope the code works for you, if pymssql dones't work for you, you could try to revert code back to
#     using pyodbc, for which you need to:
#         change every %s to ? in all query strings
#         uncomment all lines:
#          # conn = pyodbc.connect(connection_string)
#         then comment all lines of:
#         conn = pymssql.connect(host=server, user=username, password=password, database=database)

import pyodbc
import pymssql
from datetime import datetime
import sys
server = 'cypress.csil.sfu.ca'
database = 'qqz354'
username = 's_qqz'
password = '2hNjJqFRf3na643Q'
driver = '{ODBC Driver 18 for SQL Server}'  # or '{ODBC Driver 13 for SQL Server}'
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
#connection_string = f'driver={driver};server={server};Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes'



def generate_variable(username):
    # Truncate or limit the username to 5 characters
    truncated_username = username[:5]

    # Get the current date-time in a specific format (YYMMDDHHMMSS)
    current_date_time = datetime.now().strftime('%y%m%d%H%M%S')

    # Combine the truncated username and date-time to create a 22-character variable
    generated_variable = f"{truncated_username:5}{current_date_time:17}"

    # Replace any whitespace with underscores
    generated_variable = generated_variable.replace(' ', '_')

    return generated_variable[:22]  # Return the first 22 characters

def login():
    global username, password
    # Asking user for username and password
    print("Would you like to use my (Peter) login and password?:")
    print("yes -> use Peter's login and password")
    print("no -> enter your own login and password")
    print("enter 'quit' to Quit")
    
    while True :
        choice = input("Enter your choice (yes/no/quit): ")
        if choice == 'yes':
            break
        elif choice == 'no':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
        elif choice == 'quit':
            sys.exit()
        else:
            print("invalid input, please try again")

    

    # Here you can perform validation or checks against stored usernames/passwords
    # For this example, let's just print the entered credentials
    
    
    print(f"using username: {username}")
    print(f"using password: {password}")

def makeConnection():
    try:
        # Establish the connection
        # conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_qqz;pwd=2hNjJqFRf3na643Q;database=qqz354')
        #conn = pyodbc.connect('driver={ODBC Driver 18 for SQL Server};server=cypress.csil.sfu.ca;uid=s_qqz;pwd=2hNjJqFRf3na643Q;Encrypt=yes;TrustServerCertificate=yes')
        #conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_qqz', password='2hNjJqFRf3na643Q', database='qqz354')
        conn = pymssql.connect(host=server, user=username, password=password, database=database)

        print("welcome to the database")
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")


def search_business():
    print('')
    print("searching for business")
    # conn = pyodbc.connect(connection_string)
    conn = pymssql.connect(host=server, user=username, password=password, database=database)
    cursor = conn.cursor()


    # min_stars = '1'
    # city = 'Edmonton'
    # name = 'pub'
    min_stars = input("Enter the minimum number of stars: ")
    city = input("Enter the city: ")
    name = input("Enter the name or part of the name: ")
    
    print("Choose the ordering of results:")
    print("1. By name")
    print("2. By city")
    print("3. By number of stars")
    choice = input("Enter your choice (1/2/3): ")

    # Mapping user's choice to SQL ordering
    ordering = {
        '1': 'name',
        '2': 'city',
        '3': 'stars'
    }.get(choice)

    if ordering is None:
        print("Invalid choice. Exiting.")
        return


    # SQL query to search for businesses based on user input
    query = f"""
    SELECT * 
    FROM Business 
    WHERE stars >= %s 
    AND LOWER(city) = LOWER(%s) 
    AND LOWER(name) LIKE LOWER(%s)
    ORDER BY {ordering}
"""
    #print(f'%{name}%')
    cursor.execute(query, (min_stars, city, f'%{name}%'))
    results = cursor.fetchall()
    if results:
        print("Search Results:")
        for row in results:
            print(row) 
    else:
        print("No businesses found based on the provided criteria.")

def search_user():
    print('')
    print("searching for user")
    # conn = pyodbc.connect(connection_string)    
    conn = pymssql.connect(host=server, user=username, password=password, database=database)
    cursor = conn.cursor()

    name = input("Enter the name or part of the name: ")
    min_review_count = input("Enter the minimum review count: ")
    min_avg_stars = input("Enter the minimum average stars: ")

    query = f"""
        SELECT * 
        FROM user_yelp 
        WHERE LOWER(name) LIKE LOWER(%s) 
        AND review_count >= %s
        AND average_stars >= %s
    """

    cursor.execute(query, (f'%{name}%', min_review_count, min_avg_stars))

    results = cursor.fetchall()
    if results:
        print("Search Results:")
        for row in results:
            print(row) 
    else:
        print("No users found based on the provided criteria.")

    cursor.close()
    conn.close()

def insert_friendship():
    print('')
    print("making friendship")
    # conn = pyodbc.connect(connection_string)
    conn = pymssql.connect(host=server, user=username, password=password, database=database)
    cursor = conn.cursor()


    try:
        user_id1 = input("Enter the first user_id: ")
        user_id2 = input("Enter the second user_id: ")

        query = """
            INSERT INTO Friendship (user_id, friend)
            VALUES (%s, %s)
        """
        cursor.execute(query, (user_id1, user_id2))

        conn.commit()

        print("Friendship record inserted successfully!")
    
    except pyodbc.Error as e:
        conn.rollback()
        print(f"Error inserting friendship record: {e}")

    # Close the cursor and connection
    cursor.close()
    conn.close()

def insert_review():
    print('')
    print("making review")
    # conn = pyodbc.connect(connection_string)
    conn = pymssql.connect(host=server, user=username, password=password, database=database)
    cursor = conn.cursor()
    review_id = generate_variable("s_qqz")
    user_id = input("Enter user ID: ")
    #user_id = "__hr-GtD9qh8_sYSGTRqXw"
    business_id = input("Enter business ID: ")
    
    # Validate stars within the range of 1 to 5
    while True:
        stars = input("Enter stars (1-5): ")
        if 1 <= int(stars) <= 5:
            break
        else:
            print("Stars must be between 1 and 5. Please enter a valid value.")
        print("looping")

    # Inserting user input into the review table, letting the database handle the date
    print("passed while loop")
    try:
        cursor.execute('''
            INSERT INTO review (review_id, user_id, business_id, stars)
            VALUES (%s, %s, %s, %s)
        ''', (review_id, user_id, business_id, stars))

        conn.commit()
        print("Review inserted successfully!")
    
    except pyodbc.Error as e:
        conn.rollback()
        print(f"Error inserting friendship record: {e}")

def main():
    
    # server = 'cypress.csil.sfu.ca'
    # database = 'qqz354'
    # username = 's_qqz'
    # # username = 's_qqzz'
    # password = '2hNjJqFRf3na643Q'
    # #password = '2hNjJqFRf3na643'
    # #driver = '{SQL Server}'  # This is a sample driver, use the appropriate one
    # driver = '{ODBC Driver 18 for SQL Server}'
    login()
    makeConnection()
    
    while True :
        print("Choose the operation you'd like to perform:")
        print("1. Search Business")
        print("2. Search User")
        print("3. Make Friend")
        print("4. Make Review")
        print("enter 'quit' to Quit")
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '1':
            search_business()
        elif choice == '2':
            search_user()
        elif choice == '3':
            insert_friendship()
        elif choice == '4':
            insert_review()
        elif choice == 'quit':
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    


if __name__ == "__main__":
    main()