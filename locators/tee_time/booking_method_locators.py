"""
Android XPaths for the Swing Tee Time > Booking method bottom sheet.

Opened after tapping "Book tee time" on the golf course details screen. Lets the
user choose Group vs Standard booking, with a "Learn more" info dialog. Flutter
app — elements surface through ``content-desc``. ``contains`` is used for the
multi-line option cards.
"""


class BookingMethodLocators:
    # --- chooser sheet ---
    label_title = '//android.view.View[@content-desc="How would you like to make this tee time booking?"]'
    option_group_booking = '//android.view.View[contains(@content-desc,"Group booking")]'
    option_standard_booking = '//android.view.View[contains(@content-desc,"Standard booking")]'
    link_learn_more = '//android.widget.ImageView[@content-desc="Learn more about booking methods"]'
    # bottom action button (no content-desc); it's the last Button in the sheet.
    button_continue = '(//android.widget.Button)[last()]'
    scrim = '//android.view.View[@content-desc="Scrim"]'

    # --- "Booking method info" dialog (from Learn more) ---
    label_info_title = '//android.view.View[@content-desc="Booking method info"]'
    info_section_group = '//android.widget.ImageView[@content-desc="Group booking"]'
    info_section_standard = '//android.widget.ImageView[@content-desc="Standard booking"]'
    button_got_it = '//android.widget.Button[@content-desc="Got it!"]'
