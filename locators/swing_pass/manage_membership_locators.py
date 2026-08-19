class ManageMembershipLocators:
    # ================= rows =================
    ROW_BILLING_HISTORY = "See billing history"
    ROW_CHANGE_PLAN = "Change billing plan"
    ROW_CHANGE_METHOD = "Change billing method"
    ROW_CONTACT_SUPPORT = "Contact Swing Support"
    ROW_CANCEL_MEMBERSHIP = "Cancel Swing Pass membership"

    row_by_label = '//android.view.View[@content-desc="%s"]'
    row_billing_history = row_by_label % ROW_BILLING_HISTORY
    row_change_plan = row_by_label % ROW_CHANGE_PLAN
    row_change_method = row_by_label % ROW_CHANGE_METHOD
    row_contact_support = row_by_label % ROW_CONTACT_SUPPORT
    row_cancel_membership = row_by_label % ROW_CANCEL_MEMBERSHIP

    # ================= dismissing =================
    # the unlabelled button at the foot of the sheet (Close)
    button_close = '//android.widget.Button[not(@content-desc) or @content-desc=""]'
    # the dimmed area above the sheet; tapping it dismisses
    scrim = '//android.view.View[@content-desc="Scrim"]'
