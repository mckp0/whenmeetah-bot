## Inspiration
As we grow older, our schedules get busier and it becomes increasingly hard to find a common time to meet up with old friends. The constant back and forth of “When are you free?” and “How about another day?” makes planning to meetup frustrating, and takes the joy away from meeting up old friends. We wanted a way to make meet-ups easy and seamless.


## What it does
whenmeetah? (@whenmeetah_bot) is a Telegram bot which can be integrated directly into group chats to /decidewhen to meet up. After selecting a timeframe, the user can select multiple dates to indicate availability. Our bot allows every member in the group chat to be fully aware of each other’s schedules. Use /answered to see who have indicated their availability and /done to generate the best available date. 

On the day itself, use /whereyall to enter the postal code of the meeting venue. Afterwhich, each user can use /eta to enter their current location and mode of transport to find out how long more before they reach the destination.


## How we built it
Using Telegram Bot API and the pyTelegramBotAPI library, we developed commands that we think would make finding a common time easier. We used different types of handlers: CommandHandlers, CallbackQueryHandlers and more. To make the bot interactive, we have also custom InlineKeyboards as our input method, and also come up with various responses for the uses. Integrating Google Maps Distance Matrix API, we have also developed a way to find out accurately the time needed for one to reach the destination based on their current location and their mode of transport.


## Challenges we ran into
Being the first time building a Telegram bot, there was some learning curve to understanding the API and documentation. It was also our first time calling an API service, and hence also took time and effort to familiarize with the Google Maps API. However, it all paid off when the final product was working. 


## Accomplishments that we're proud of
@whenmeetah_bot
Built a completed date-picker for an event.
Built a completed ETA-calculator for users.

## What we learned
Telegram Bot API
Google Maps API Integration


## What's next for whenmeetah?
We plan on expanding the date ranges by using a calendar widget to be able to select more dates, and include time/timeslots for each day to give the user more flexibility in planning meet-ups. We also are looking into improving the date selection method to provide more transparency as to who is available on which dates. Lastly, we plan on obtaining even more accurate results using the Google Maps API such as calling for ETA times with regards to live-time traffic conditions, and also to use the built-in geolocation service to obtain the current location of the user, in order to make sending locations easier.



