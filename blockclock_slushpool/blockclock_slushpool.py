import pyinputplus as pyip
import requests
import json
import time



slush_pool_url = "https://slushpool.com/accounts/profile/json/btc/"
headers = {"SlushPool-Auth-Token": "<YOURSLUSHPOOLAUTHTOKENGOESHERE>"}
blockclock_ip = "<YOUBLOCKCLOCKIPGOESHERE>"

# Available tags
tags = {
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
  "Estimated Hash Rate": "cm.mining.hash_rate_2016_blocks",
  "USD Market Price": "cm.markets.price",
  "EUR Market Price": "coinbase.BTC-EUR.spot",
  "GBP Market Price": "coinbase.BTC-GBP.spot",
  "Sats per Dollar":  "cm.markets.sats_per_dollar",
  "Mempool Transactions": "cm.mempool.transactions",
  "Difficulty Retarget Date": "cm.retarget.retarget_date",
  "Blockchain Height": "cm.blockchain.block_height",
  "Moscow Time": "memes.moscow.time",
}
  

def instructions():
    print("""
    <---------------------------->
    Select the tags you wish to display by entering the line number and pressing enter after each entry.
    Enter the number 615 to skip to the next part or to end the selection process at any time.\n
    The list will display all available tags. First half is Slushpool tags, second is Blocklock tags.\n
    Tags will appear in the order selected and repeat continuously until the script is stopped (CTRL-C).
    You may also select a refresh rate. Min: 5 minutes, Max: 10080 minutes (1 week, cause why not??!).\n
    
    Note: Currently you can select up to 18 tags. You may select the same one multiple times.
          This is a WORK IN PROGRESS. ENJOY :)   
    <---------------------------->\n
          """)
    return 

def display_refresh_time():
    # obtain an integer from the user to set display refresh rate
    display_refresh = pyip.inputNum("Enter an update rate(5 - 10080 minutes) ", min=5, max=10080)
    print(f"\ndisplay will update every {display_refresh} minutes\n")  
    
    return int(display_refresh)
  
def helper_nothing_selected():
      print(f"\n\n\n\n\n\n\n\n<----You selected 0 items... Let's try that again eh?---->\n\n\n\n\n\n\n\n")
      time.sleep(3)
      return list_available_tags()

def list_available_tags():
  print("<--- Please select your tags --->\n")
  # list for user selected tags
  selected_tags = []
  max_length_list = len(tags)
  # get slushpool keys from dict and display to the user. 
  tags_to_list = list(tags.keys())
  for element in enumerate(tags_to_list):
      if element == "Moscow Time":
        print(f"{element}\nSlushpool Tags:\n")
      print(element) 
  print("\nTo Skip or move to the next step enter 615\n")
  # loop until user selects desired tags, add them to a list.
  while len(selected_tags) <= max_length_list:
      element = pyip.inputNum("Enter line number: ", min=0)
      if element == 615 or element > max_length_list:
        print(f"Selected Tags: {selected_tags}\n")
        if len(selected_tags) <= 0:
          helper_nothing_selected()
        break
      selected_tags.append(tags_to_list[int(element)])
      
  return selected_tags
  

def get_slushpool_stats():
  # try GET request and catch any errors
  try:
    response = requests.get(slush_pool_url, headers=headers)
    # make sure it's a valid 200 response
    if not response.status_code // 100 == 2:
      print(f"Error: Unexpected response {response}")
      print("Could not connect to slushpool\nTrying again in 15 seconds")
      time.sleep(15)
      get_slushpool_stats()      
  except requests.exceptions.RequestException as e:
    return f"Error: {e}"
    
  try:
    # change json response from slushpool to python Dict
    response_dict = json.loads(response.text)  
  except json.decoder.JSONDecodeError as e:
    return f"Json Error - check the URL/Parameters and try again.\nError: {e}"
  
  return response_dict
  
 
def loop_tag_list():
    # keep count so that we can continuously loop over the list of tags
    count = 0
    items_to_call = []
    # get user selection, get the appropriate key from the dict and add to the call list. 
    tag_list = list_available_tags()
    for tag in tag_list:
      result = tags.get(tag)
      items_to_call.append(result)
    refresh_rate = (display_refresh_time() * 60)
    # run indefinitely and display selected tags based on refresh rate.
    # different conditions based on tag used, different formating applied.
    while True:
       tag = items_to_call[count]
       slushpool_query_dict = get_slushpool_stats()
       if tag == 'ok_workers' or tag == 'off_workers':
         slushpool_element = slushpool_query_dict["btc"][tag]
         send_to_blockclock(slushpool_element, tag)
         print(f"Now Displaying: {tag}")
         if count >= len(items_to_call) - 1:
           count = 0
           time.sleep(refresh_rate)
         else:
           count += 1
           time.sleep(refresh_rate)
       elif tag == "hash_rate_5m" or tag == "hash_rate_60m" or tag == "hash_rate_24h" or tag == "hash_rate_scoring":
        slushpool_element = slushpool_query_dict["btc"][tag]
        formatted_hash_result = round(slushpool_element / 1000, 1)
        # call function that send formatted tags to blockclock
        send_to_blockclock(formatted_hash_result, tag)
        print(f"Now Displaying: {tag}")
        if count >= len(items_to_call) -1:
            count = 0
            time.sleep(refresh_rate)
        else:
            count += 1
            time.sleep(refresh_rate)
       elif tag == "confirmed_reward" or tag == "unconfirmed_reward" or tag == "estimated_reward" or tag == "all_time_reward":
        slushpool_element = slushpool_query_dict["btc"][tag]
        # format result to 7 digit precision
        formatted_result = "{:.7}".format(slushpool_element)
        send_to_blockclock(formatted_result, tag)
        print(f"Now Displaying: {tag}")
        if count >= len(items_to_call) -1:
            count = 0
            time.sleep(refresh_rate)
        else:
            count += 1
            time.sleep(refresh_rate)
       else:
          send_to_blockclock_backend_tag(tag)
          print(f"Now Displaying: {tag}")
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
        url = f"http://{blockclock_ip}/api/show/number/{result}?pair=ASIC/DOWN?"
      push_to_blocklock = requests.get(url)
    elif tag == "hash_rate_5m" or tag == "hash_rate_60m" or tag == "hash_rate_24h" or tag == "hash_rate_scoring": 
      url = f"http://{blockclock_ip}/api/show/number/{result}?pair=TH/S"
      push_to_blocklock = requests.get(url)
    else:
      url = f"http://{blockclock_ip}/api/show/number/{result}?sym=bitcoin"
      push_to_blocklock = requests.get(url)
    return push_to_blocklock
  
def send_to_blockclock_backend_tag(tag):
  # if tag == "cm.mempool.transactions":
  #   url = f"http://{blockclock_ip}/api/pick/{tag}?pair=MEM/POOL"
  #   push_backend_tag = requests.get(url)  
    url = f"http://{blockclock_ip}/api/pick/{tag}"
    push_backend_tag = requests.get(url)
  
    return push_backend_tag


def main():  
  instructions()
  loop_tag_list()


if __name__ == "__main__":
    main()