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

    def use_reporter(self, reporter):
        from core.base_page import BasePage

        self.reporter = reporter
        for value in vars(self).values():
            if isinstance(value, BasePage):
                value.reporter = reporter
        return reporter
