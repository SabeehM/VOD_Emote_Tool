A simple python-package created to help gather emote analytics from any twitch VOD.

Requires a Twitch Client ID and Twitch Secret ID. 
If you don't have one visit [Twitch Development Console](https://dev.twitch.tv/console/apps) to learn more about obtaining it.

### Installation: 
```console
pip install VODet
```
*NOTE: May need to install colorama: `pip install colorama`*

## Usage
Obtain the VOD ID from the disired VOD [VOD_ID from https://www.twitch.tv/videos/VOD_ID]

#### Required Parameter

`-v <VOD_ID>`

*NOTE: Either --e or --t must be used*

##### Emote Distribution

`--e` to get emote usage distribution

##### Emote Usage over Time

`--t <EMOTE_NAME>` to get emote usage over time

add flag `--external` if not build into twitch

add flag `--segment <SEGMENTS>` to change how the data gets segmented in seconds
 
add flag `--timestamps` to get VOD link recommendations for the emote. Add a number `--timestamps <TIMESTAMPS>` to specify number of suggestions

*Plots are saved according to config.json (can be changed).*

### Upcoming Features

- Get data specific to a user
- Option to include emote spam
- Add external emotes to distribution

### Screenshots

__Extracting comment data__

![image](https://user-images.githubusercontent.com/35205235/117105731-a4dd0500-ad4c-11eb-865e-1cd59c5389e6.png)

__Emote distribution output__

![image](https://user-images.githubusercontent.com/35205235/117105939-00a78e00-ad4d-11eb-9343-1093b188aac4.png)

__Emote usage plot output__

![image](https://user-images.githubusercontent.com/35205235/117105868-e5d51980-ad4c-11eb-8334-bc23849e28fe.png)

__VOD suggestion output__

![image](https://user-images.githubusercontent.com/35205235/117444981-2c22a800-af08-11eb-8798-b16b74fdfb1a.png)


