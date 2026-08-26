class EventDetailsLocators:
    # --- Header
    title_header = "//*[@content-desc='Event details']"
    button_back = "//*[@content-desc='Event details']/preceding-sibling::*"
    button_share = "//*[@content-desc='Event details']/following-sibling::*"

    # --- description
    title_event = "//android.widget.ScrollView/*[contains(@content-desc, '%s')]"

    # --- footer
    button_booking = "//android.widget.Button[@content-desc='Secure your slot']"
    button_reminder = "//android.widget.Button[@content-desc='Notify me for the next event']"
    label_successfully_reminder = "//android.view.View[contains(@content-desc,'notify you if')]"
    icon_successfully_reminder = "//android.view.View[contains(@content-desc,'notify you if')]/preceding-sibling::android.widget.ImageView[last()]"
