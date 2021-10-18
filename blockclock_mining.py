import requests
import json
import time

slush_pool_url = "https://slushpool.com/accounts/profile/json/btc/"
headers = {"SlushPool-Auth-Token": "<YOURSLUSHPOOLAPITOKEN>"}


def get_stats():
    # pull data from slushpool api - specific user
    stats = requests.get(slush_pool_url, headers=headers)
    # convert json into dict
    stats_dict = json.loads(stats.text)
    # get the confirmed_reward value
    confirmed_reward = stats_dict["btc"]["confirmed_reward"]
    # truncate to 7 character for blocklock
    formatted_reward = "{:.7}".format(confirmed_reward)

    return float(formatted_reward)


def send_stats():
    reward = get_stats()
    url = f"http://<YOURBLOCKCLOCKIP>/api/show/number/{reward}?sym=bitcoin"
    # push data to blockclock
    send_to_blockclock = requests.get(url)

    return send_to_blockclock


def main():
    print("Mining Ahoy!")
    old_reward = get_stats()
    print(old_reward)
    while True:
        new_reward = get_stats()
        print(new_reward)
        if new_reward > old_reward:
            send_stats()
        else:
            print("sleeping for 5 minutes to the sound of hashing ASICs")
            time.sleep(5 * 60)


if __name__ == "__main__":
    main()
