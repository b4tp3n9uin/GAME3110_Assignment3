import json
import boto3
dynamodb = boto3.resource('dynamodb')


# player varification function
# return the player if found
def Varification(UserName):
    UserTable = dynamodb.Table('Players')
    
    TargetUser = UserTable.get_item(
        Key={'user_id': UserName}
    )
    
    return 'Item' in TargetUser


def UpdateWin(UserName):
    UserTable = dynamodb.Table('Players')
    
    # pull player row from table
    TargetUser = UserTable.get_item(
        Key = {
            'user_id': UserName
        }
    )
    
    
    # get player info from db
    PlayerRow = TargetUser['Item']
    matches = PlayerRow['matches']
    loss = PlayerRow['loss']
    wins = PlayerRow['wins']
    
    # update user info
    matches += 1
    wins += 1
    
    
    
    # push to database table
    UserTable.put_item(
        Item = {
            'user_id': UserName,
            'matches': matches,
            'loss': loss,
            'wins': wins
        }
    )


def UpdateLost(UserName):
    UserTable = dynamodb.Table('Players')
    
    # pull player row from table
    TargetUser = UserTable.get_item(
        Key = {
            'user_id': UserName
        }
    )
    
    # get player info from db
    PlayerRow = TargetUser['Item']
    matches = PlayerRow['matches']
    loss = PlayerRow['loss']
    wins = PlayerRow['wins']
    
    # update user info
    matches += 1
    loss += 1
    
    
    
    # push to database table
    UserTable.put_item(
        Item = {
            'user_id': UserName,
            'matches': matches,
            'loss': loss,
            'wins': wins
        }
    )






# main
def lambda_handler(event, context):
    
    # user info
    Parameters = event['queryStringParameters']
    # Parameters = {'user_id': 'sdfasdfasdfasdfasdf', 'lost': 'true'}
    
    # get player ID
    UserID = Parameters['user_id']
    
    # if player exist, update the player
    if Varification(UserID):
        for i in Parameters:
            if i == 'win':
                UpdateWin(UserID)
                # return 200
                return {
                    'statusCode': 200,
                    'body': json.dumps('Win player info updated!')
                }
                
            if i == 'lost':
                UpdateLost(UserID)
                # return 200
                return {
                    'statusCode': 200,
                    'body': json.dumps('Lost player info updated!')
                }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('No Player Found')
        }
    

