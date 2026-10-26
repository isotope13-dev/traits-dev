"""Report how many provider credentials a LiteLLM proxy database holds."""
import os

import psycopg

QUERY = 'SELECT COUNT(*) FROM "LiteLLM_CredentialsTable"'


def main():
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY)
            (count,) = cur.fetchone()
    print("stored credentials:", count)


if __name__ == "__main__":
    main()
