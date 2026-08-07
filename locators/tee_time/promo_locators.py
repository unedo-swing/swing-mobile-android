class PromoLocators:
    # --- Available promos list ---
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="Available promos"]'
    input_search = '//android.view.View[@content-desc="Search here..."]//android.widget.EditText'
    section_your_promos = '//android.view.View[@content-desc="Your promos"]'
    promo_by_name = '//android.view.View[contains(@content-desc,"%s")]'
    button_apply = '//android.widget.Button[@content-desc="Apply"]'
    apply_by_promo_name = '//android.view.View[contains(@content-desc,"%s")]//android.widget.Button[@content-desc="Apply"]'
    button_remove_promo = '//android.widget.ImageView[@content-desc="Remove promo"]'
    button_add_promo_code = '//android.widget.Button[@content-desc="Add a promo code"]'

    # --- "Add a Promo Code" dialog ---
    label_add_promo_title = '//android.view.View[@content-desc="Add a Promo Code"]'
    input_promo_code = '//android.widget.EditText[@hint="e.g. SWING123"]'
    button_submit_promo = '//android.widget.Button[@content-desc="Add Promo code"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
