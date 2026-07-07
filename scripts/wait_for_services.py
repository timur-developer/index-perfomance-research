import time

from db_connections import postgres_conn, mysql_conn, mongo_client


def wait_for(name: str, fn, timeout_seconds: int = 180) -> None:
    start = time.time()
    last_error = None
    while time.time() - start < timeout_seconds:
        try:
            resource = fn()
            try:
                if name == "MongoDB":
                    resource.admin.command("ping")
                else:
                    resource.close()
            finally:
                if name == "MongoDB":
                    resource.close()
            print(f"{name} is ready.")
            return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(3)
    raise RuntimeError(f"{name} is not ready after {timeout_seconds}s. Last error: {last_error}")


def main() -> None:
    wait_for("PostgreSQL", postgres_conn)
    wait_for("MySQL", mysql_conn)
    wait_for("MongoDB", mongo_client)


if __name__ == "__main__":
    main()
