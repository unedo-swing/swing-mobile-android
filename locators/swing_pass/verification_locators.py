class VerificationLocators:
    label_title = '//android.view.View[@content-desc="Swing Pass verification" and @heading="true"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_headline = '//android.view.View[contains(@content-desc,"waiting for your verification")]'
    label_description = '//android.view.View[contains(@content-desc,"complete verification to start using it")]'

    label_full_name = '//android.view.View[contains(@content-desc,"Full name as on your identification")]'
    input_full_name = '//android.widget.EditText'

    section_photo = '//android.view.View[starts-with(@content-desc,"Take a picture of yourself")]'
    button_open_camera = '//android.widget.ImageView[@content-desc="Open camera"]'

    button_submit = '//android.widget.Button[@content-desc="Submit verification"]'
