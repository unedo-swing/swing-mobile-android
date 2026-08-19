class CancelSwingPassLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Cancel Swing Pass"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= membership summary =================
    label_section = '//android.view.View[@content-desc="Swing Pass membership"]'

    # note the capitals — this screen's labels are not the other screens'
    FIELD_PLAYER_NAME = "Player Name"
    FIELD_CANCEL_DATE = "Cancel Date"
    FIELD_ENDS_ON = "Ends on"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    # ================= cancellation reason =================
    label_reason_section = '//android.view.View[@content-desc="Cancellation reason"]'
    # "Before you go, please share with us why you’re cancelling ..."
    label_reason_hint = '//android.view.View[contains(@content-desc,"please share with us why")]'

    # Fragments, not full labels — see the note on apostrophes above.
    REASON_NO_VALUE = "much value in the benefits"
    REASON_TOO_EXPENSIVE = "too expensive"
    REASON_CANNOT_USE_UP = "struggling to use up"
    REASON_DIDNT_KNOW_AUTORENEW = "know it auto-renews"
    REASON_RARELY_USED = "using Swing that often"
    REASON_OTHER_PROVIDER = "another plan or membership"
    REASON_NO_PERKS = "perks available"

    # the radio carries the label itself on this screen
    reason_any = '//android.widget.RadioButton'
    reason_by_text = '//android.widget.RadioButton[contains(@content-desc,"%s")]'
    reason_selected = '//android.widget.RadioButton[@checked="true"]'

    # ================= confirm =================
    # An ImageView, not a Button, and enabled="false" until a reason is picked.
    button_cancel_membership = '//android.widget.ImageView[@content-desc="Cancel membership"]'
