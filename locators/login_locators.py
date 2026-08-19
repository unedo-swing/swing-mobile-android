
class LoginLocators:
    # --- phone entry screen ---
    label_header = '//android.view.View[@content-desc="Log in or sign up"]'
    button_country_code = '//android.view.View[@hint="Country"]'
    # The picked country as shown on the button: 'ID (+62)'. Matched on the
    # '(+' rather than a fixed country so any selection is readable.
    label_country_code = '//android.view.View[contains(@text,"(+")]'
    input_phone_number = '//android.widget.EditText[@hint="Phone Number"]'
    button_continue = '//android.widget.Button[@content-desc="Continue"]'
    label_verification_title = '//android.view.View[@content-desc="Select verification method"]'
    button_verification_sms = '//android.widget.ImageView[contains(@content-desc,"SMS")]'
    button_verification_whatsapp = '//android.widget.ImageView[@content-desc="WhatsApp"]'
    label_otp_title = '//*[@content-desc="SMS verification" or @content-desc="WhatsApp verification"]'
    input_verification_code = '//android.widget.EditText'
    label_resend_timer = '//*[contains(@content-desc,"Send again")]'
    link_switch_to_whatsapp = '//*[@content-desc="Try verification with WhatsApp"]'
    button_close = '//android.widget.Button[@content-desc="Close" or @content-desc="close"]'
    label_secure_challenge = (
        '//*[@content-desc="One more check" '
        'or contains(@content-desc,"secure challenge") '
        'or contains(@content-desc,"Verify you are human")]'
    )
