import os
import psycopg2

def register_training():
    training_id = os.getenv('training_id')
    conn = psycopg2.connect(
        user="postgresadmin",
        database="postgresdb",
        password="admin123",
        host="167.205.35.252",
        port="30513"
    )
    print('\n\n REGISTERING TRAINING {} \n\n'.format(training_id))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO running_training(training_id) VALUES ('{}')".format(training_id))
    conn.commit()
    cursor.close()
    conn.close()