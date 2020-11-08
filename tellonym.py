import argparse
import logging
import time
import sys

from lib.service import Service
from lib.constants import PAGE_URL
from lib.utils import sleep_random, proxy_regex

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO)


class Tellonym(object):
    def __init__(self, user, timeout, proxy):
        self.cookies = False
        self.user = user
        self.timeout = timeout

        self.s = Service(url=PAGE_URL + self.user, timeout=self.timeout, proxy=proxy)

    def send(self, message) -> bool:
        self.s.load_page()

        if not self.cookies:
            self.s.handle_popup()
            self.cookies = True

        self.s.send_message(message)

        try:
            return self.s.validate_message()
        except:
            return False

    def close(self) -> None:
        self.s.close_browser_instance()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""Py-onym: Tellonym message spammer.""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('user', help="Name of the target user.")
    parser.add_argument(
        '-i',
        '--input-file',
        help="Input file containing messages to be sent.",
        type=argparse.FileType('r'),
        default='-')
    parser.add_argument(
        '-t',
        '--times',
        help="Number of times to loop through the messages",
        type=int,
        default=1)
    parser.add_argument(
        '-r',
        '--retries',
        help='Number of times to retry sending message until giving up.',
        type=int,
        default=10)
    parser.add_argument(
        '-T',
        '--timeout',
        help='Number of seconds to wait on each operation until giving up.',
        type=int,
        default=10)
    parser.add_argument(
        '-R',
        '--rate',
        help='Number of seconds to wait between sending each message.',
        type=int,
        default=1)
    parser.add_argument(
        '-p',
        '--proxy',
        help='Proxy server to be used for browser proxy configuration (firefox only).',
        type=proxy_regex
    )

    args = parser.parse_args()
    return args


def run(args=None):
    logging.info("Starting Tellonym Spammer application.")

    # read messages from input file or stdin and load them in a list
    messages = [message.strip() for message in args.input_file.readlines()]

    tellonym = Tellonym(args.user, args.timeout, args.proxy)

    for _ in range(args.times):
        for message in messages:
            logging.info("Sending message: '%s'" % message)
            tries = 0

            while True:
                try:
                    if tellonym.send(message):
                        logging.info("Message sent succesfully.")
                        break

                except KeyboardInterrupt:
                    logging.info(
                        "Caught keyboard interrupt signal. Shutting down...")
                    tellonym.close()

                    sys.exit(0)

                else:
                    if tries > args.retries:
                        logging.error("Max retries exceeded. Giving up.")
                        tellonym.close()

                        sys.exit(1)
                    else:
                        logging.error("Failed to send message. Retrying...")
                        tries += 1

            sleep_random(args.rate, args.rate + 1)

    # close browser instance
    tellonym.close()


def main():
    run(parse_args())

if __name__ == "__main__":
    main()
