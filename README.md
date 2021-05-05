A simple python-package tool created to help gather emote analytics from any twitch VOD.

Requires a Twitch Client ID and Twitch Secret ID. 
If you don't have one visit [Twitch Development Console](https://dev.twitch.tv/console/apps) to learn more about obtaining it.

### Installation: 
```console
pip install VODet
```

## Usage
Obtain the VOD ID from the disired VOD, ( VOD_ID from https://www.twitch.tv/videos/VOD_ID when viewing a vod)
-v <VOD_ID>
--e to get emote usage distribution

![image](https://user-images.githubusercontent.com/35205235/117105731-a4dd0500-ad4c-11eb-865e-1cd59c5389e6.png)

![image](https://user-images.githubusercontent.com/35205235/117105939-00a78e00-ad4d-11eb-9343-1093b188aac4.png)

--t <EMOTE_NAME> 

add flag --external if not build into twitch

![image](https://user-images.githubusercontent.com/35205235/117105806-c5a55a80-ad4c-11eb-9d92-25b0a4442238.png)

Plots are saved according to config.json (can be changed).

![image](https://user-images.githubusercontent.com/35205235/117105868-e5d51980-ad4c-11eb-8334-bc23849e28fe.png)

add flag --segment <SEGMENTS> to change how the data gets segmented in seconds
 
add flag --timestamps to get VOD link recommendations for the emote. Add a number --timestamps <TIMESTAMPS> to specify number of suggestions
