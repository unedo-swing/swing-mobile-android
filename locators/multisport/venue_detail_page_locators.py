class VenueDetailPageLocators:
    #--- header
    header_venue_details = "//android.view.View[@content-desc='Venue details']"
    button_back_from_venue_details = "//android.view.View[@content-desc='Venue details']/preceding-sibling::android.widget.ImageView"

    #--- body
    text_venue_name = "//android.widget.ScrollView/android.view.View[@content-desc='%s']"
    button_tab_venue_info = "//android.view.View[starts-with(@content-desc,'Tab 1')]"
    button_tab_menu_packages = "//android.view.View[starts-with(@content-desc,'Tab 2')]"

    #--- footer
    button_book_venue = "//android.widget.Button[@content-desc='Book venue']"