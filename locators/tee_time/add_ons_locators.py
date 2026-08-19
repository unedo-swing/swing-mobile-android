class AddOnsLocators:
    label_title = '//android.view.View[@content-desc="Select add-ons"]'
    label_for_player = '//android.view.View[starts-with(@content-desc,"For ")]'

    # a whole add-on row by name: addon_row_by_name % '"Stick"'
    addon_row_by_name = '//android.view.View[starts-with(@content-desc,"%s")]'
    # +/- steppers inside a named row (1st ImageView = minus, 2nd = plus):
    addon_minus_by_name = '//android.view.View[starts-with(@content-desc,"%s")]/android.widget.ImageView[1]'
    addon_plus_by_name = '//android.view.View[starts-with(@content-desc,"%s")]/android.widget.ImageView[2]'

    # bottom buttons (Save label carries the count, e.g. "Save 2 add-ons")
    button_save = '//android.widget.Button[starts-with(@content-desc,"Save")]'
    button_cancel = '//android.widget.Button[@content-desc="Cancel"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
