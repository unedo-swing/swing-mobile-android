class BilliardPageLocators:
    #--- header
    header_billiard_page = "//*[@resource-id='home_multisport_explore_nearest_title']"

    #--- body
    button_see_all_venue = "//*[@resource-id='home_multisport_explore_nearest_see_all_button']"
    button_card_venue = "//*[starts-with(@resource-id, 'home_multisport_explore_card') and contains(@content-desc, '%s')]"