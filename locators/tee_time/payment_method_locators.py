class PaymentMethodLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Select payment method"]'

    # --- section headers ---
    section_credit_cards = '//android.view.View[@content-desc="Credit cards"]'
    section_qris = '//android.view.View[@content-desc="QRIS"]'
    section_ewallets = '//android.view.View[@content-desc="E-wallets"]'

    # --- credit cards ---
    # by label: card_by_name % '"VISA 0014"' (first match)
    card_by_name = '//android.widget.ImageView[@content-desc="%s"]'
    # nth card with a repeated label: card_by_index % ('"VISA 2503"', 2)
    card_by_index = '(//android.widget.ImageView[@content-desc="%s"])[%d]'
    button_add_credit_card = '//android.widget.ImageView[@content-desc="Add credit card"]'

    # --- QRIS option (the tappable one, not the section header) ---
    option_qris = '//android.widget.ImageView[@content-desc="QRIS"]'

    # --- e-wallets ---
    # ewallet_by_name % '"Gopay"'  ('Shopee Pay' / 'Link Aja' / 'Gopay')
    ewallet_by_name = '//android.widget.ImageView[@content-desc="%s"]'
