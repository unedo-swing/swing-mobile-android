class SelectBillingMethodLocators:
    # ================= header =================
    # a View here; the picker row on the Change billing method screen carries
    # the same content-desc but is an ImageView
    label_title = '//android.view.View[@content-desc="Select billing method"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= credit cards =================
    label_credit_cards = '//android.view.View[@content-desc="Credit cards"]'
    card_any = label_credit_cards + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    # the Nth saved card, 1-based and top-down — the only unambiguous handle
    # when several cards share a label
    card_at = '(' + card_any + ')[%d]'
    # a card by its label, e.g. card_by_label % "VISA 0014". Returns the FIRST
    # match, which is wrong whenever the label is duplicated.
    card_by_label = '//android.widget.ImageView[@clickable="true" and @content-desc="%s"]'
    button_add_card = '//android.widget.ImageView[@content-desc="Add credit card"]'

    # ================= e-wallets =================
    label_ewallets = '//android.view.View[@content-desc="E-wallets"]'
    wallet_any = label_ewallets + '/following-sibling::android.view.View[1]/android.view.View/android.widget.ImageView'
    # a wallet row by its name, e.g. wallet_by_name % "OVO" -> "OVO Connect"
    wallet_by_name = '//android.widget.ImageView[starts-with(@content-desc,"%s")]'
    # every wallet's button reads "Connect", so scope it to its row
    button_connect_by_wallet = wallet_by_name + '/android.widget.Button'
