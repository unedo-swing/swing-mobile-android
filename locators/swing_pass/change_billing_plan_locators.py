class ChangeBillingPlanLocators:
    label_title = '//android.view.View[@content-desc="Change billing plan"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_section = '//android.view.View[@content-desc="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_RENEW_DATE = "Renew date"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    label_select_plan = '//android.view.View[@content-desc="Select new billing plan"]'

    plan_any = '//android.widget.RadioButton/parent::android.view.View'
    plan_selected = '//android.view.View[android.widget.RadioButton[@checked="true"]]'
    badge_current_plan = '//android.view.View[@content-desc="Current plan"]'
    plan_current = badge_current_plan + '/parent::android.view.View'

    plan_by_duration = '//android.view.View[android.widget.RadioButton and contains(@content-desc,"%s")]'
    radio_by_duration = plan_by_duration + '/android.widget.RadioButton'

    label_start_note = '//android.view.View[contains(@content-desc,"new billing plan will begin")]'

    checkbox_terms = '//android.widget.CheckBox'
    row_terms = checkbox_terms + '/parent::android.view.View'
    label_agree = '//android.view.View[contains(@content-desc,"I have read and agreed")]'
    link_terms = '//android.view.View[@clickable="true" and contains(@content-desc,"terms")]'

    slider_confirm = '//android.view.View[@content-desc="Slide to confirm"]'
    slider_thumb = slider_confirm + '/android.widget.ImageView'
