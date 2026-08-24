class ChangeBillingMethodLocators:
    label_title = '//android.view.View[@content-desc="Change billing method"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_section = '//android.view.View[@content-desc="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_RENEW_DATE = "Renew date"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    label_select_method = '//android.view.View[@content-desc="Select new billing method"]'
    PLACEHOLDER_METHOD = "Select billing method"
    row_method = '//android.widget.ImageView[android.widget.Button]'
    button_select = row_method + '/android.widget.Button'

    checkbox_terms = '//android.widget.CheckBox'
    row_terms = checkbox_terms + '/parent::android.view.View'
    label_agree = '//android.view.View[contains(@content-desc,"I have read and agreed")]'
    link_terms = '//android.view.View[@clickable="true" and contains(@content-desc,"terms")]'

    slider_confirm = '//android.view.View[@content-desc="Slide to confirm"]'
    slider_thumb = slider_confirm + '/android.widget.ImageView'
