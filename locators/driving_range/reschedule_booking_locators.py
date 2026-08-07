"""
Android XPaths for the Swing Driving Range > Reschedule booking screen.

Opened from Change Booking > 'Continue reschedule'. Pick a new date & time
(keeping the same duration / bays / bay type). Shows the original booking
summary, a day grid and a time-slot grid, then 'Confirm new date & time'.

Flutter app — values surface through ``content-desc``.
"""


class RescheduleBookingLocators:
    # ================= header =================
    label_reschedule_booking = '//android.view.View[@content-desc="Reschedule booking"]'
    button_back = '//android.view.View[@content-desc="Reschedule booking"]/preceding-sibling::android.widget.ImageView[1]'

    # ================= original booking summary =================
    label_new_date_time = '//android.view.View[@content-desc="Select new date & time"]'
    label_original_date_time = '//android.view.View[@content-desc="Original date & time"]'
    value_original_date_time = '(//android.view.View[@content-desc="Original date & time"]/following-sibling::*)[1]'
    label_duration = '//android.view.View[@content-desc="Duration"]'
    value_duration = '(//android.view.View[@content-desc="Duration"]/following-sibling::*)[1]'
    label_bays = '//android.view.View[@content-desc="Bays"]'
    value_bays = '(//android.view.View[@content-desc="Bays"]/following-sibling::*)[1]'
    label_bay_type = '//android.view.View[@content-desc="Bay type"]'
    value_bay_type = '(//android.view.View[@content-desc="Bay type"]/following-sibling::*)[1]'
    label_description_reschedule = '//android.view.View[@content-desc="You can only reschedule by maintaining the same duration, number of bays, and bay type as the original booking. "]'
    button_open_calender = '//android.view.View[@content-desc="You can only reschedule by maintaining the same duration, number of bays, and bay type as the original booking. "]/following-sibling::*[3]'
    button_date_in_calender = '//android.view.View[contains(@content-desc,"%s")]'
    # ================= week / day grid =================
    # the current week range, e.g. "03 Aug - 09 Aug"
    label_week_range = '//android.view.View[contains(@content-desc," - ")]'
    # a day-of-month cell by its number, e.g. "5" (disabled days are enabled=false)
    date_by_number = '//android.widget.Button[@content-desc="%s"]'

    # ================= time grid =================
    # a time slot, e.g. "18:00" (only available slots are clickable=true)
    button_slot_time = '//android.view.View[@content-desc="%s"]'

    # ================= confirm =================
    # disabled (enabled=false) until a date + time are selected
    button_confirm_new_date = '//android.widget.Button[@content-desc="Confirm new date & time"]'
