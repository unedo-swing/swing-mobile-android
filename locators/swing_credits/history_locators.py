class HistoryLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Swing Credits history"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= filter chips =================
    FILTER_ALL = "All"
    FILTER_EARNED = "Credits Earned"
    FILTER_USAGE = "Credits Usage"

    chip_by_label = '//android.view.View[@content-desc="%s"]'
    chip_all = chip_by_label % FILTER_ALL
    chip_earned = chip_by_label % FILTER_EARNED
    chip_usage = chip_by_label % FILTER_USAGE

    group_by_date = '//android.view.View[@content-desc="%s"]'
    group_any = '//android.view.View[@focusable="true" and not(@clickable="true") and contains(@content-desc,", ")]'

    entry_any = (
        '//android.view.View[@clickable="true" and '
        '(contains(@content-desc,"earned") or contains(@content-desc,"used"))]'
    )
    entry_by_booking_id = '//android.view.View[contains(@content-desc,"#%s") and @clickable="true"]'
    entry_by_text = '//android.view.View[contains(@content-desc,"%s") and @clickable="true"]'
    entry_referral = '//android.view.View[contains(@content-desc,"referral")]'
    entry_referral_reward = '//android.view.View[contains(@content-desc,"Reward for using") and contains(@content-desc,"referral") and contains(translate(@content-desc,",",""),"50000")]'
    entries_in_group = group_by_date + (
        '//android.view.View[@clickable="true" and '
        '(contains(@content-desc,"earned") or contains(@content-desc,"used"))]'
    )
    
    list_credit_by_booking_code = '//android.view.View[contains(@content-desc, "%s")]'
    list_credit_by_reward_for_refferal = '(//android.view.View[contains(@content-desc, "Reward for referring")])[1]'
    list_credit_by_reward_by_using_refferal = '//android.view.View[contains(@content-desc, "Reward for using")]'
