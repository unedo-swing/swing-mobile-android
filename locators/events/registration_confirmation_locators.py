class RegistrationConfirmationLocators :
    # --- Header
    title_header = "//*[@content-desc='Registration confirmation']"
    button_back = "//*[@content-desc='Registration confirmation']/preceding-sibling::*"

    # --- Event details
    text_title_event = "//android.widget.ScrollView/*[@content-desc='%s']"
    text_title_date = "//android.widget.ScrollView//*[starts-with(@content-desc, 'Date')]"
    text_title_start_time = "//android.widget.ScrollView//*[starts-with(@content-desc, 'Starting Time')]"
    text_title_venue = "//android.widget.ScrollView//*[starts-with(@content-desc, 'Venue')]"
    text_title_player = "//android.widget.ScrollView//*[starts-with(@content-desc, 'Player')]"

    # --- User details
    text_host = "//*[@content-desc='%s']/following-sibling::android.view.View//android.widget.ImageView[contains(@content-desc, 'Rp')]"
    text_registration_fee = "//*[starts-with(@content-desc, 'Registration fee')]"
    switch_button_swing_credit = "//android.widget.Switch[contains(@content-desc, 'Swing Credit')]"
    button_add_player = "//android.widget.ImageView[@content-desc='Add a player' or contains(@content-desc, 'more players')]"
    input_notes = "//android.widget.EditText[starts-with(@hint, 'Add notes')]"
    button_change_event_type = "//android.view.View[@content-desc='%s']/following-sibling::android.widget.ImageView[1]"
    button_remove_player_specific = "(//android.widget.ImageView[@content-desc='Remove player'])[%i]"
    button_remove_player_all = "//android.widget.ImageView[@content-desc='Remove player']"

    # --- Price details
    text_price_details = "//*[@content-desc = 'Price details']"
    text_price_number = "//*[@content-desc='Price details']/following-sibling::*//android.widget.ImageView[contains(@content-desc, '(Host)')]"
    text_processing_fee = "//*[@content-desc='Price details']/following-sibling::*//android.view.View[starts-with(@content-desc, 'Processing fee')]"
    text_total_payment = "//*[@content-desc='Price details']/following-sibling::*//android.view.View[starts-with(@content-desc, 'Total payment')]"
    button_select_payment = "//android.widget.Button[@content-desc='Select payment']"
    button_change_payment = "//android.widget.Button[@content-desc='Change']/parent::*[@content-desc='%s']"

    # --- Footer details
    button_pay_now = "//android.widget.ImageView[@content-desc='Pay now']"



    # --- bottomsheets invite friend
    button_invite_friends = "//android.widget.ImageView[@content-desc='Invite friends']"

    #bottomsheet remove friend
    title_header_bottomsheet_remove_friends = "//android.view.View[starts-with(@content-desc, 'Remove ')]"
    button_remove_player_bottomsheet = "//android.widget.Button[starts-with(@content-desc, 'Remove ')]"
    button_keep_player_bottomsheet = "//android.widget.Button[starts-with(@content-desc, 'Keep ')]"

