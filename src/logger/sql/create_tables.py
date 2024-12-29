import sqlite3

from logger.sql.tables import TABLES, COLUMNS

create_table_statements = []

for table_name in TABLES.keys():
    create_table_statement = '''\n\tCREATE TABLE IF NOT EXISTS'''
    create_table_statement += f"\n\t\t\t{table_name} ("
    for column_name, column_type in TABLES[table_name][COLUMNS].items():
        create_table_statement += f"\n\t\t\t\t{column_name} {column_type},"
    create_table_statement = create_table_statement[:-1]
    create_table_statement += "\n\t\t)"
    create_table_statements.append(create_table_statement)


def create_tables(cursor: sqlite3.Cursor):
    for stmt in create_table_statements:
        cursor.execute(stmt)
