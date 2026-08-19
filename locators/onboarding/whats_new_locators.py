class WhatsNewLocators:
    # ================= header =================
    label_title = '//android.view.View[contains(@content-desc,"new with Swing")]'
    button_close = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= body =================
    content = '//android.widget.ScrollView'
    label_headline = '//android.view.View[contains(@content-desc,"major updates with Swing version")]'
    label_subtitle = '//android.view.View[contains(@content-desc,"minor updates")]'
    link_see_updates = '//android.view.View[@content-desc="See our updates"]'
