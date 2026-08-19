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

    # ================= date groups =================
    # a date heading, e.g. group_by_date % "Mon, 10 Aug 2026"
    group_by_date = '//android.view.View[@content-desc="%s"]'
    # Every date heading. Matched on shape rather than on nesting depth: the
    # headings are the only focusable-but-not-clickable Views carrying a comma
    # (entries are clickable; the filter chip labels have no comma). A
    # structural path can't be used — the scroll view disappears entirely when
    # the list is short enough to fit, which is exactly the new-account case.
    group_any = '//android.view.View[@focusable="true" and not(@clickable="true") and contains(@content-desc,", ")]'

    # ================= entries =================
    # Every entry card. Anchored on the trailing "earned"/"used" line, NOT on
    # the word "booking": a new account's first entry is a referral reward
    # ("Reward for using <name>'s referral"), which is not a booking at all.
    entry_any = (
        '//android.view.View[@clickable="true" and '
        '(contains(@content-desc,"earned") or contains(@content-desc,"used"))]'
    )
    # an entry by its booking id, e.g. entry_by_booking_id % "QZA4T"
    entry_by_booking_id = '//android.view.View[contains(@content-desc,"#%s") and @clickable="true"]'
    # an entry by any fragment of its label
    entry_by_text = '//android.view.View[contains(@content-desc,"%s") and @clickable="true"]'
    # the referral-signup reward a new account gets for entering a referral
    # code. The label carries an apostrophe ("Tam's referral"), so it's matched
    # on the apostrophe-free part.
    entry_referral = '//android.view.View[contains(@content-desc,"referral")]'
    # the 50,000-credit signup reward, whole card in one content-desc:
    # "Reward for using QA's referral\n13:05\n+ 50,000\nearned" — the name (and
    # its apostrophe) is stepped over, and translate() drops the thousands
    # comma so "50,000" and "50000" both match
    entry_referral_reward = '//android.view.View[contains(@content-desc,"Reward for using") and contains(@content-desc,"referral") and contains(translate(@content-desc,",",""),"50000")]'
    # the entries inside one date group, e.g. entries_in_group % "Fri, 07 Aug 2026"
    entries_in_group = group_by_date + (
        '//android.view.View[@clickable="true" and '
        '(contains(@content-desc,"earned") or contains(@content-desc,"used"))]'
    )
