from connector import DBConnect


connection = DBConnect()


def clear_table(table_name: str) -> None:
    """Clear the table of all data."""

    # Clear the table
    sql = f"""
    DELETE FROM public."{table_name}";
    """.format(table_name)

    connection.execute_query(sql)