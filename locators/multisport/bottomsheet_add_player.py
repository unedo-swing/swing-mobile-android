class BottomsheetAddPlayer :
    title_bottomsheet = "//android.view.View[@content-desc='Add a player' or @content-desc='Invite a player']"
    button_close = "//android.view.View[@content-desc='Add a player']/android.widget.ImageView[1]"
    button_tab_search_friend = "//android.view.View[contains(@content-desc, 'Search a friend')]"
    button_tab_search_friend = "//android.view.View[contains(@content-desc, 'Add manually')]"
    input_search_friend_name = "//android.view.View[starts-with(@content-desc, 'Search your friend')]/android.widget.EditText"  
    button_option_player_name_static = "//android.view.View[contains(@content-desc, 'search result')]/following-sibling::*[1]"
    button_option_player_name_dynamic = "//android.view.View[contains(@content-desc, '%s')]"
    button_close_bottomsheet_switch_to_group_registration = "//android.widget.ImageView[@content-desc='Switch to group registration']/following-sibling::android.widget.Button"