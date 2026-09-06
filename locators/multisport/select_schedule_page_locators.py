class SelectSchedulePageLocators:
    #--- header
    header_select_schedule_page = "//android.view.View[@content-desc='Select your schedule']"
    button_back_from_select_schedule_page = "//android.view.View[@content-desc='Select your schedule']/preceding-sibling::android.widget.ImageView"
    button_calendar = "//android.view.View[@content-desc='Select your schedule']/following-sibling::android.widget.ImageView"

    #--- body
    text_there_is_no_schedule = "//android.view.View[@content-desc='Unfortunately, there are no more available time slots on this date']"
    button_go_to_next_day = "//android.widget.Button[@content-desc='Go to the next day']"
    button_pick_date = "//android.view.View[@content-desc='%s']" #need to make function to create text format like "05 sep" if you want to selecting date
    button_choose_schedule = "//*[starts-with(@resource-id, '%s') and contains(@resource-id, '%s') and not(contains(@resource-id, 'not_available')) and not(contains(@content-desc, 'Booked'))][%i]" #first %s should be years and second %s should be title schedule (should be on lowercase) and %i is how much you awnt to select the schedule 
    button_confirm_schedule = "//android.widget.Button[@content-desc='Confirm Schedules']"
    text_total_price = "//android.widget.Button[@content-desc='Confirm Schedules']/preceding-sibling::android.widget.ImageView[ends-with(@content-desc, 'schedules selected')]"


