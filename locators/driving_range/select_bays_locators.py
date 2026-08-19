class SelectBaysLocators:
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'
    label_title = '//android.view.View[@content-desc="How many bays?"]'
    label_number_of_bays = '//android.view.View[@content-desc="Number of bays"]'
    # stepper: first ImageView after the label = minus, second = plus.
    button_minus = '//android.view.View[@content-desc="Number of bays"]/following-sibling::android.widget.ImageView[1]'
    button_plus = '//android.view.View[@content-desc="Number of bays"]/following-sibling::android.widget.ImageView[2]'
    button_confirm = '//android.widget.Button[@content-desc="Confirm bays"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
    toaster_maximum_bay = '//android.view.View[@content-desc="You can only select up to %s bays"]'
