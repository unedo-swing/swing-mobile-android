class ProfileSetupLocators:
    # ================= header =================
    # anchored on an apostrophe-free part of "Hi, welcome to Swing! Let's begin
    # by setting up your account and profile."
    label_welcome = '//android.view.View[contains(@content-desc,"welcome to Swing")]'
    form = '//android.widget.ScrollView'

    # ================= name =================
    input_first_name = '//android.widget.EditText[@hint="First name"]'
    input_last_name = '//android.widget.EditText[@hint="Last name"]'

    # ================= picker fields (read-only, tap to open a dialog) =================
    # the selected value shows up as the field's own content-desc once chosen
    field_birthday = '//android.view.View[@hint="Birthday"]'
    field_nationality = '//android.view.View[@hint="Nationality"]'
    field_gender = '//android.view.View[@hint="Gender"]'
    # the trailing chevron / calendar icon inside each field
    icon_birthday = field_birthday + '/android.widget.ImageView'
    icon_nationality = field_nationality + '/android.widget.ImageView'
    icon_gender = field_gender + '/android.widget.ImageView'

    # ================= username / email / referral =================
    input_username = '//android.widget.EditText[@hint="Username"]'
    label_username_hint = '//*[contains(@content-desc,"Your friends will be able to search for your profile")]'
    input_email = '//android.widget.EditText[@hint="Email"]'
    label_email_hint = '//*[contains(@content-desc,"confirmations")]'
    input_referral_code = '//android.widget.EditText[@hint="Referral code"]'

    # ================= submit =================
    # enabled=false until the required fields are filled
    button_next = '//android.widget.Button[@content-desc="Next"]'

    # ================= helpers =================
    # a validation / error message by its wording, e.g.
    #   label_message % "Username is already taken"
    label_message = '//*[contains(@content-desc,"%s")]'
