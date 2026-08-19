class AccountLocators:
    # --- profile header ---
    link_edit_personal_info = '//android.widget.ImageView[@content-desc="Edit my personal information"]'
    label_username = '//android.view.View[starts-with(@content-desc,"@")]'
    # display name varies — match a known value: label_name_by_text % '"QA Auto Mation"'
    label_name_by_text = '//android.view.View[@content-desc="%s"]'

    # --- refer a friend card (also on Home) ---
    card_refer_friend = '//*[contains(@content-desc,"refer a friend to join Swing")]'
    button_refer_friend = '//android.widget.ImageView[@content-desc="Refer a friend"]'

    # --- section headers ---
    label_section_account = '//android.view.View[@content-desc="Account"]'
    label_section_support = '//android.view.View[@content-desc="Support"]'
    label_section_legal = '//android.view.View[@content-desc="Legal"]'

    # --- "Account" section rows ---
    menu_saved_credit_cards = '//android.view.View[@content-desc="Saved credit cards"]'
    menu_notifications_settings = '//android.view.View[@content-desc="Notifications settings"]'
    menu_my_receipts = '//android.view.View[@content-desc="My receipts"]'

    # --- "Support" section rows ---
    menu_give_us_feedback = '//android.view.View[@content-desc="Give us feedback"]'
    menu_contact_support = '//android.view.View[@content-desc="Contact Swing support"]'
    menu_delete_account = '//android.view.View[@content-desc="Delete my account"]'

    # --- "Legal" section rows ---
    menu_terms = '//android.view.View[@content-desc="Terms & conditions"]'
    menu_privacy_policy = '//android.view.View[@content-desc="Privacy policy"]'

    # --- log out ---
    button_log_out = '//android.widget.ImageView[@content-desc="Log out"]'

    # generic menu row by its label: menu_item % '"Saved credit cards"'
    menu_item = '//android.view.View[@content-desc="%s"]'

    # --- bottom navigation ---
    tab_home = '//android.widget.ImageView[starts-with(@content-desc,"Home")]'
    tab_activity = '//android.widget.ImageView[starts-with(@content-desc,"Activity")]'
    tab_account = '//android.widget.ImageView[starts-with(@content-desc,"Account")]'
    
    # ----- Log out ---
    label_logout = '//android.view.View[@content-desc="Log out?"]'
    button_log_out_bottom_sheet = '//android.widget.Button[@content-desc="Log out"]'
    button_cancel_logout = '//android.widget.Button[@content-desc="Cancel log out"]'
    button_close_bottom_sheet = '//android.view.View[@content-desc="Log out?"]/following-sibling::android.widget.Button[last()]'
