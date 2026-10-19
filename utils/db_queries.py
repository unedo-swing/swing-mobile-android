import os

from utils.db_client import DbClient, DbError, Row


def _db(db=None):
    return db or DbClient.from_env()


def _named_db(db, env_key, default_name):
    if db:
        return db
    client = DbClient.from_env()
    client.name = (os.getenv(env_key) or "").strip() or default_name
    client.label = client.name
    return client


def _sport_db(db=None):
    return _named_db(db, "SPORT_DB_NAME", "dev-swing-sport-db")


def _payment_db(db=None):
    return _named_db(db, "PAYMENT_DB_NAME", "dev-swing-payment-db")


def _booking_code(booking_code):
    return str(booking_code or "").split("#")[-1].strip()


def pending_booking_payment(payment_method, timeout=30, db=None) -> Row:
    rows = _db(db).wait_for("""
        select bp.id, bp.value, pm.name as payment_method, bp.created_at
        from booking_payments bp
        join payment_methods pm on pm.id = bp.payment_method_id
        where lower(pm.name) = lower(%s) and bp.status = 'PENDING'
        order by bp.created_at desc
        limit 1
    """, [payment_method], timeout=float(timeout))
    return rows[0]


def latest_booking_payment_id(payment_method, db=None):
    return _db(db).query_value("""
        select bp.id
        from booking_payments bp
        join payment_methods pm on pm.id = bp.payment_method_id
        where pm.name = %s
        order by bp.created_at desc
        limit 1
    """, [payment_method])


def order_id_by_booking_code(booking_code, timeout=30, db=None):
    code = _booking_code(booking_code)
    if not code:
        raise DbError(f"No booking code to look up in orders, got {booking_code!r}")
    rows = _sport_db(db).wait_for("""
        select o.id
        from orders o
        where o.booking_code = %s
        order by o.created_at desc
        limit 1
    """, [code], timeout=float(timeout))
    return rows[0]["id"]


def payments_by_order_id(order_id, timeout=30, db=None) -> list[Row]:
    return _payment_db(db).wait_for("""
        select p.id, p.order_id, p.provider_account_id, p.status, p.created_at
        from payments p
        where p.order_id = %s
        order by p.created_at desc
    """, [str(order_id)], timeout=float(timeout))


def payment_provider_account(booking_code, timeout=30, sport_db=None, payment_db=None) -> Row:
    order_id = order_id_by_booking_code(booking_code, timeout, sport_db)
    payment = payments_by_order_id(order_id, timeout, payment_db)[0]
    return {**payment, "booking_code": _booking_code(booking_code),
            "provider_account_id_is_null": payment["provider_account_id"] is None}


def verify_provider_account_id(booking_code, expect_null=False, timeout=30,
                               sport_db=None, payment_db=None) -> Row:
    payment = payment_provider_account(booking_code, timeout, sport_db, payment_db)
    state = "null" if payment["provider_account_id_is_null"] else "not null"
    expected = "null" if expect_null else "not null"
    assert payment["provider_account_id_is_null"] == expect_null, (
        f"payments.provider_account_id for booking #{payment['booking_code']} "
        f"(order {payment['order_id']}, payment {payment['id']}) is {state}, expected {expected}: "
        f"{payment['provider_account_id']!r}")
    return payment


def run_sql(sql, params=None, db=None):
    return _db(db).query(sql, params)
