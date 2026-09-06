from pages.multisport.sport_option_page import SportOptionPage
from pages.multisport.billiard_page import BilliardPage
from pages.multisport.all_venue_list_page import AllVenueListPage
from pages.multisport.venue_detail_page import VenueDetailPage
from pages.multisport.select_schedule_page import SelectSchedulePage
from pages.multisport.booking_confirmation_page import BookingConfirmationPage
from pages.multisport.payment_method_page import PaymentMethodPage
from pages.multisport.bottomsheet_add_player_page import BottomsheetAddPlayerPage
from pages.multisport.order_page import OrderPage


class MultisportFlow:

    def __init__(self, driver, reporter=None):
        self.driver = driver
        self.reporter = reporter
        self.sport_option = SportOptionPage(driver, reporter)
        self.billiard_page = BilliardPage(driver, reporter)
        self.all_venue_list = AllVenueListPage(driver, reporter)
        self.venue_detail = VenueDetailPage(driver, reporter)
        self.select_schedule = SelectSchedulePage(driver, reporter)
        self.booking_confirmation = BookingConfirmationPage(driver, reporter)
        self.payment_method = PaymentMethodPage(driver, reporter)
        self.add_player = BottomsheetAddPlayerPage(driver, reporter)
        self.order = OrderPage(driver, reporter)

    # -------- initiation from Home --------
    def open_multisport_sport(self):
        """From the app bar on Home, enter the sport option page."""
        self.sport_option.navigate_from_home()
        self.sport_option.verify_screen()

    def select_sport(self, sport_name: str):
        self.sport_option.choose_sport(sport_name)
        self.billiard_page.verify_screen()

    def view_all_venue(self):
        self.billiard_page.go_to_all_venue()
        self.all_venue_list.verify_screen()

    def select_venue(self, venue_name: str):
        self.all_venue_list.choose_venue(venue_name)
        self.venue_detail.verify_screen(venue_name)

    def book_venue(self):
        self.venue_detail.book_venue()
        self.select_schedule.verify_screen()

    def select_schedule_flow(self, schedule_title: str, how_many: int):
        self.select_schedule.navigate_to_next_day_until_gone()
        self.select_schedule.select_schedule(schedule_title, how_many)

    def confirm_schedule(self):
        self.select_schedule.confirm_schedules()

    def payment_method_flow(self, method_name: str):
        self.booking_confirmation.open_payment_method()
        self.payment_method.verify_screen()
        self.payment_method.select_payment_method(method_name)

    def add_player_by_name(self, name: str):
        self.booking_confirmation.click_add_player()
        self.add_player.verify_screen()
        self.add_player.search_friend(name)
        self.add_player.select_player(name)
        self.add_player.verify_player_added(name)
        self.booking_confirmation.verify_screen()
        self.booking_confirmation.verify_total_player()

    def remove_player(self):
        self.booking_confirmation.delete_player()

    def pay_now(self):
        self.booking_confirmation.tap_pay_now()

    def finish(self):
        self.order.tap_finish()
