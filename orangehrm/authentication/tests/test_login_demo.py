"""
Demo test for visual debugging with highlight and blink effects.

This test demonstrates the use of highlight_element and blink_element methods
for visual debugging purposes. Effects are slowed down to be visible to the human eye.
"""
import pytest
import time
from orangehrm.authentication.pages import LoginPage
from framework.utils.logger import log_test_step, TestLogger


@pytest.mark.authentication
@pytest.mark.demo
class TestLoginDemo:
    """Demo test class for visual debugging effects."""

    @log_test_step("Demo: Visual login with highlight and blink effects")
    def test_login_with_visual_effects(self, login_page: LoginPage, valid_user):
        """
        Demonstrate successful login with visual debugging effects.

        This test uses:
        - highlight_element: Adds colored border to elements
        - blink_element: Makes elements blink multiple times

        The effects are intentionally slowed down to be visible.
        """
        logger = TestLogger.get_logger(__name__)

        logger.info("="*80)
        logger.info("🎨 DEMO: Visual Debugging Effects")
        logger.info("="*80)

        # Verify login page is loaded
        assert login_page.is_login_page_loaded()
        logger.info("✓ Login page loaded")
        time.sleep(1)

        # Step 1: Highlight the username field (green border)
        logger.info("1️⃣  Highlighting username field (GREEN)...")
        login_page.highlight_element(
            login_page.USERNAME_INPUT,
            color="green",
            duration=3  # 3 seconds
        )
        time.sleep(1)

        # Step 2: Enter username with blink effect
        logger.info("2️⃣  Entering username with BLINK effect (RED, 5 times)...")
        login_page.enter_username(valid_user.username)
        login_page.blink_element(
            login_page.USERNAME_INPUT,
            color="red",
            times=5  # Blink 5 times
        )
        time.sleep(1)

        # Step 3: Highlight password field (blue border)
        logger.info("3️⃣  Highlighting password field (BLUE)...")
        login_page.highlight_element(
            login_page.PASSWORD_INPUT,
            color="blue",
            duration=3
        )
        time.sleep(1)

        # Step 4: Enter password with blink effect
        logger.info("4️⃣  Entering password with BLINK effect (ORANGE, 5 times)...")
        login_page.enter_password(valid_user.password)
        login_page.blink_element(
            login_page.PASSWORD_INPUT,
            color="orange",
            times=5
        )
        time.sleep(1)

        # Step 5: Highlight login button (purple border)
        logger.info("5️⃣  Highlighting login button (PURPLE)...")
        login_page.highlight_element(
            login_page.LOGIN_BUTTON,
            color="purple",
            duration=3
        )
        time.sleep(1)

        # Step 6: Click login with blink effect
        logger.info("6️⃣  Clicking login button with BLINK effect (CYAN, 3 times)...")
        login_page.blink_element(
            login_page.LOGIN_BUTTON,
            color="cyan",
            times=3
        )
        login_page.click_login_button()
        time.sleep(2)  # Wait for navigation

        # Verify successful login
        current_url = login_page.get_current_url().lower()
        assert "dashboard" in current_url or "index" in current_url

        logger.info("="*80)
        logger.info("✅ DEMO COMPLETE: Login successful with visual effects!")
        logger.info("="*80)

    @log_test_step("Demo: Highlight multiple elements simultaneously")
    def test_highlight_all_login_elements(self, login_page: LoginPage):
        """
        Demo showing all login page elements highlighted at once.

        Useful for visual verification of page structure.
        """
        logger = TestLogger.get_logger(__name__)

        logger.info("="*80)
        logger.info("🎨 DEMO: Highlight All Login Elements")
        logger.info("="*80)

        assert login_page.is_login_page_loaded()

        logger.info("1️⃣  Highlighting all elements with different colors...")

        # Highlight all elements with different colors (they'll overlap)
        login_page.highlight_element(login_page.USERNAME_INPUT, color="green", duration=5)
        login_page.highlight_element(login_page.PASSWORD_INPUT, color="blue", duration=5)
        login_page.highlight_element(login_page.LOGIN_BUTTON, color="red", duration=5)

        logger.info("   - Username field: GREEN")
        logger.info("   - Password field: BLUE")
        logger.info("   - Login button: RED")
        logger.info("⏳ Waiting 5 seconds to show highlights...")

        time.sleep(5)

        logger.info("2️⃣  Blinking all elements sequentially...")
        login_page.blink_element(login_page.USERNAME_INPUT, color="yellow", times=3)
        logger.info("   ✓ Username field blinked")

        login_page.blink_element(login_page.PASSWORD_INPUT, color="orange", times=3)
        logger.info("   ✓ Password field blinked")

        login_page.blink_element(login_page.LOGIN_BUTTON, color="purple", times=3)
        logger.info("   ✓ Login button blinked")

        logger.info("="*80)
        logger.info("✅ DEMO COMPLETE: All elements highlighted and blinked!")
        logger.info("="*80)

    @log_test_step("Demo: Custom border styles and colors")
    def test_custom_highlight_styles(self, login_page: LoginPage):
        """
        Demo showing different highlight border styles and colors.

        Demonstrates customization options for visual debugging.
        """
        logger = TestLogger.get_logger(__name__)

        logger.info("="*80)
        logger.info("🎨 DEMO: Custom Highlight Styles")
        logger.info("="*80)

        assert login_page.is_login_page_loaded()

        # Test different border styles
        logger.info("1️⃣  Testing different border styles on username field...")

        logger.info("   - Thin border (2px solid)...")
        login_page.highlight_element(login_page.USERNAME_INPUT, color="red", border="2px solid", duration=2)
        time.sleep(2)

        logger.info("   - Medium border (5px solid)...")
        login_page.highlight_element(login_page.USERNAME_INPUT, color="blue", border="5px solid", duration=2)
        time.sleep(2)

        logger.info("   - Thick border (10px solid)...")
        login_page.highlight_element(login_page.USERNAME_INPUT, color="green", border="10px solid", duration=2)
        time.sleep(2)

        logger.info("   - Dashed border (3px dashed)...")
        login_page.highlight_element(login_page.USERNAME_INPUT, color="purple", border="3px dashed", duration=2)
        time.sleep(2)

        logger.info("   - Dotted border (3px dotted)...")
        login_page.highlight_element(login_page.USERNAME_INPUT, color="orange", border="3px dotted", duration=2)
        time.sleep(2)

        # Test different colors
        logger.info("2️⃣  Testing different colors with standard border (3px solid)...")

        colors = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta"]

        for color in colors:
            logger.info(f"   - {color.upper()}...")
            login_page.highlight_element(login_page.USERNAME_INPUT, color=color, duration=1)
            time.sleep(1)

        logger.info("="*80)
        logger.info("✅ DEMO COMPLETE: Custom styles demonstrated!")
        logger.info("="*80)
