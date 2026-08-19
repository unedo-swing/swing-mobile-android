class NationalityPickerLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Select nationality"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    scrim = '//android.view.View[@content-desc="Scrim"]'

    # ================= search =================
    _search_box = '//android.view.View[@content-desc="Search country"]'
    input_search = _search_box + '//android.widget.EditText'

    # ================= list =================
    # the scrollable country list
    list_countries = '//android.view.View[@scrollable="true"]'
    # a row by its country name, e.g. option_exact % "Indonesia"
    option_exact = '//android.view.View[@content-desc="%s"]'
    option_contains = '//android.view.View[contains(@content-desc,"%s")]'
