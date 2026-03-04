import base64
import random
import requests
from seleniumbase import SB


def get_geo_data():
    geo_data = requests.get("http://ip-api.com/json/").json()
    return {
        "latitude": geo_data["lat"],
        "longitude": geo_data["lon"],
        "timezone": geo_data["timezone"],
        "language_code": geo_data["countryCode"].lower()
    }


def decode_channel_name(encoded_name: str) -> str:
    return base64.b64decode(encoded_name).decode("utf-8")


def handle_accept_button(driver):
    if driver.is_element_present('button:contains("Accept")'):
        driver.cdp.click('button:contains("Accept")', timeout=4)


def handle_start_watching(driver):
    if driver.is_element_present('button:contains("Start Watching")'):
        driver.cdp.click('button:contains("Start Watching")', timeout=4)
        driver.sleep(8)


def main():
    geo = get_geo_data()
    proxy_str = False

    encoded_name = "YnJ1dGFsbGVz"
    channel_name = decode_channel_name(encoded_name)

    url = f"https://www.twitch.tv/{channel_name}"
    # url = f"https://www.youtube.com/@{channel_name}/live"

    while True:
        with SB(
            uc=True,
            locale="en",
            ad_block=True,
            chromium_arg="--disable-webgl",
            proxy=proxy_str
        ) as driver:

            random_watch_time = random.randint(450, 800)

            driver.activate_cdp_mode(
                url,
                tzone=geo["timezone"],
                geoloc=(geo["latitude"], geo["longitude"])
            )

            driver.sleep(4)
            handle_accept_button(driver)

            driver.sleep(21)
            handle_start_watching(driver)
            handle_accept_button(driver)

            if driver.is_element_present("#live-channel-stream-information"):

                handle_accept_button(driver)

                # Secondary driver (logic preserved)
                secondary_driver = driver.get_new_driver(undetectable=True)
                secondary_driver.activate_cdp_mode(
                    url,
                    tzone=geo["timezone"],
                    geoloc=(geo["latitude"], geo["longitude"])
                )

                secondary_driver.sleep(15)
                handle_start_watching(secondary_driver)
                handle_accept_button(secondary_driver)

                driver.sleep(15)
                driver.sleep(random_watch_time)

            else:
                break


if __name__ == "__main__":
    main()
