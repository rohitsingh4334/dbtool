import argparse
from src.db import DatabaseOperation
from src.table import TableOps

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "option",
        type=str,
        choices=[
            "create-database", "create-table", "insert-into","drop-table", "update", "truncate-table"
        ],
        help="src available commands."
    )
    parser.add_argument("--db-name", type=str, help="meant for database name. ex: 'a.db' ")
    parser.add_argument("--query", type=str, help="meant for sqlite query. ex: 'select column from table '")
    parser.add_argument("--data", type=str, help="data in the form of json string. ex: '{column: value}'")
    parser.add_argument("--table-name", type=str, help="sqlite table name.")
    args = parser.parse_args()

    db_ops, tbl_ops = None, None
    if args.db_name:
        db_ops = DatabaseOperation(args.db_name)
        tbl_ops = TableOps(args.db_name)

    if args.option == "create-database":
        if db_ops:
            db_ops.create()
        else:
            print("more operations will be add in future version.")
    elif args.option == "create-table":
        if len(args.query) > 1 and tbl_ops:
            tbl_ops.create(args.query)
        else:
            print("Syntax Error: please provide syntax like create-table --db-name [db] --query '[create table query]' ")
    elif args.option == "drop-table":
        if args.table_name and tbl_ops:
            tbl_ops.drop(args.table_name)
        else:
            print("Syntax Error: please provide syntax like drop-table --db-name [db] --table-name [table] ")
    elif args.option == "insert-into":
        if args.table_name and len(args.data) > 1 and tbl_ops:
            tbl_ops.insert(args.table_name, args.data)
        else:
            print('Syntax Error: please provide syntax like insert-into --db-name [db] --table-name [table] --data {"id":1, "name":"John"}')
    elif args.option == "update":
        if args.db_name and len(args.query) > 1 and tbl_ops:
            tbl_ops.update(args.query)
        else:
            print('Syntax Error: please provide syntax like update --db-name [db] --query "[update_query]" ')
    elif args.option == "truncate-table":
        if args.db_name and tbl_ops:
            tbl_ops.truncate(args.table_name)
        else:
            print('Syntax Error: please provide syntax like update --db-name [db] --table-name [table] ')
    else:
        print("Limited options are available in the current version.")

if __name__ == '__main__':
    main()