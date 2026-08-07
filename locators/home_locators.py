class HomeLocators:
    # --- bottom navigation (content-desc is "<Label>\nTab N of 3") ---
    tab_home = '//android.widget.ImageView[starts-with(@content-desc,"Home")]'
    tab_activity = '//android.widget.ImageView[starts-with(@content-desc,"Activity")]'
    tab_account = '//android.widget.ImageView[starts-with(@content-desc,"Account")]'

    # --- header ---
    search_bar = '//android.widget.ImageView[@content-desc="Search..."]'
    region_selector = '//android.widget.ImageView[@content-desc="Search..."]/android.view.View'
    
    # -- Region Select
    title_select_region = '//android.view.View[@content-desc="Select country"]'
    label_region = '//android.widget.ImageView[@content-desc="%s"]'
    button_close_bottom_sheet_select_region = '//android.view.View[@content-desc="Select country"]/following-sibling::android.widget.Button'

    # --- greeting ("How would you like to swing today, <name>?") ---
    label_greeting = '//*[contains(@content-desc,"How would you like to swing today")]'

    # --- quick-action tiles ---
    action_tee_time = '//android.widget.ImageView[@content-desc="Tee time"]'
    action_driving_range = '//android.widget.ImageView[@content-desc="Driving range"]'
    action_events = '//android.widget.ImageView[@content-desc="Events"]'
    action_marketplace = '//android.widget.ImageView[@content-desc="Marketplace"]'

    # --- membership / credits ---
    card_membership = '//*[contains(@content-desc,"Renews on")]'
    label_credits = '//*[contains(@content-desc,"credits")]'

    # There are several identical "See all" links (one per carousel). Anchor
    # each to its section title so the right one is tapped.
    link_see_all = '//android.widget.ImageView[@content-desc="See all"]'  # first/any

    # --- "Explore golf courses near you" section ---
    label_explore_courses_title = '//*[contains(@content-desc,"Explore golf")]'
    label_explore_title = label_explore_courses_title  # backwards-compatible alias
    see_all_courses = (
        '//*[contains(@content-desc,"Explore golf")]'
        '/following::android.widget.ImageView[@content-desc="See all"][1]'
    )
    # any course card, or a specific one — pass a quoted string for %s:
    #   course_card_by_name % '"Klub Golf Bogor Raya"'
    course_card_any = '//android.view.View[contains(@content-desc,"cashback")]'
    course_card_by_name = '//android.view.View[contains(@content-desc,"%s")]'

    # --- "Explore driving ranges near you" section ---
    label_explore_ranges_title = '//*[contains(@content-desc,"Explore driving")]'
    see_all_ranges = (
        '//*[contains(@content-desc,"Explore driving")]'
        '/following::android.widget.ImageView[@content-desc="See all"][1]'
    )
    # driving-range cards carry a price like "Rp. .../ 60 mins" or ".../ 100 balls"
    range_card_any = '//android.view.View[contains(@content-desc,"mins") or contains(@content-desc,"balls")]'
    range_card_by_name = '//android.view.View[contains(@content-desc,"%s")]'

    # --- refer a friend card ---
    card_refer_friend = '//*[contains(@content-desc,"refer a friend to join Swing")]'
    button_refer_friend = '//android.widget.ImageView[@content-desc="Refer a friend"]'

    # --- "Need help with anything else?" card ---
    card_need_help = '//*[contains(@content-desc,"Need help with anything else")]'
    link_call_center = '//android.widget.ImageView[@content-desc="Go to call center"]'

    # --- footer cards (substrings avoid the apostrophes in "What's" / "we've" /
    #     "We'd" / "We're") ---
    card_whats_new = '//android.view.View[contains(@content-desc,"included on version")]'
    card_give_feedback = '//android.view.View[contains(@content-desc,"Give us feedback")]'
    card_follow_instagram = '//android.view.View[contains(@content-desc,"Follow us on Instagram")]'
    card_leave_rating = '//android.view.View[contains(@content-desc,"Leave a rating")]'
    card_request_venue = '//android.view.View[contains(@content-desc,"Request a golf venue")]'
    card_contact_support = '//android.view.View[contains(@content-desc,"Contact Swing support")]'
