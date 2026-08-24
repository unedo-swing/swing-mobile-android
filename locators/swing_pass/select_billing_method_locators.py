class SelectBillingMethodLocators:
    label_title = '//android.view.View[@content-desc="Select billing method"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_credit_cards = '//android.view.View[@content-desc="Credit cards"]'
    card_any = label_credit_cards + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    card_at = '(' + card_any + ')[%d]'
    card_by_label = '//android.widget.ImageView[@clickable="true" and @content-desc="%s"]'
    button_add_card = '//android.widget.ImageView[@content-desc="Add credit card"]'

    label_ewallets = '//android.view.View[@content-desc="E-wallets"]'
    wallet_any = label_ewallets + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    wallet_by_name = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'
    button_connect_by_wallet = wallet_by_name + '/android.widget.Button'
