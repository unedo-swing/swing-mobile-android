class AddCreditCardLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Add credit card"]'

    # --- form fields ---
    input_cardholder = '//android.widget.EditText[@hint="Enter name"]'
    input_card_number = '//android.view.View[@content-desc="0000 - 0000 - 0000 - 0000"]//android.widget.EditText'
    input_expiry = '//android.widget.EditText[@hint="MM / YY"]'
    input_cvv = '//android.widget.EditText[@hint="123"]'

    switch_set_primary = '//android.view.View[@content-desc="Set as primary method"]//android.widget.Switch'
    link_terms = '//android.view.View[@content-desc="Terms & conditions."]'

    button_save = '//android.widget.Button[@content-desc="Save credit card"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
