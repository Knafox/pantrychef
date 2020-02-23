import json
import os
from database import DB
from identity import Identity
from user import User

# Everything outside of the handler is 'cached' on the virtual machine, connections should be here
# Initialize the DB connect
db = DB(database_name=os.environ['DB_NAME'], cluster_arn=os.environ['RDS_ARN'], secret_arn=os.environ['Secrets_ARN'])


def lambda_handler(event, context):
    print(event)

    # Safe defaults for return values
    u = None  # The user
    result = {}
    status_code = 200  # todo: make 201

    # Incoming payload from user
    payload = json.loads(event['body'])
    print(payload)

    ###
    # Grab data about person invoking the request TODO: refactor this out?
    ###
    ident = Identity(event)
    claim = ident.get_claim()
    if 'sub' in claim:
        print("User is actively logged in, their user ID (cognitoId) is:", claim['sub'])
        # Retrieve User Data for USER ID
        u = User(db, claim['sub'])
        u.retrieve_info()
    else:
        print("User token is expired, corrupted, we should exit/aka return out of the lambda early")
        return {
            'statusCode': 403,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(result)
        }

    ###
    # Actual Routing
    ###
    if event['resource'] == '/profiles':
        if event['httpMethod'] == 'GET':
            # Retrieve all profiles
            result = db.execute(
                sql="select * FROM `UserProfile` up JOIN `User` u on u.ID=up.UserId WHERE u.CognitoID=:cognitoId",
                parameters=[
                    {
                        'name': 'cognitoId',
                        'value': {
                            'stringValue': claim['sub']
                        }
                    }
                ]
            )
            # todo: parse info
        elif event['httpMethod'] == 'POST':
            # Create a profile
            print("Create a profile")
            transaction_id = db.begin_transaction()
            try:
                list1 = db.execute(
                    sql="INSERT INTO `IngredientList` (ListType) VALUES(:stuff)",
                    parameters=[{'name': 'stuff', 'value': {'stringValue': 'WhatGoesHere'}}],
                    transaction_id=transaction_id
                )
                list2 = db.execute(
                    sql="INSERT INTO `IngredientList` (ListType) VALUES(:stuff)",
                    parameters=[{'name': 'stuff', 'value': {'stringValue': 'WhatGoesHere'}}],
                    transaction_id=transaction_id
                )
                profile = db.execute(
                    sql="INSERT INTO `UserProfile` (ProfileName, UserID, DietType, PantryList, ShoppingList) VALUES(:profileName, :userId, :dietType, :pantryList, :shoppingList)",
                    parameters=[
                        {'name': 'profileName', 'value': {'stringValue': str(payload['name'])}},
                        {'name': 'userId', 'value': {'longValue': int(u.get_id())}},
                        {'name': 'dietType', 'value': {'longValue': int(1)}},  # Random number for now
                        {'name': 'pantryList', 'value': {'longValue': int(list1['generatedFields'][0]['longValue'])}},
                        {'name': 'shoppingList', 'value': {'longValue': int(list2['generatedFields'][0]['longValue'])}}
                    ],
                    transaction_id=transaction_id
                )
                print(profile)
                db.commit_transaction(transaction_id)
                result = profile
            except Exception as e:
                db.rollback_transaction(transaction_id)
                status_code = 500
                result = {'errorMessage': 'Could not save the profile.'}
                print(str(e))

    elif event['resource'] == '/profiles/{profileId}':
        result = {}
        print("Entered specific profile route")
        print("profile ID:", event['pathParameters']['profileId'])

    return {
        'statusCode': status_code,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(result)
    }
