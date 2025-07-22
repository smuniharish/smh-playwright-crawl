from threading import Lock
import asyncio
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

_set_policy_once = Lock()
_policy_set = False

def set_playwright_event_loop_if_needed():
    global _policy_set
    if sys.platform.startswith("win") and not _policy_set:
        with _set_policy_once:
            if not _policy_set:
                current_policy = asyncio.get_event_loop_policy()
                if not isinstance(current_policy, asyncio.WindowsSelectorEventLoopPolicy):
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                    logger.info("WindowsSelectorEventLoopPolicy set for Playwright.")
                _policy_set = True
