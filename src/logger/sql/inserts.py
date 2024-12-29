import sqlite3

from logger.sql.tables import TABLES, COLUMNS


def insert(con: sqlite3.Connection, table_name, values):

    columns_to_use = []
    value_keys = set([key for value in values for key in value.keys()])
    for column_name in TABLES[table_name][COLUMNS].keys():
        if column_name in value_keys:
            columns_to_use.append(column_name)

    insert_statement = f'''
        INSERT INTO
            {table_name}
            ('''
    for column in columns_to_use:
        insert_statement += column + ", "

    insert_statement = insert_statement[:-2] + ''')
        VALUES
            ('''
    for column in columns_to_use:
        insert_statement += ":" + column + ", "

    insert_statement = insert_statement[:-2] + ")"
    con.executemany(insert_statement, values)
    con.commit()

