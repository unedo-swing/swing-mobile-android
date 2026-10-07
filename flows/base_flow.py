from core.android_base_page import AndroidBasePage
from pages.featured_promos_page import FeaturedPromosPage
from utils import step_guard


class BaseFlow:
    _UNGUARDED = ("page", "use_reporter", "capture_step")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, attr in list(vars(cls).items()):
            if name.startswith("_") or name in cls._UNGUARDED:
                continue
            if isinstance(attr, staticmethod) or isinstance(attr, classmethod):
                continue
            if callable(attr):
                setattr(cls, name, step_guard.guard(attr))

    def __init__(self, driver, reporter=None):
        self.driver = driver
        self.reporter = reporter
        # Shared screens every flow can reach: "Featured promos" is opened from
        # the promo strip on tee time, event and driving-range details alike.
        self.featured_promos = self.page(FeaturedPromosPage)
        # Not a screen: the page the guard screenshots through when a step
        # fails. use_reporter() wires it like any other page.
        self._evidence_page = self.page(AndroidBasePage)

    def page(self, page_class):
        return page_class(self.driver, self.reporter)

    def capture_step(self, title: str, description: str = "", status: str = ""):
        return self._evidence_page.capture_step(title, description, status=status)

    # --- Xendit test-mode payments: the pending order is read from the DB ---
    SIMULATED_PAYMENT_TYPES = ("qris", "virtual account")

    def simulate_qris_payment(self, payment_method="QRIS"):
        return self.simulate_gateway_payment(payment_method, "QRIS")

    def simulate_va_payment(self, payment_method):
        return self.simulate_gateway_payment(payment_method, "Virtual account")

    def simulate_gateway_payment(self, payment_method, payment_type):
        kind = str(payment_type or "").strip().lower()
        if kind not in self.SIMULATED_PAYMENT_TYPES:
            return None
        from utils.api_client import ApiClient
        from utils.db_queries import pending_booking_payment

        payment = pending_booking_payment(payment_method)
        client = ApiClient.swing()
        if kind == "qris":
            response = client.simulate_qr_payment(payment["id"])
        else:
            response = client.simulate_va_payment(payment["id"], payment["value"])
        print(f"[xendit] simulated {payment['payment_method']} payment order {payment['id']} "
              f"amount {payment['value']}: HTTP {response.status} {response.text[:300]}")
        self.step(f"Simulate {payment['payment_method']} payment, order {payment['id']}",
                  f"HTTP {response.status} {response.text[:300]}",
                  status="" if response.ok else "FAIL")
        response.raise_for_status()
        return payment["id"]

    def step(self, title, description="", status=""):
        if self.reporter:
            self.reporter.add_step(title, description, status=status)
        return self

    def use_reporter(self, reporter):
        from core.base_page import BasePage

        self.reporter = reporter
        for value in vars(self).values():
            if isinstance(value, BasePage):
                value.reporter = reporter
        return reporter
