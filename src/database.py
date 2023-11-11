import sqlite3


class Database:
    def __init__(self) -> None:
        self.db = sqlite3.connect("session.sqlite")
        self.cur = self.db.cursor()

        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS leaderboard(Id INTEGER PRIMARY KEY AUTOINCREMENT, Winner TEXT);"
        )

    def get_field(self) -> str | None:
        table = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
  AND name='session'; """
        ).fetchall()

        if table:
            return self.cur.execute(
                """SELECT Field FROM session ORDER BY Id DESC LIMIT 1"""
            ).fetchone()[0]

        self.cur.execute(
            "CREATE TABLE session(Id INTEGER PRIMARY KEY AUTOINCREMENT, Field TEXT, Turn TEXT);"
        )

        return None

    def get_session(self) -> tuple[str, ...] | None:
        table = self.cur.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
  AND name='session'; """
        ).fetchall()

        if table:
            session = self.cur.execute(
                """SELECT Field, Turn FROM session ORDER BY Id DESC LIMIT 1"""
            ).fetchone()
            return session

        self.create_session()

        return None

    def create_session(self) -> None:
        self.cur.execute(
            "CREATE TABLE session(Id INTEGER PRIMARY KEY AUTOINCREMENT, Field TEXT, Turn TEXT);"
        )

    def add_move(
        self,
        field: str,
        turn: str,
    ) -> None:
        self.cur.execute(
            f"INSERT INTO session(Field, Turn) VALUES('{field}', '{turn}');"
        )
        # self.db.commit()

    def close(self) -> None:
        self.db.commit()
        self.db.close()

    def clear_session(self) -> None:
        self.cur.execute("""DROP TABLE session""")
        # self.db.commit()

    def write_leaderboard(self, winner) -> None:
        self.cur.execute(f"INSERT INTO leaderboard(Winner) VALUES('{winner}')")
