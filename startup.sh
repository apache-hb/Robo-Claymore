cd source/

# run the backend web api
screen -S ClaymoreAPI -dm bash -c "cd api;gradle run"

# run the frontend web server
screen -S ClaymoreWeb -dm bash -c "cd web;npm run build"

# startup lavalink
screen -S ClaymoreLava -dm bash -c "cd lavalink;java -jar Lavalink.jar"

# then run the discord bot
screen -S ClaymoreBot -dm bash -c "cd bot;python3.7 main.py"