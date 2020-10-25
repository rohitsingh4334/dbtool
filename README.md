## Databuild tool 

<p>
A command line interface 'dbtool' using python and sqlite to do basic database operations.
</p>

* Available Subcommands :
    * create-database
    * create-table
    * insert-into
    * drop-table
    * update
    * truncate-table

```shell script
usage: dbtool [-h] [--db-name DB_NAME] [--query QUERY] [--data DATA] [--table-name TABLE_NAME]
               {create-database,create-table,insert-into,drop-table,update,truncate-table}
dbtool available commands:
      positional arguments: {create-database,create-table,insert-into,drop-table,update,truncate-table}.

optional arguments:
  -h, --help                  show this help message and exit
  --db-name DB_NAME           meant for database name. ex: 'a.db'
  --query QUERY               meant for sqlite query. ex: 'select column from table '
  --data DATA                 data in the form of json string. ex: '{column: value}'
  --table-name TABLE_NAME     sqlite table name.
```# src
