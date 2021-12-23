def lambda_handler(event, handler):
    return 'Hello {} {}'.format(event['first_name'], event['last_name'])