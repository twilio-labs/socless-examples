import slack, os
from socless import socless_bootstrap

SOCLESS_BOT_TOKEN = os.environ.get('SOCLESS_BOT_TOKEN')
sc = slack.WebClient(token=SOCLESS_BOT_TOKEN)

def find_user(name, page_limit=1000, include_locale='false'):
    """
    Find a user's Slack profile based on their full or display name
    """
    paginate = True
    next_cursor = ''
    while paginate:
        resp = sc.users_list(cursor=next_cursor, limit=page_limit, include_locale=include_locale)
        data = resp.data
        next_cursor = resp.data['response_metadata'].get('next_cursor','')
        if not next_cursor:
            paginate = False

        for user in data['members']:
            user_names = [user.get('name'), user.get('real_name'), user.get('profile',{}).get('real_name')]
            if name in user_names:
                return {"found":True, "user": user}

    return {"found": False}


def handle_state(context, target, target_type, message_template):
    """
    Send a Slack message to either a user or channel
    """
    target_id = ''
    # Determine Slack ID for the target
    if target_type == 'user':
        result = find_user(target)
        if result['found'] == False:
            raise Exception(f"User {target} not found in Slack instance")

        target_id = result['user']['id']
    else:
        target_id = f"#{target}"

    # Render the message template and send the message
    message = message_template
    resp = sc.chat_postMessage(channel=target_id, text=message, as_user=True)
    return resp.data

def lambda_handler(event,lambda_context):
    return socless_bootstrap(event,lambda_context,handle_state, include_event=True)
