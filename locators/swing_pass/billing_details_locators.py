class BillingDetailsLocators:
    label_title = '//android.view.View[@content-desc="Billing Details"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_section = '//android.view.View[@content-desc="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_MEMBERSHIP_ID = "Membership ID"
    FIELD_BILLING_DURATION = "Billing duration"
    FIELD_JOIN_DATE = "Join date"
    FIELD_RENEWS_ON = "Renews on"
    FIELD_PAYMENT_DATE = "Payment date"
    FIELD_TOTAL = "Total"
    FIELD_PAYMENT_METHOD = "Payment method"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    label_helping_hand = '//android.view.View[@content-desc="Need a helping hand?"]'
    button_contact_support = '//android.view.View[@content-desc="Contact Swing Support"]'

    button_send_receipt = '//android.widget.Button[@content-desc="Send receipt"]'
