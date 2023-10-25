# Django chat app

A simple chat app in Django using channels.

```
## database migration
python manage.py makemigrations
python manage.py migrate


## start Redis container
docker run --name my-redis -p 6379:6379 -d redis

## run the app
python manage.py runserver
```

The app will be available at http://localhost:8000/.

## Access the Chat App

Open a web browser and navigate to http://localhost:8000/ to access the chat app. You can start chatting with other users in real-time.

## Troubleshooting
If you encounter any issues, here are some common fixes:

Ensure you have Python and Django installed in your environment.

Check that Docker is installed and the Redis container is running as described in the README.

Verify that you have the necessary Python packages installed, especially Django and Channels. You can use pip to install them:

```
pip install django channels

```

Make sure your settings.py is correctly configured, including the CHANNEL_LAYERS settings for Channels.

If you face specific errors or issues, refer to the official documentation and online resources for troubleshooting and solutions.

Enjoy chatting with your friends using the Django Chat App!
