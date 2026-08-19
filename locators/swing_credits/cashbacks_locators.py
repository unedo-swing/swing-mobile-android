class CashbacksLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Swing Credits cashbacks"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= search =================
    _search_box = '//android.view.View[@content-desc="Search here..."]'
    input_search = _search_box + '//android.widget.EditText'

    # ================= tabs =================
    # content-desc is "Tab N of 4\n<label>", so a label alone isn't unique
    # enough — pair it with the "of 4" part. The selected tab has selected=true.
    TAB_ALL = "All"
    TAB_DRIVING_RANGE = "Driving range"
    TAB_GOLF_COURSE = "Golf course"
    TAB_EVENT = "Event"

    tab_by_label = '//*[contains(@content-desc,"of 4") and contains(@content-desc,"%s")]'
    tab_all = tab_by_label % TAB_ALL
    tab_driving_range = tab_by_label % TAB_DRIVING_RANGE
    tab_golf_course = tab_by_label % TAB_GOLF_COURSE
    tab_event = tab_by_label % TAB_EVENT
    tab_selected = '//*[contains(@content-desc,"of 4") and @selected="true"]'

    # ================= column headers =================
    label_regular_players = '//android.view.View[contains(@content-desc,"Regular Swing")]'
    label_pass_members = '//android.view.View[contains(@content-desc,"Swing Pass")]'

    # ================= venue rows =================
    # the venue name, e.g. venue_by_name % "Bandung Golf Country"
    venue_by_name = '//android.view.View[@content-desc="%s"]'
    # Everything else in the row is a following sibling View of that name, in
    # render order: type, the "•" separator, location, days, hours, the regular
    # rate, its "cashback" caption, then the Swing Pass rate. Positional, so it
    # breaks if the row layout changes — check here first when a value reads
    # wrong.
    venue_type = venue_by_name + '/following-sibling::android.view.View[1]'
    venue_location = venue_by_name + '/following-sibling::android.view.View[3]'
    venue_days = venue_by_name + '/following-sibling::android.view.View[4]'
    venue_hours = venue_by_name + '/following-sibling::android.view.View[5]'
    venue_cashback_regular = venue_by_name + '/following-sibling::android.view.View[6]'
    venue_cashback_pass = venue_by_name + '/following-sibling::android.view.View[8]'
