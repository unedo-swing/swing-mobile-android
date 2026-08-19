class ReferralRewardDetailsLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Referral reward details"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= terms =================
    # "By using <name>'s referral code, enjoy 50,000 Swing Credits. Expires one
    # month after received."
    label_description = '//android.view.View[contains(@content-desc,"referral code, enjoy")]'
    # "Expired on Thu, 10 Sep 2026 23:59"
    label_expiry = '//android.view.View[contains(@content-desc,"Expired on")]'

    # ================= amount =================
    label_credits = '//android.view.View[@content-desc="Swing Credits"]'
    # the "+ 50,000" sits after the label, with the coin icon between them —
    # following-sibling skips the ImageView, so [1] is the amount
    value_amount = label_credits + '/following-sibling::android.view.View[1]'
    # "Earned on Mon, 10 Aug 2026 14:51"
    label_earned_on = '//android.view.View[contains(@content-desc,"Earned on")]'

    # ================= support =================
    label_have_question = '//android.view.View[@content-desc="Have a question?"]'
    # content-desc is "Contact Swing support\nWe're here for you if you need help"
    button_contact_support = '//android.view.View[contains(@content-desc,"Contact Swing support")]'
