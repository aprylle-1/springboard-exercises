from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

#Making a bunch of users

#user(first_name[required], last_name[required], image_url=[nullable])
u1 = User(first_name="Aprylle", last_name="Ablaza")
u2 = User(first_name="Marlone", last_name="Gibalay")
u3 = User(first_name="Mark", last_name="Daquila")
u4 = User(first_name="Aldrin", last_name="Ablaza")
u5 = User(first_name="Allen", last_name="Santos")
u6 = User(first_name="Liz", last_name="Sabandal")

users = [u1, u2, u3, u4, u5, u6]

db.session.add_all(users)

db.session.commit()

#Making a bunch of posts
#post = title, content, user_id
post1u1 = Post(title="This is my first post", content="This is the content of my first post", user_id=1)
post2u1 = Post(title="This is my second post", content="This is the content of my second post", user_id=1)
post1u2 = Post(title="nkfgdshfsdhjkfdsfsd", content='fsdfhksfhjksdhfksd', user_id=2)

posts = [post1u1, post1u2, post2u1]

db.session.add_all(posts)

db.session.commit()