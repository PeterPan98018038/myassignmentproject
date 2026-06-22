import psycopg2

# Connect Configuration
DB_CONFIG = {
    "host": "localhost",
    "database": "assignment_db",
    "user": "postgres",
    "password": "1234",
    "port": "5432"
}

def get_connection():
    """Establish and return a connection to PostgreSQL database"""
    return psycopg2.connect(**DB_CONFIG)

def setup_database():
    """Create a fresh table for demo"""
    conn = get_connection()
    cursor = conn.cursor()

    # Drop table if exists to start fresh, then create it
    cursor.execute("DROP TABLE IF EXISTS student_scores;")
    cursor.execute("""
        CREATE TABLE student_scores (
            id SERIAL PRIMARY KEY,
            student_name VARCHAR(50),
            score INT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("\nOK, Database initialized: 'student_scores' table is ready.")


# Send the below test data to postgreSQL

def insert_test_data():
    test_data = [
        ("Alice Chan", 50),
        ("Johny Pan", 84),
        ("Mary Cheung", 84),
        ("Carie Lee", 63),
        ("Paul Ho", 34),
        ("Bob Mok", 92),
        ("Peter Chan", 58),
        ("Mary Poon", 79),
        ("Lily Chiang", 82),
        ("Peter Mok", 69),
        ("Yuki Pan", 67),
        ("Miki Li", 97),
        ("Charlie Lee", 68),
        ("John Mok", 69),
        ("Ambrose Leung", 99)
    ]

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO student_scores (student_name, score) VALUES (%s, %s);"
    cursor.executemany(query, test_data)

    conn.commit()
    cursor.close()
    conn.close()
    print("\nCongratulations! Test data successfully sent to postgresSQL database.")
          

# Fetch and display data from database

def fetch_data_from_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, student_name, score FROM student_scores ORDER BY id;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    print("\nCurrent Data pulled from postgreSQL into Python:")
    print("-" * 40)
    print(f"{'ID':<5} | {'Student Name':<15} | {'Score':<5}")
    print("-" * 40)
    for row in rows:
        print(f"{row[0]:<5} | {row[1]:<15} | {row[2]:<5}")
    print("-" * 40)


if __name__ == "__main__":
    try:
        setup_database()

        insert_test_data()

        fetch_data_from_db()

        print("\nPAUSE FOR PRESENTATION")
        print("1. Go to pgAdmin and change some student's score (e.g., 100)")

        print("2. Remember to click 'Save/Commit' at database in pgAdmin.")

        input("After changing the data in pgAdmin, press ENTER here to pull the revised data transfered back")

        print("\n Fetching updated data from pgAdmin...")
        fetch_data_from_db()

    except Exception as e:
        print(f"An error occurred: {e}")

