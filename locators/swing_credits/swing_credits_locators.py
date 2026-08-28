class SwingCreditsLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Swing Credits"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    button_region = '//android.view.View[@content-desc="Swing Credits"]/following-sibling::android.widget.ImageView'

    value_balance = '(//android.widget.ScrollView/android.view.View)[1]'
    label_earn_hint = '//android.widget.ImageView[contains(@content-desc,"Make your first booking")]'

    button_redeem_credits = '//android.widget.ImageView[@content-desc="Redeem Swing Credits"]'
    switch_always_use = '//android.widget.Switch[contains(@content-desc,"Always use Swing Credits")]'
    button_see_all_cashbacks = '//android.widget.ImageView[@content-desc="See all cashbacks"]'
    button_learn_more = '//android.widget.ImageView[@content-desc="Learn more"]'
    button_see_history = '//android.widget.ImageView[@content-desc="See history"]'
    label_redeem_section = '//android.view.View[@content-desc="Redeem your Swing Credits"]'
    reward_card_by_name = '//android.view.View[contains(@content-desc,"%s")]'
    reward_card_any = '//android.view.View[contains(@content-desc,"Swing Credits") and @clickable="true"]'
    
    label_select_country_swing_credit = '//android.view.View[@content-desc="Select country for Swing Credits"]'
    button_selected_region = '//android.view.View[starts-with(@content-desc,"%s")]'
