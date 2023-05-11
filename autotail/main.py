import argparse
import logging
from autotail.workersunitedlies import WorkersUnitedLiesDeployment
import traceback
import sys
import time

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(
    "TELL MANY OF THE SAME STORY", epilog="IF THEY WANT STORIES, WE'LL GIVE EM STORIES"
)
parser.add_argument("-n", type=int, default=1, help="Apply for n jobs (default: 1)")
parser.add_argument("--relentless", action="store_true", help="Keep applying forever")
parser.add_argument(
    "--noheadless",
    action="store_false",
    help="Show the chromium driver as it fills in the application",
)
parser.add_argument(
    "--leaveopen",
    action="store_true",
    help="Try to leave the browser open after an application is completed",
)
parser.add_argument(
    "--juststories",
    action="store_true",
    help="Just print n ChatGPT stories to the console",
)
parser.add_argument(
    "-f", type=str, default="stories.csv", help="Output file for stories (default: 1)"
)


def main():
    args = parser.parse_args()
    headless = args.noheadless  # flipped bool b/c store_false above

    deployment = WorkersUnitedLiesDeployment

    if args.juststories:
        for i in range(args.n):
            bot = deployment.make(headless=headless)
            with open(args.f, "a") as fi:
                fi.write(bot.get_story())
        return

    if args.relentless:
        while True:
            bot = deployment.make(headless=headless)
            with open(args.f, "a") as fi:
                fi.write(bot.get_story())
            bot.post_story()
            if headless:
                bot.quit(args.leaveopen)
            logging.info("Success!")
    else:
        for i in range(args.n):
            try:
                print(
                    "-" * 50 + f"\n    submitting story #{i+1}/{args.n}\n" + "-" * 50,
                    flush=True,
                )
                bot = deployment.make(headless=headless)
                with open(args.f, "a") as fi:
                    fi.write(bot.get_story())
                bot.post_story()
                if headless:
                    bot.quit(args.leaveopen)
                logging.info("Success!")
            except Exception as e:
                logging.error(f"Error! {e}")
                traceback.print_exc()
                print(
                    "-" * 50
                    + f"\n    failed submission for #{i+1}/{args.n}! Trying next\n"
                    + "-" * 50,
                    flush=True,
                )
