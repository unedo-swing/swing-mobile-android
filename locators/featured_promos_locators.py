"""
Android XPaths for the shared "Featured promos" screen.

Reached from the promo strip on tee time, event and driving-range details
(the "See all" tile), so it is deliberately global — nothing here is
product-specific. Flutter app: everything surfaces through ``content-desc``.
"""


class FeaturedPromosLocators:
    # ================= header =================
    label_title = '//android.view.View[@content-desc="Featured promos"]'
    button_back = '(//android.widget.ImageView[@clickable="true"])[1]'

    # ================= info banner =================
    # "Featured promos are now automatically claimed and will be automatically
    # applied whenever they are eligible."
    banner_auto_claim = '//android.widget.ImageView[contains(@content-desc,"automatically claimed")]'

    # ================= promo cards =================
    # Every card carries a "Validity" line, which is also what keeps the
    # auto-claim banner — nested inside the first card — out of the match.
    promo_any = '//android.widget.ImageView[contains(@content-desc,"Validity")]'
    # the Nth card, 1-based and top-down
    promo_at = '(' + promo_any + ')[%d]'
    # a card by any fragment of its label — usually the promo name
    # promo_by_name % 'HARI INI'
    promo_by_name = '//android.widget.ImageView[contains(@content-desc,"Validity") and contains(@content-desc,"%s")]'

    # the redemption quota badge sits *inside* a card, e.g. "x1 / day"
    quota_any = '//android.view.View[contains(@content-desc,"/ day")]'
    # quota_by_promo % 'HARI INI'
    quota_by_promo = promo_by_name + '//android.view.View[contains(@content-desc,"/ day")]'

    # marks a card as Swing Pass only
    badge_swing_pass_by_promo = promo_by_name + '[contains(@content-desc,"Swing Pass Exclusive")]'
