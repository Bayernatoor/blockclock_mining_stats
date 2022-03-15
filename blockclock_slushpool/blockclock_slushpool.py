import pyinputplus as pyip
import requests
import json
import time



slush_pool_url = "https://slushpool.com/accounts/profile/json/btc/"
headers = {"SlushPool-Auth-Token": "<YOURSLUSHPOOLAUTHTOKENGOESHERE>"}
blockclock_ip = "<YOUBLOCKCLOCKIPGOESHERE>"

blockclock_tags = {
    "Estimated Hash Rate": "cm.mining.hash_rate_2016_blocks",
    "USD Market Price": "cm.markets.price",
    "EUR Market Price": "coinbase.BTC-EUR.spot",
    "GBP Market Price": "coinbase.BTC-GBP.spot",
    "Sats per Dollar":  "cm.markets.sats_per_dollar",
    "Mempool Transactions": "cm.mempool.transactions",
    "Difficulty Retarget Date": "cm.retarget.retarget_date",
    "Blockchain Height": "cm.blockchain.block_height",
    "Moscow Time": "memes.moscow.time"
}

slushpool_tags = {
    "Confirmed Reward": "confirmed_reward",
    "Unconfirmed Reward": "unconfirmed_reward",
    "Estimated Reward": "estimated_reward",
    "Alltime Reward": "all_time_reward",
    "Hashrate 5m": "hash_rate_5m",
    "Hashrate 60m": "hash_rate_60m",
    "Hashrate 24h": "hash_rate_24h",
    "Hashrate Scoring": "hash_rate_scoring",
    "Active Workers": "ok_workers",
    "Offline workers": "off_workers", 
}

def instructions():
    print("""
    <---------------------------->
    Select the tags you wish to display by entering the line number and pressing enter.
    Enter the number 615 to skip to the next part or to end the selection process at any time.\n
    First list is Slushpool profile tags. Second list is Blockclock tags (COMING SOON). 
    Tags will appear in order selected and repeat continuously until the script is stopped (CTRL-C).
    You may also select a refresh rate. Min: 5 minutes, Max: 10080 minutes (1 week, cause why not??!).   
    <---------------------------->\n
          """)
    return 

def display_refresh_time():
    display_refresh = pyip.inputNum("Enter an update rate(5 - 999 minutes) ", min=5, max=10080)
    print(f"display will update every {display_refresh} minutes")  
    
    return int(display_refresh)
  
# def helper_nothing_selected():
#     if len(selected_tags_slushpool) <= 0:
#       print(f"\n\n\n\n\n\n\n\n<----You selected 0 items... Let's try that again eh?---->\n\n\n\n\n\n\n\n")
#       time.sleep(5)
#       list_slushpool_tags()

# def list_blocklock_tags():
#     print("<--- Please select your Blockclock default tags --->\n")
#     selectedElements_blockclock = []
#     maxLengthList = len(blockclock_tags)
#     blockclockToList = list(blockclock_tags.keys())
#     for element in enumerate(blockclockToList, 1):
#       print(element)
#     print("\nTo Skip or move to the next step enter 615\n")
#     while len(selectedElements_blockclock) < maxLengthList:
#         element = pyip.inputNum("Enter line number: ", min=0)
#         if element == 615:
#           print(f"You selected {selectedElements_blockclock}")
#           break
#         selectedElements_blockclock.append(blockclockToList[int(element)])
 
#     return selectedElements_blockclock
  
  
def list_slushpool_tags():
  print("<--- Please select your Slushpool tags --->\n")
  selected_tags_slushpool = []
  max_length_list_slush = len(slushpool_tags)
  slushpool_to_list = list(slushpool_tags.keys())
  for element in enumerate(slushpool_to_list):
      print(element) 
  print("\nTo Skip or move to the next step enter 615\n")
  while len(selected_tags_slushpool) < max_length_list_slush:
      element = pyip.inputNum("Enter line number: ", min=0)
      if element == 615 or element > max_length_list_slush:
        print(f"You selected {selected_tags_slushpool}")
        break
      selected_tags_slushpool.append(slushpool_to_list[int(element)])
      
  return selected_tags_slushpool
  

def get_slushpool_stats():
  # try GET request and catch any errors
  try:
    response = requests.get(slush_pool_url, headers=headers)
    
    if not response.status_code // 100 == 2:
      print(f"Error: Unexpected response {response}")
      print("Could not connect to slushpool\nTrying again in 15 seconds")
      time.sleep(15)
      get_slushpool_stats()      
  except requests.exceptions.RequestException as e:
    return f"Error: {e}"
    
  try:
    response_dict = json.loads(response.text)  
  except json.decoder.JSONDecodeError as e:
    return f"Json Error - check the URL/Parameters and try again.\nError: {e}"
  
  return response_dict
  
 
def format_slushpool_data():
    count = 0
    items_to_call = []
    slushpool_query_dict = get_slushpool_stats()
    slushpool_tag_list = list_slushpool_tags() 
    refresh_rate = (display_refresh_time() * 60)
    print(refresh_rate)
    for item in slushpool_tag_list:
      result = slushpool_tags.get(item)
      items_to_call.append(result)
    while True:
       x = items_to_call[count]
      #  print(x)
       if x == 'ok_workers' or x == 'off_workers':
         slushpool_element = slushpool_query_dict["btc"][x]
         send_to_blockclock(slushpool_element, x)
         if count >= len(items_to_call) - 1:
           count = 0
           time.sleep(refresh_rate)
         else:
           count += 1
           time.sleep(refresh_rate)
       elif x == "hash_rate_5m" or x == "hash_rate_60m" or x == "hash_rate_24h" or x == "hash_rate_scoring":
        slushpool_element = slushpool_query_dict["btc"][x]
        formatted_hash_result = round(slushpool_element / 1000, 1)
        send_to_blockclock(formatted_hash_result, x)
        if count >= len(items_to_call) -1:
            count = 0
            time.sleep(refresh_rate)
        else:
            count += 1
            time.sleep(refresh_rate)
       else: 
        slushpool_element = slushpool_query_dict["btc"][x]
        formatted_result = "{:.7}".format(slushpool_element)
        send_to_blockclock(formatted_result, x)
        if count >= len(items_to_call) -1:
            count = 0
            time.sleep(refresh_rate)
        else:
            count += 1
            time.sleep(refresh_rate)



def send_to_blockclock(result, tag): 
    # build URL for blocklock
    if tag == 'ok_workers' or tag == 'off_workers':
      if tag == "ok_workers":
        url = f"http://{blockclock_ip}/api/show/number/{result}?pair=ASIC/UP"
      else:
        url = f"http://{blockclock_ip}/api/show/number/{result}?pair=ASIC/DOWN"
      push_to_blocklock = requests.get(url)
    elif tag == "hash_rate_5m" or tag == "hash_rate_60m" or tag == "hash_rate_24h" or tag == "hash_rate_scoring": 
      url = f"http://{blockclock_ip}/api/show/number/{result}?pair=TH/S"
      push_to_blocklock = requests.get(url)
    else:
      url = f"http://{blockclock_ip}/api/show/number/{result}?sym=bitcoin"
      push_to_blocklock = requests.get(url)
    return push_to_blocklock


def main():
  instructions()
  format_slushpool_data()


if __name__ == "__main__":
    main()
