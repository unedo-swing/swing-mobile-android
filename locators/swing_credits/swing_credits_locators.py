class SwingCreditsLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Swing Credits"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    # the country/region toggle in the top-right, e.g. "ID"
    button_region = '//android.widget.ImageView[@content-desc="ID"]'
    button_region_by_code = '//android.widget.ImageView[@content-desc="%s"]'

    # ================= balance =================
    # The balance is the first View in the scroll view — it carries only the
    # number ("0", "25,000"), with no label of its own to anchor on.
    value_balance = '(//android.widget.ScrollView/android.view.View)[1]'
    # shown while the account has never earned any credits
    label_earn_hint = '//android.widget.ImageView[contains(@content-desc,"Make your first booking")]'

    # ================= actions =================
    # opens the Redeem Swing Credits code sheet (RedeemSwingCreditsPage).
    # An ImageView here, unlike the sheet's Button of the same name.
    button_redeem_credits = '//android.widget.ImageView[@content-desc="Redeem Swing Credits"]'
    # content-desc is "Always use Swing Credits\nCredits will always be used during payments"
    switch_always_use = '//android.widget.Switch[contains(@content-desc,"Always use Swing Credits")]'
    button_see_all_cashbacks = '//android.widget.ImageView[@content-desc="See all cashbacks"]'
    button_learn_more = '//android.widget.ImageView[@content-desc="Learn more"]'
    button_see_history = '//android.widget.ImageView[@content-desc="See history"]'

    # ================= redeem your Swing Credits =================
    label_redeem_section = '//android.view.View[@content-desc="Redeem your Swing Credits"]'
    # a reward card; content-desc is "<Reward>\n<Merchant>\n<N> Swing Credits"
    #   reward_card_by_name % "Chocolate Frappe Point"
    reward_card_by_name = '//android.view.View[contains(@content-desc,"%s")]'
    # every reward card (each one prices itself in Swing Credits)
    reward_card_any = '//android.view.View[contains(@content-desc,"Swing Credits") and @clickable="true"]'
