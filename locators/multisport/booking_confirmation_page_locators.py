class BookingConfirmationPageLocators:
    #--- header
    header_booking_confirmation_page = "//android.view.View[@content-desc='Booking Confirmation']"
    button_back_from_booking_page = "//android.view.View[@content-desc='Booking Confirmation']/preceding-sibling::android.widget.ImageView"

    #--- body
    button_edit_schedule = "//android.widget.Button[@content-desc='Edit']"
    button_add_player = "//android.widget.ImageView[@content-desc='Add a player' or contains(@content-desc, 'more players')]"
    button_delete_player = "(//android.view.View[@content-desc='Players']/following-sibling::android.view.View//android.widget.ImageView)[%i]"
    text_all_player_total = "//android.view.View[@content-desc='Players']//following-sibling::android.view.View[1]/android.view.View/android.view.View"
    button_select_payment = "//android.widget.Button[@content-desc='Select payment']"

    #--- footer
    button_pay_now = "//android.widget.ImageView[@content-desc='Pay now']"