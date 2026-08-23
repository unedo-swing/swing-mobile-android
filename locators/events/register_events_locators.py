class RegisterEventsLocators:
    # -- Header tittle (scrolled / unscrolled)
    title_page = "//*[contains(@content-desc, 'Register')]"

    # --- Button header page Register Events (unscrolled)
    button_back = "//*[contains(@content-desc, 'Register')]/ancestor::*/preceding-sibling::*"

    # --- Button sticky header page Register Events (scrolled)
    button_back_scrolled = "//*[contains(@content-desc, 'Register')]/preceding-sibling::*"
    button_self_host = "//*[contains(@content-desc, 'Register')]/following-sibling::android.widget.ImageView"

    # --- Show Filter
    title_filter = "//*[@content-desc='Only show Swing Pass partners']"
    switch_button_option = "//*[@content-desc='Only show Swing Pass partners']//child::android.widget.Switch"

    # --- Event option cards
    card_event = "//android.widget.ScrollView//android.view.View[contains(@content-desc, '%s')]"

    # --- Footer
    label_footer = "//android.widget.ScrollView//android.view.View[@content-desc='Planning to host a tournament really soon? Connect with us and let Swing help you!']"
    button_footer_self_host = "//*[@content-desc='Host your tournament']"

