import sqlite3
from bs4 import BeautifulSoup

# Step 1: Create a database connection
conn = sqlite3.connect('my_database.db')

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Create a table to store the HTML data
cursor.execute('''CREATE TABLE my_table (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    body TEXT
                )''')

# Step 4: Parse the HTML file
with open('my_html_file.html') as fp:
    soup = BeautifulSoup(fp, 'html.parser')

    # Step 5: Extract data from the HTML file and insert it into the database
    for idx, article in enumerate(soup.find_all('article')):
        title = article.find('h1').text.strip()
        body = article.find('div', {'class': 'article-body'}).text.strip()

        cursor.execute("INSERT INTO my_table (id, title, body) VALUES (?, ?, ?)", (idx+1, title, body))

# Step 6: Commit the changes
conn.commit()

# Step 7: Close the cursor and database connection
cursor.close()
conn.close()
