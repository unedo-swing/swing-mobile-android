from utils.db_client import DbClient, Row


def _db(db=None):
    return db or DbClient.from_env()


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


def run_sql(sql, params=None, db=None):
    return _db(db).query(sql, params)
