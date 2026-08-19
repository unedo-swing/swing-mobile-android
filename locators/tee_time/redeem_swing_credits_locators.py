class RedeemSwingCreditsLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    # title is a View; the confirm button below is a Button with the same label.
    label_title = '//android.view.View[@content-desc="Redeem Swing Credits"]'
    input_code = '//android.widget.EditText[@hint="Enter Swing Credits Code"]'
    button_redeem = '//android.widget.Button[@content-desc="Redeem Swing Credits"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
