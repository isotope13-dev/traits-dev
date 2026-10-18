parser grammar SqlContextParser;

execute_clause
    : EXECUTE AS (SELF | user_name = STRING | OWNER)
    ;

lowercase_clause
    : execute as (self | owner)
    ;
