from constante import SLACK_BOT_TOKEN, CHANNEL_ID, DATA_DIR, Socket_Token, WOODY_USER_ID
from outils import envoyer_hello_world, envoyer_tous_les_png, lancer_ecoute_wikipedia_socket_mode


# We run each step one after another, so the first is the Helle World

ts = envoyer_hello_world(SLACK_BOT_TOKEN, CHANNEL_ID)
print("Sent:", ts)

#The second is the Image sender 
n = envoyer_tous_les_png(SLACK_BOT_TOKEN, CHANNEL_ID, DATA_DIR)
print(f"{n} images envoyées")


# the third wait for Wikipedia message from Woody and reply fetching the first paragraph of the corresponding Wikipedia page
lancer_ecoute_wikipedia_socket_mode(
    bot_token=SLACK_BOT_TOKEN,
    app_token=Socket_Token,
    channel_id=CHANNEL_ID,
    woody_user_id=WOODY_USER_ID,
    lang="en",
)
