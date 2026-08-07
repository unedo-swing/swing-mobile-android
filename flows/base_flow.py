"""
Base flow.

Holds the shared driver + reporter and a small factory for building page
objects, so concrete flows don't repeat the wiring. A flow composes page steps
into scenarios; page objects come from ``self.page(SomePage)``.
"""


class BaseFlow:
    def __init__(self, driver, reporter=None):
        self.driver = driver
        self.reporter = reporter

    def page(self, page_class):
        return page_class(self.driver, self.reporter)
