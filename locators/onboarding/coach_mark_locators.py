class CoachMarkLocators:
    # ================= titles =================
    TITLE_SPORT_MODE = "Change sport mode"
    TITLE_COUNTRIES = "Change countries"

    # a coach mark by title, e.g. label_title % TITLE_SPORT_MODE
    label_title = '//android.view.View[@content-desc="%s"]'
    label_title_sport_mode = label_title % TITLE_SPORT_MODE
    label_title_countries = label_title % TITLE_COUNTRIES

    # any coach mark, whichever one is currently up
    any_title = (
        f'//android.view.View[@content-desc="{TITLE_SPORT_MODE}"'
        f' or @content-desc="{TITLE_COUNTRIES}"]'
    )

    # ================= body =================
    # the explanatory line under a title, matched on a distinctive fragment
    label_body = '//android.view.View[contains(@content-desc,"%s")]'
    body_sport_mode = label_body % "change from one sport mode to another"
    body_countries = label_body % "change countries"

    # ================= dismiss =================
    # the same button on every coach mark — tapping it advances to the next one
    button_got_it = '//android.widget.Button[@content-desc="Got it!"]'
