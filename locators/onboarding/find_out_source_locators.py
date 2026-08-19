class FindOutSourceLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="How did you find out about Swing?"]'

    # ================= options =================
    # any option by its label, e.g. option_by_label % "Web search"
    option_by_label = '//android.widget.ImageView[@content-desc="%s"]'
    # every option on the screen (they all sit under the titled container)
    options_all = label_title + '//android.widget.ImageView[@content-desc]'

    option_social_media = option_by_label % "Social media"
    option_article_or_blogs = option_by_label % "Article or blogs"
    option_recommended = option_by_label % "Recommended by friends or family"
    option_web_search = option_by_label % "Web search"
    option_offline_advertisement = option_by_label % "Offline advertisement"
    option_swing_event = option_by_label % "A Swing event"
    option_others = option_by_label % "Others"

    # ================= navigation =================
    button_previous = '//android.widget.Button[@content-desc="Previous"]'
    button_finish = '//android.widget.Button[@content-desc="Finish"]'
