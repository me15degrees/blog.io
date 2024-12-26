import sqlite3
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('Downloads/githubio-35801-firebase-adminsdk-quwm5-85a8cb6612.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://githubio-35801-default-rtdb.firebaseio.com/'
})

conn = sqlite3.connect("likes.db")
cursor = conn.cursor()
cursor.execute("SELECT id, like_count FROM likes")
posts = cursor.fetchall()

ref = db.reference('posts')

for post in posts:
    post_id, like_count = post
    ref.child(str(post_id)).set({
        'like_count': like_count
    })

conn.close()
