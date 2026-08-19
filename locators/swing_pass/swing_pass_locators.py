class SwingPassLocators:
    # ================= header =================
    # exact match: contains("Swing Pass") would also hit the comparison card,
    # the FAQ heading and the promo section label
    label_title = '//android.view.View[@content-desc="Swing Pass" and @heading="true"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    # the country/region toggle in the top-right, e.g. "ID"
    button_region = '//android.widget.ImageView[@content-desc="ID"]'
    button_region_by_code = '//android.widget.ImageView[@content-desc="%s"]'

    # ================= membership card =================
    # "<Member name>\n<PASS-ID>\n • \nActive until 02 Mar 2027"
    card_membership = '//android.view.View[contains(@content-desc,"Active until")]'
    # the "BETA" badge printed on the card
    label_beta = '//android.view.View[@content-desc="BETA"]'
    button_enlarge_card = '//android.view.View[@content-desc="Enlarge card"]'

    # ================= savings summary =================
    # "Since 02 Jul 2026, you’ve saved\nRp. 3,530,012\nSee how you’ve saved this much"
    # Anchored on " saved" — the line carries a curly apostrophe that is not
    # safe to put in an XPath literal.
    card_savings = '//android.widget.ImageView[contains(@content-desc," saved")]'

    # ================= with / without comparison =================
    # "728,027\nWithout Swing Pass\n583,391\nWith Swing Pass"
    card_comparison = '//android.view.View[contains(@content-desc,"Without Swing Pass")]'
    # the link inside it: "See how you've earned 0 more with Swing Pass since 02 Jul 2026."
    button_see_earnings = '//android.widget.ImageView[contains(@content-desc,"more with Swing Pass since")]'

    # ================= billing =================
    # "Rp. 150,000 / 7 months\nRenews on 02 Mar 2027"
    button_manage = '//android.widget.Button[@content-desc="Manage"]'
    # The card wrapping that button. Matched through the button rather than on
    # "Renews on", which changes wording once a membership is cancelled.
    card_billing = '//android.widget.ImageView[.//android.widget.Button[@content-desc="Manage"]]'
    # The card's second line switches wording once the Pass is cancelled:
    # "Renews on 02 Mar 2027" while active, "Ends on 02 Mar 2027" after.
    label_renews_on = '//android.widget.ImageView[contains(@content-desc,"Renews on")]'
    label_ends_on = '//android.widget.ImageView[contains(@content-desc,"Ends on")]'
    # Shown under the billing card after a plan change has been confirmed:
    # "You've updated your plan. From 02 Mar 2027, you'll be charged Rp. 50,000
    # every 3 months." Absent until then, so treat it as optional.
    label_plan_updated = '//android.widget.ImageView[contains(@content-desc,"updated your plan")]'

    # ================= cancelled state =================
    # Replaces the plan-updated banner once the membership is cancelled:
    # "You can still use Swing Pass until 02 Mar 2027 and it won't be auto renewed."
    label_cancellation_notice = '//android.widget.ImageView[contains(@content-desc,"auto renewed")]'
    # A win-back footer appears too — pinned BELOW the scroll view, not inside
    # it, so it needs no scrolling to reach.
    label_renew_prompt = '//android.view.View[contains(@content-desc,"Keep your membership active")]'
    button_renew = '//android.widget.Button[@content-desc="Renew"]'

    # ================= member-only promos =================
    # "Exclusive promos only for\nSwing Pass members"
    label_promos_section = '//android.view.View[contains(@content-desc,"Exclusive promos")]'
    # The promo strip is the section label's next sibling — the strip itself
    # carries no content-desc of its own, so there is nothing else to anchor
    # on. Positional: check here first if the promo list reads empty.
    #
    # Direct children only, deliberately: each promo card holds a nested
    # ImageView for its category chip ("Tee Time", "Driving Range"), so a
    # descendant search would return every card twice.
    promo_any = label_promos_section + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    # one promo card by its code, e.g. promo_by_code % "JANPROMO"
    # content-desc is "<CODE>\n<days>. <hours>."
    promo_by_code = '//android.widget.ImageView[contains(@content-desc,"%s")]'
    # the category chip printed on a card, e.g. "Driving Range"
    promo_category_by_code = promo_by_code + '/android.widget.ImageView'

    # ================= benefits =================
    # "<Benefit title>\n<description>", e.g.
    #   "Earn more Swing Credits\nSwing Pass member earns up to 10% more ..."
    benefit_by_title = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'
    # Every benefit card. The benefit strip is the sibling right before
    # 'See all cashbacks' — same story as promo_any, no content-desc to anchor
    # on. Flutter builds lazily, so this only ever returns what is on screen.
    button_see_all_cashbacks = '//android.widget.ImageView[@content-desc="See all cashbacks"]'
    benefit_any = button_see_all_cashbacks + '/preceding-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'

    # ================= FAQ =================
    label_faq_section = '//android.view.View[@content-desc="FAQs about Swing Pass"]'
    # Every FAQ row, taken from the block right after the heading. Each row's
    # content-desc holds BOTH the question and its answer, newline separated,
    # whether or not the row is expanded — so the answer can be read without
    # tapping anything.
    faq_any = label_faq_section + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView[@clickable="true"]'
    # one FAQ by its question, e.g. faq_by_question % "How long is my Pass valid?"
    faq_by_question = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'

    # ================= footer =================
    # note the trailing space in the app's copy
    label_other_questions = '//android.view.View[contains(@content-desc,"Have any other questions")]'
    button_contact_us = '//android.view.View[@content-desc="Contact us here."]'
