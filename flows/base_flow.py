from pages.featured_promos_page import FeaturedPromosPage


class BaseFlow:
    def __init__(self, driver, reporter=None):
        self.driver = driver
        self.reporter = reporter
        # Shared screens every flow can reach: "Featured promos" is opened from
        # the promo strip on tee time, event and driving-range details alike.
        self.featured_promos = self.page(FeaturedPromosPage)

    def page(self, page_class):
        return page_class(self.driver, self.reporter)

    def use_reporter(self, reporter):
        from core.base_page import BasePage

        self.reporter = reporter
        for value in vars(self).values():
            if isinstance(value, BasePage):
                value.reporter = reporter
        return reporter
