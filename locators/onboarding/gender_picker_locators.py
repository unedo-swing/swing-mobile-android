class GenderPickerLocators:
    scrim = '//android.view.View[@content-desc="Scrim"]'

    # ================= options =================
    option_not_specified = '//android.view.View[@content-desc="Not specified"]'
    option_male = '//android.view.View[@content-desc="Male"]'
    option_female = '//android.view.View[@content-desc="Female"]'
    # any option by label, e.g. option_by_label % "Male"
    option_by_label = '//android.view.View[@content-desc="%s"]'

    # ================= confirm =================
    # the sheet's only button; it carries no content-desc, so it can't be
    # anchored on its label
    button_confirm = '//android.widget.Button'
