import logging

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import exceptions

cred = credentials.Certificate("I:\Projects\discord-bot\cryptobot-32178-firebase-adminsdk-at1nj-0a324079c1.json")
app = firebase_admin.initialize_app(cred)

db = firestore.AsyncClient(credentials=app.credential.get_credential(), project=app.project_id)

'''
To add/manage data:
- Add data:                      https://firebase.google.com/docs/firestore/manage-data/add-data
- Transactions & batched writes: https://firebase.google.com/docs/firestore/manage-data/transactions
- Delete data:                   https://firebase.google.com/docs/firestore/manage-data/delete-data

To read data:
- Get data:                      https://firebase.google.com/docs/firestore/query-data/get-data
- Simple & compound queries:     https://firebase.google.com/docs/firestore/query-data/queries
- Order & limit data:            https://firebase.google.com/docs/firestore/query-data/order-limit-data
'''


async def add_data(collection, document, data):
    try:
        await db.collection(collection).document(document).set(data)
    except exceptions.FirebaseError as fire:
        print("FirebaseError: ", fire)


async def get_support_data(collection, userid=None):
    res = []
    try:
        docs = db.collection(collection).stream()
        async for doc in docs:
            if userid:
                if int(doc.id.split('_')[0]) == userid:
                    res.append(doc.to_dict())
            else:
                res.append(doc.to_dict())
    except exceptions.FirebaseError as fire:
        print("FirebaseError: ", fire)
    finally:
        return res


def get_exchange_data(collection, userid):
    try:
        docs = db.collection(collection).stream()
        for doc in docs:
            if int(doc.id) == userid:
                return doc.to_dict()
    except exceptions.FirebaseError as fire:
        print("FirebaseError: ", fire)
    return None
