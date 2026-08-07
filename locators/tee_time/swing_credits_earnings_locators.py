"""
Android XPaths for the Swing Tee Time > "Swing Credits earnings" dialog.

Opened by tapping the "+ N (for all)" credits bar on the booking confirmation.
Lists the Swing Credits each player earns. Flutter app — elements surface
through ``content-desc``.
"""


class SwingCreditsEarningsLocators:
    label_title = '//android.view.View[@content-desc="Swing Credits earnings"]'
    # a player's credit row (content-desc: "<Name>\n• <%> ...\n+<amount>"):
    #   player_credit_by_name % '"Tam Lembong"'
    player_credit_by_name = '//*[contains(@content-desc,"%s")]'
    button_got_it = '//android.widget.Button[@content-desc="Got it!"]'
    scrim = '//android.view.View[@content-desc="Scrim"]'
