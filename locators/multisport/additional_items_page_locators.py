class AdditionalItemsPageLocators:
        header_page_title = "//android.view.View[@content-desc='Additional items']"
        button_back_page = "//android.view.View[@content-desc='Additional items']/preceding-sibling::android.widget.ImageView"

        button_add_additional_items = "//android.widget.ImageView[contains(@content-desc, '%s')]//android.widget.Button" # -> 'BALLS' dynamic additional items name
        button_skip_additional_items = "//android.widget.Button[@content-desc='Skip additional items']"
        button_plus_additional_items = "(//android.widget.Button[@content-desc='Save items']/preceding-sibling::android.view.View[last()]/android.view.View//android.widget.ImageView)[last()]"
        button_minus_additional_items = "(//android.widget.Button[@content-desc='Save items']/preceding-sibling::android.view.View[last()]/android.view.View//android.widget.ImageView)[last() - 1]"
        button_save_additional_items = "//android.widget.Button[@content-desc='Save items']"
        button_confirm_additional_items = "//android.widget.Button[@content-desc='Confirm additional items']"

        button_edit_additional_items = "//android.widget.ImageView[contains(@content-desc, '%s')]/android.widget.ImageView[@content-desc='Edit']"
