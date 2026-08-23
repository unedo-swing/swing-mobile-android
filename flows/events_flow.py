from flows.base_flow import BaseFlow
from pages.home_page import HomePage
from pages.events.events_list_page import EventsListPage
from pages.events.event_details_page import EventDetailsPage
from pages.events.bottomsheet_detail_event_regis_page import (
    BottomsheetDetailEventRegisPage,
)
from pages.events.registration_confirmation_page import RegistrationConfirmationPage
from pages.events.bottomsheet_add_player_page import BottomsheetAddPlayerPage
from pages.events.payment_method_page import PaymentMethodPage
from pages.events.order_page import OrderPage


class EventsFlow(BaseFlow):
    def __init__(self, driver, reporter=None):
        super().__init__(driver, reporter)
        self.home = self.page(HomePage)
        self.list = self.page(EventsListPage)
        self.details = self.page(EventDetailsPage)
        self.reg_sheet = self.page(BottomsheetDetailEventRegisPage)
        self.confirm = self.page(RegistrationConfirmationPage)
        self.add_player = self.page(BottomsheetAddPlayerPage)
        self.payment = self.page(PaymentMethodPage)
        self.order = self.page(OrderPage)

    def open_events(self):
        self.home.open_events()
        self.list.verify_screen()

    def select_event(self, name: str):
        self.list.verify_event_card(name)
        self.list.open_event(name)
        self.details.verify_screen()
        self.details.verify_event_title(name)

    def verify_registration_state(self, status: str):
        if status == "Closed":
            self.details.verify_registration_closed_footer()
        else:
            self.details.verify_registration_open()

    def choose_registration(self, reg_type: str):
        self.details.tap_booking_button()
        self.reg_sheet.verify_screen()
        self.reg_sheet.choose_registration_type(reg_type)
        self.confirm.verify_screen()

    def add_player_by_name(self, name: str):
        self.confirm.tap_add_player()
        self.add_player.verify_screen()
        self.add_player.search_friend(name)
        self.add_player.select_player(name)
        self.add_player.verify_player_added(name)
        self.confirm.verify_screen()

    def select_payment(self, method: str):
        self.confirm.tap_select_payment()
        self.payment.verify_screen()
        self.payment.select_payment_method(method)
        self.confirm.verify_screen()
        self.confirm.verify_payment_selected(method)

    def pay_now(self):
        self.confirm.tap_pay_now()
        self.order.verify_success()

    def finish(self):
        self.order.tap_finish()
