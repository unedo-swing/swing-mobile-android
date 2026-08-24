class JoinSwingPassLocators:
    label_title = '//android.view.View[@content-desc="Join Swing Pass" and @heading="true"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    label_summary = ('//android.view.View[@clickable="true" and contains(@content-desc,"Rp.")'
                     ' and contains(@content-desc,"for ")]')

    label_select_plan = '//android.view.View[@content-desc="Select billing plan"]'

    BADGE_MOST_POPULAR = "MOST POPULAR!"

    plan_any = '//android.widget.RadioButton/parent::android.view.View'
    plan_selected = '//android.view.View[android.widget.RadioButton[@checked="true"]]'
    plan_by_duration = '//android.view.View[android.widget.RadioButton and contains(@content-desc,"%s")]'
    radio_by_duration = plan_by_duration + '/android.widget.RadioButton'
    plan_most_popular = ('//android.view.View[android.widget.RadioButton and'
                         ' starts-with(@content-desc,"' + BADGE_MOST_POPULAR + '")]')

    PLACEHOLDER_METHOD = "Select billing method"

    label_select_method = '//android.view.View[@content-desc="Select billing method"]'
    row_promo = '//android.widget.ImageView[@content-desc="Swing Pass promo code"]'
    button_add_promo = row_promo + '/android.widget.Button'
    row_method = ('//android.widget.ImageView[android.widget.Button and'
                  ' not(@content-desc="Swing Pass promo code")]')
    button_select_method = row_method + '/android.widget.Button'

    checkbox_terms = '//android.widget.CheckBox'
    row_terms = checkbox_terms + '/parent::android.view.View'
    label_agree = '//android.view.View[contains(@content-desc,"I have read and agreed")]'
    link_terms = '//android.view.View[@clickable="true" and contains(@content-desc,"terms")]'

    slider_confirm = '//android.view.View[@content-desc="Slide to confirm"]'
    slider_thumb = slider_confirm + '/android.widget.ImageView'
