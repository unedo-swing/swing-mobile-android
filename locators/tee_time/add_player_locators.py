class AddPlayerLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Add a player"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'

    # --- tabs (content-desc is "Tab N of 2\n<label>") ---
    tab_search_friend = '//android.view.View[contains(@content-desc,"Search a friend")]'
    tab_add_manually = '//android.view.View[contains(@content-desc,"Add manually")]'

    # --- tab 1: search a friend ---
    # search box carries a curly apostrophe, so anchor on an apostrophe-free part.
    input_search_friend = '//android.view.View[contains(@content-desc,"Search your friend")]//android.widget.EditText'
    label_search_hint = '//*[contains(@content-desc,"already has a Swing account")]'
    # a result row by name (structure guessed — adjust when you have the XML):
    #   friend_result_by_name % '"Tam Lembong"'
    friend_result_by_name = '(//*[contains(@content-desc,"%s")])[last()]'

    # --- tab 2: add manually ---
    link_add_from_contacts = '//android.widget.ImageView[@content-desc="Add from contacts"]'
    input_first_name = '//android.widget.EditText[@hint="* First name"]'
    input_last_name = '//android.widget.EditText[@hint="* Last name"]'
    button_country = '//android.view.View[@hint="Country"]'
    input_phone = '//android.widget.EditText[@hint="* Phone number"]'
    input_email = '//android.widget.EditText[@hint="Email"]'

    # --- submit ---
    button_save_player = '//android.widget.Button[@content-desc="Save player"]'
