class JoinSuccessLocators:
    label_title = '//android.view.View[@content-desc="Membership acquired!"]'
    label_subtitle = '//android.view.View[@content-desc="Welcome to Swing Pass"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_JOIN_DATE = "Join date"
    FIELD_ENDS_ON = "Ends on"
    FIELD_MEMBERSHIP_ID = "Membership ID"
    FIELD_BILLING_AMOUNT = "Billing amount"
    FIELD_BILLING_METHOD = "Billing method"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    label_verification_note = ('//android.view.View[contains(@content-desc,'
                               '"complete the verification process")]')
    button_continue_verification = '//android.widget.ImageView[@content-desc="Continue to verification"]'
