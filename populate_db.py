import csv
import sqlite3
import os

con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'glucose_levels.db'))


def load_files():
    """
    Loading sample data in memory ready to be inserted into rows in the database.
    :return: Dictionary containing all 3 sample data provided in the format of a dictionary.
    """
    sample_data_dict = {'bruce_wayne.csv': [],'user_a.csv': [], 'user_b.csv': [], 'user_c.csv': []}
    for filename in ['bruce_wayne.csv', 'user_a.csv', 'user_b.csv', 'user_c.csv', ]:

        with open(os.path.join(os.path.dirname(__file__), 'sample-data', filename)) as sample_data:

            for line in csv.DictReader(sample_data):
                sample_data_dict[filename].append(dict(line))

    return sample_data_dict


def insert_into_db(glucose_data_sets):
    """
    :param glucose_data_sets:
    :return:
    """
    cur = con.cursor()
    cur.execute("DROP TABLE levels")
    # Seems like we don't actually need all the data so only creating the fields we need for the API
    cur.execute('''CREATE TABLE levels
                   (recording_id integer NOT NULL,
                    user_id text NOT NULL,
                    timestamp text NOT NULL,
                    recording integer NOT NULL,
                    serial_number text NOT NULL,
                    device text NOT NULL,
                    recording_type text NOT NULL)''')

    # There's a better way to do this 100% but in the interest of time...
    row_id = 1

    for dataset_name, data in glucose_data_sets.items():
        for row in data:
            #  We don't want the file type in the DB.
            user_id = dataset_name.replace('.csv', '')
            # Insert a row of data, converting from german to english
            sql = "INSERT INTO levels VALUES (?,?,?,?,?,?, ?)"
            cur.execute(sql, [row_id,
                              user_id,
                              row['Gerätezeitstempel'],
                              row['Glukosewert-Verlauf mg/dL'],
                              row['Seriennummer'],
                              row['Gerät'],
                              row['Aufzeichnungstyp']])
            # Save (commit) the changes
            con.commit()
            row_id = row_id+1


if __name__ == '__main__':
    sample_data = load_files()
    insert_into_db(sample_data)
