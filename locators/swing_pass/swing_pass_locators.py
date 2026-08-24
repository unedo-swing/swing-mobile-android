class SwingPassLocators:
    label_title = '//android.view.View[@content-desc="Swing Pass" and @heading="true"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    button_region = '//android.widget.ImageView[@content-desc="ID"]'
    button_region_by_code = '//android.widget.ImageView[@content-desc="%s"]'

    card_membership = '//android.view.View[contains(@content-desc,"Active until")]'
    card_membership_inactive = '//android.view.View[contains(@content-desc,"Inactive")]'
    card_membership_waiting = '//android.view.View[contains(@content-desc,"Waiting for verification")]'
    card_membership_any = ('//android.view.View[contains(@content-desc,"Active until")'
                           ' or contains(@content-desc,"Inactive")'
                           ' or contains(@content-desc,"Waiting for verification")]')
    label_beta = '//android.view.View[@content-desc="BETA"]'
    button_enlarge_card = '//android.view.View[@content-desc="Enlarge card"]'

    label_verification_submitted = '//android.view.View[@content-desc="Verification submitted!"]'
    label_verification_note = '//android.view.View[contains(@content-desc,"will be verified within")]'
    button_ok_got_it = '//android.view.View[@content-desc="Ok, got it!"]'
    button_contact_support = '//android.widget.Button[@content-desc="Contact Swing Support"]'

    label_tagline = '//android.view.View[@content-desc="The one true ultimate golf membership"]'
    label_subscribe_info = '//android.view.View[contains(@content-desc,"Subscribe to Swing pass")]'
    button_join = '//android.widget.ImageView[@content-desc="Join Swing Pass"]'

    card_savings = '//android.widget.ImageView[contains(@content-desc," saved")]'

    card_comparison = '//android.view.View[contains(@content-desc,"Without Swing Pass")]'
    button_see_earnings = '//android.widget.ImageView[contains(@content-desc,"more with Swing Pass since")]'

    button_manage = '//android.widget.Button[@content-desc="Manage"]'
    card_billing = '//android.widget.ImageView[.//android.widget.Button[@content-desc="Manage"]]'
    label_renews_on = '//android.widget.ImageView[contains(@content-desc,"Renews on")]'
    label_ends_on = '//android.widget.ImageView[contains(@content-desc,"Ends on")]'
    label_plan_updated = '//android.widget.ImageView[contains(@content-desc,"updated your plan")]'

    label_cancellation_notice = '//android.widget.ImageView[contains(@content-desc,"auto renewed")]'
    label_renew_prompt = '//android.view.View[contains(@content-desc,"Keep your membership active")]'
    button_renew = '//android.widget.Button[@content-desc="Renew"]'

    label_promos_section = '//android.view.View[contains(@content-desc,"Exclusive promos")]'
    promo_any = label_promos_section + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    promo_by_code = '//android.widget.ImageView[contains(@content-desc,"%s")]'
    promo_category_by_code = promo_by_code + '/android.widget.ImageView'

    benefit_by_title = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'
    button_see_all_cashbacks = '//android.widget.ImageView[@content-desc="See all cashbacks"]'
    benefit_any = button_see_all_cashbacks + '/preceding-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'

    label_faq_section = '//android.view.View[@content-desc="FAQs about Swing Pass"]'
    faq_any = label_faq_section + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView[@clickable="true"]'
    faq_by_question = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'

    label_other_questions = '//android.view.View[contains(@content-desc,"Have any other questions")]'
    button_contact_us = '//android.view.View[@content-desc="Contact us here."]'
