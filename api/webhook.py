from http import HTTPStatus
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def handler(request, context):
    if request.method != 'POST':
        return {
            'statusCode': HTTPStatus.METHOD_NOT_ALLOWED.value,
            'body': json.dumps({'message': 'Method Not Allowed'})
        }

    try:
        data = json.loads(request.get_data())
        name = data.get('name')
        suggestion = data.get('suggestion')

        if not name or not suggestion:
            return {
                'statusCode': HTTPStatus.BAD_REQUEST.value,
                'body': json.dumps({'message': 'Missing name or suggestion'})
            }

        discord_webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'
        discord_user_id = 'YOUR_DISCORD_USER_ID'

        webhook = DiscordWebhook(url=discord_webhook_url)
        embed = DiscordEmbed(title='New Suggestion', color='03b2f8')
        embed.add_embed_field(name='Name:', value=name)
        embed.add_embed_field(name='Suggestion:', value=suggestion)
        webhook.content = f'<@{discord_user_id}> You have a new suggestion!'
        webhook.add_embed(embed)
        webhook.execute()

        # Correct way to add CORS headers:
        response = {
            'statusCode': HTTPStatus.OK.value,
            'body': json.dumps({'message': 'Suggestion sent!'})
        }
        response['headers'] = {
            'Access-Control-Allow-Origin': 'https://webpagescript.vercel.app', # Your GitHub Pages domain
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
        return response

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR.value,
            'body': json.dumps({'message': 'Error sending suggestion'})
        }
