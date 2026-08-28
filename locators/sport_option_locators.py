class SportOptionLocators:
    label_title = '//android.view.View[@resource-id="sport_option_page_title"]'
    scroll_view = '//android.widget.ScrollView'

    card_by_code = '//android.view.View[@resource-id="sport_option_card_%s"]'
    card_by_name = '//android.view.View[@resource-id and contains(@resource-id,"sport_option_card_") and @content-desc="%s"]'
    cards_all = '//android.view.View[contains(@resource-id,"sport_option_card_")]'

    card_golf = card_by_code % "GOLF"
    card_billiard = card_by_code % "BILLIARD"
    card_padel = card_by_code % "PADEL"
    card_badminton = card_by_code % "BADMINTON"
    card_tennis = card_by_code % "TENNIS"
    card_basketball = card_by_code % "BASKETBALL"
    card_football = card_by_code % "FOOTBALL"
    card_volleyball = card_by_code % "VOLLEYBALL"
    card_running = card_by_code % "RUNNING"
    card_table_tennis = card_by_code % "TABLE_TENNIS"

    badge_beta_in_card = card_by_code + '//android.view.View[@content-desc="BETA"]'
    badge_coming_soon_in_card = card_by_code + '//android.view.View[@content-desc="COMING SOON"]'
    badge_beta_any = '//android.view.View[@content-desc="BETA"]'
    badge_coming_soon_any = '//android.view.View[@content-desc="COMING SOON"]'
