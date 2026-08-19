class BirthdayPickerLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Select birthday"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    scrim = '//android.view.View[@content-desc="Scrim"]'

    # ================= wheels =================
    # document order is month, day, year (left to right)
    WHEEL_MONTH = 1
    WHEEL_DAY = 2
    WHEEL_YEAR = 3

    wheel = '(//android.widget.ScrollView)[%d]'
    wheel_month = wheel % WHEEL_MONTH
    wheel_day = wheel % WHEEL_DAY
    wheel_year = wheel % WHEEL_YEAR

    # an entry inside a given wheel, e.g. option_in_wheel % (WHEEL_MONTH, "September")
    option_in_wheel = '(//android.widget.ScrollView)[%d]//android.view.View[@content-desc="%s"]'
    # every entry currently rendered in a wheel, e.g. options_in_wheel % WHEEL_YEAR
    options_in_wheel = '(//android.widget.ScrollView)[%d]//android.view.View[@content-desc]'

    # ================= confirm =================
    button_confirm = '//android.widget.Button[@content-desc="Confirm"]'
