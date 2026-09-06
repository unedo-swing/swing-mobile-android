class AllVenueListPage:
        #--- header
        header_all_venue_list_page = "//android.view.View[ends-with(@content-desc, 'billiard venues')]"

        #--- body
        button_card_venue = "//android.view.View[contains(@resource-id, 'venue_card') and contains(@content-desc, '%s')]"