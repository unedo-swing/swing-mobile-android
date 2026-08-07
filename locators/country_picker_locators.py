class CountryPickerLocators:
    label_title = '//android.view.View[@content-desc="Select country code"]'
    _search_box = '//android.view.View[@content-desc="Search country code"]'
    input_search = _search_box + '//android.widget.EditText'
    button_back = '//android.widget.ImageView[@clickable="true"]'
    option_exact = '//android.view.View[@content-desc="%s"]'
    option_contains = '//android.view.View[contains(@content-desc,"%s")]'
