class ActivityLocators:
    label_activity = '//android.view.View[@content-desc="Activity"]'
    label_filter_driving_range = '//android.widget.ImageView[contains(@content-desc,"Driving range")]'
    label_filter_tee_time = '//android.widget.ImageView[contains(@content-desc,"Tee time")]'
    label_filter_event = '//android.widget.ImageView[contains(@content-desc,"Event")]'
    label_filter_marketplace = '//android.widget.ImageView[contains(@content-desc,"Marketplace")]'
    
    # a booking card matched by name + time + date (no payment)
    # e.g. (//android.widget.ImageView[contains(@content-desc,"Albatross Driving Range")
    #        and contains(@content-desc,"18:00") and contains(@content-desc,"11 Aug 2026")])[1]
    card_activity = '(//android.widget.ImageView[contains(@content-desc, "%s") and contains(@content-desc, "%s") and contains(@content-desc, "%s")])[1]'
    
    