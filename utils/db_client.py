import getpass
import os
import time
from contextlib import contextmanager
from typing import Any, Callable, cast

Row = dict[str, Any]


class DbError(RuntimeError):
    pass


def _env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value.strip()


def _clip(value, limit=200):
    text = " ".join(str(value).split())
    return text if len(text) <= limit else f"{text[:limit]}..."


class DbClient:

    def __init__(self, host="", port=5432, name="", user="", password="",
                 sslmode="prefer", connect_timeout=10, statement_timeout=30,
                 allow_write=False, retries=2, retry_delay=3, label="db"):
        self.host = host
        self.port = int(port)
        self.name = name
        self.user = user
        self.password = password
        self.sslmode = sslmode
        self.connect_timeout = int(connect_timeout)
        self.statement_timeout = float(statement_timeout)
        self.allow_write = allow_write
        self.retries = max(1, int(retries))
        self.retry_delay = float(retry_delay)
        self.label = label

    @classmethod
    def from_env(cls, prefix="DB"):
        if not cls.configured(prefix):
            raise DbError(f"{prefix}_HOST is not set, the database is not configured")
        return cls(
            host=_env(f"{prefix}_HOST", ""),
            port=_env(f"{prefix}_PORT", 5432), # type: ignore
            name=_env(f"{prefix}_NAME", ""),
            user=_env(f"{prefix}_USER", ""),
            password=_env(f"{prefix}_PASSWORD", ""),
            sslmode=_env(f"{prefix}_SSLMODE", "prefer"),
            connect_timeout=_env(f"{prefix}_CONNECT_TIMEOUT", 10), # type: ignore
            statement_timeout=_env(f"{prefix}_STATEMENT_TIMEOUT", 30), # type: ignore
            allow_write=_env(f"{prefix}_ALLOW_WRITE", "false").lower() in ("1", "true", "yes", "on"),
            retries=_env(f"{prefix}_RETRIES", 2), # type: ignore
            retry_delay=_env(f"{prefix}_RETRY_DELAY", 3), # type: ignore
            label=prefix.lower(),
        )

    @staticmethod
    def configured(prefix="DB"):
        return bool(_env(f"{prefix}_HOST"))

    def _connect(self):
        import psycopg
        from psycopg.conninfo import make_conninfo
        from psycopg.rows import dict_row

        params = {
            "host": self.host,
            "port": self.port,
            "dbname": self.name or None,
            "user": self.user or None,
            "password": self.password or None,
            "sslmode": self.sslmode or None,
            "connect_timeout": self.connect_timeout,
            "application_name": "swing-android-tests",
        }
        if self.statement_timeout:
            params["options"] = f"-c statement_timeout={int(self.statement_timeout * 1000)}"
        params = {key: value for key, value in params.items() if value is not None}
        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                connect: Any = psycopg.connect
                connection = connect(make_conninfo(**params), row_factory=dict_row)
                connection.read_only = not self.allow_write
                return connection
            except psycopg.OperationalError as exc:
                last_error = exc
                print(f"[{self.label}] connect attempt {attempt}/{self.retries} failed: {_clip(exc)}")
                if attempt < self.retries:
                    time.sleep(self.retry_delay)
        raise DbError(f"could not connect to {self.label} at {self.host}:{self.port} as user "
                      f"{self.user or getpass.getuser()!r}, database {self.name or self.user or getpass.getuser()!r}: "
                      f"{last_error}") from last_error

    @contextmanager
    def connection(self):
        connection = self._connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _run(self, sql, params=None, fetch=True) -> Any:
        started = time.time()
        with self.connection() as connection, connection.cursor() as cursor:
            try:
                cursor.execute(sql, params)
            except Exception as exc:
                raise DbError(f"{self.label} query failed: {_clip(exc)} | sql: {_clip(sql)}") from exc
            result = cursor.fetchall() if fetch and cursor.description else cursor.rowcount
        count = len(result) if isinstance(result, list) else result
        print(f"[{self.label}] {count} row(s) in {time.time() - started:.2f}s | {_clip(sql)} | {params!r}")
        return result

    def query(self, sql, params=None) -> list[Row]:
        return cast(list[Row], self._run(sql, params))

    def query_one(self, sql, params=None) -> Row | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def query_value(self, sql, params=None, default=None) -> Any:
        row = self.query_one(sql, params)
        return next(iter(row.values())) if row else default

    def execute(self, sql, params=None) -> int:
        if not self.allow_write:
            raise DbError(f"{self.label} is read-only, set {self.label.upper()}_ALLOW_WRITE=true to change data")
        return cast(int, self._run(sql, params, fetch=False))

    def wait_for(self, sql, params=None, until: Callable[[list[Row]], Any] = bool,
                 timeout: float = 30, interval: float = 2) -> list[Row]:
        deadline = time.time() + timeout
        while True:
            rows = self.query(sql, params)
            if until(rows):
                return rows
            if time.time() >= deadline:
                raise DbError(f"{self.label} condition not met after {timeout}s, last result {_clip(rows)}"
                              f" | sql: {_clip(sql)}")
            time.sleep(interval)

    def ping(self) -> bool:
        return self.query_value("select 1") == 1
