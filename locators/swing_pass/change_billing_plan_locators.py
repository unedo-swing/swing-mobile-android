class ChangeBillingPlanLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Change billing plan"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= membership summary =================
    label_section = '//android.view.View[@content-desc="Swing Pass membership"]'

    FIELD_PLAYER_NAME = "Player name"
    FIELD_RENEW_DATE = "Renew date"
    FIELD_MEMBERSHIP_ID = "Membership ID"

    label_by_name = '//android.view.View[@content-desc="%s"]'
    value_by_label = label_by_name + '/following-sibling::android.view.View[1]'

    # ================= plan list =================
    label_select_plan = '//android.view.View[@content-desc="Select new billing plan"]'

    # Every selectable plan — matched through its radio, which keeps the
    # clickable page root out of the result.
    plan_any = '//android.widget.RadioButton/parent::android.view.View'
    # the plan whose radio is on
    plan_selected = '//android.view.View[android.widget.RadioButton[@checked="true"]]'
    # The plan the account is on now: no radio, a "Current plan" badge instead.
    # Reached from the badge's parent — ``//View[.//View[...]]`` would match
    # every ancestor up to the page root as well.
    badge_current_plan = '//android.view.View[@content-desc="Current plan"]'
    plan_current = badge_current_plan + '/parent::android.view.View'

    # one plan by its duration, e.g. plan_by_duration % "3 months".
    # Substring match, so a duration that is a suffix of another ("2 months"
    # inside "12 months") would need the full label.
    plan_by_duration = '//android.view.View[android.widget.RadioButton and contains(@content-desc,"%s")]'
    radio_by_duration = plan_by_duration + '/android.widget.RadioButton'

    # ================= start-date note =================
    # "Your new billing plan will begin when your current plan ends on 02 March 2027"
    label_start_note = '//android.view.View[contains(@content-desc,"new billing plan will begin")]'

    # ================= terms =================
    checkbox_terms = '//android.widget.CheckBox'
    # the whole tappable row around the checkbox
    row_terms = checkbox_terms + '/parent::android.view.View'
    label_agree = '//android.view.View[contains(@content-desc,"I have read and agreed")]'
    # "Swing Pass’s terms & conditions" — curly apostrophe in the copy, so it is
    # matched on a fragment without one
    link_terms = '//android.view.View[@clickable="true" and contains(@content-desc,"terms")]'

    # ================= confirm =================
    # A slider, not a button: tapping it does nothing, the thumb has to be
    # dragged across. ChangeBillingPlanPage.slide_to_confirm does the drag.
    slider_confirm = '//android.view.View[@content-desc="Slide to confirm"]'
    slider_thumb = slider_confirm + '/android.widget.ImageView'
