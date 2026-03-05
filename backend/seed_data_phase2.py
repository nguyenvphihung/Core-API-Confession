from faker import Faker
from database import SessionLocal
from models import User, Post, Comment, Interaction, CommentInteraction
from auth import hash_password
import random

fake = Faker()
db = SessionLocal()

def seed_data():
    print("Bắt đầu tạo dữ liệu giả...")

    # 1. Tạo 1000 Users (có display_name và email)
    users = []
    default_password = hash_password("password123")  # Hash 1 lần, dùng chung cho tất cả
    for _ in range(1000):
        users.append(User(
            student_id=str(fake.unique.random_number(digits=9, fix_len=True)),
            display_name=fake.name(),
            email=fake.unique.email(),
            password_hash=default_password
        ))

    db.bulk_save_objects(users)
    db.commit()
    print("Đã tạo xong 1.000 Users.")

    # Lấy ID của users vừa tạo
    user_ids = [u.id for u in db.query(User.id).all()]

    # 2. Tạo 5000 Posts
    posts = []
    for _ in range(5000):
        posts.append(Post(
            author_id=random.choice(user_ids),
            content=fake.text(max_nb_chars=200)
        ))

    db.bulk_save_objects(posts)
    db.commit()
    print("Đã tạo xong 5.000 Posts.")

    # Lấy ID của posts vừa tạo
    post_ids = [p.id for p in db.query(Post.id).all()]

    # 3. Tạo 20.000 Interactions (đảm bảo không trùng unique constraint)
    interaction_types = ['like', 'view']
    seen = set()
    interactions = []

    while len(interactions) < 20000:
        uid = random.choice(user_ids)
        pid = random.choice(post_ids)
        itype = random.choices(interaction_types, weights=[30, 70], k=1)[0]
        key = (uid, pid, itype)
        if key not in seen:
            seen.add(key)
            interactions.append(Interaction(user_id=uid, post_id=pid, interaction_type=itype))

    db.bulk_save_objects(interactions)
    db.commit()
    print(f"Đã tạo xong {len(interactions)} Interactions.")

    # 4. Tạo 3000 Comments (comment gốc, parent_id = NULL)
    comments = []
    for _ in range(3000):
        comments.append(Comment(
            user_id=random.choice(user_ids),
            post_id=random.choice(post_ids),
            content=fake.sentence(nb_words=15)
        ))

    db.bulk_save_objects(comments)
    db.commit()
    print("Đã tạo xong 3.000 Comments.")

    # Lấy ID của comments vừa tạo
    comment_ids = [c.id for c in db.query(Comment.id).all()]

    # 5. Tạo 1000 Replies (comment trả lời, có parent_id)
    replies = []
    for _ in range(1000):
        parent = random.choice(comment_ids)
        # Reply cùng post với comment cha
        parent_post = db.query(Comment.post_id).filter(Comment.id == parent).scalar()
        replies.append(Comment(
            user_id=random.choice(user_ids),
            post_id=parent_post,
            parent_id=parent,
            content=fake.sentence(nb_words=10)
        ))

    db.bulk_save_objects(replies)
    db.commit()
    print("Đã tạo xong 1.000 Replies.")

    # Cập nhật lại danh sách comment_ids (bao gồm cả replies)
    comment_ids = [c.id for c in db.query(Comment.id).all()]

    # 6. Tạo 5000 CommentInteractions (đảm bảo không trùng unique constraint)
    comment_interaction_types = ['like', 'dislike']
    seen_ci = set()
    comment_interactions = []

    while len(comment_interactions) < 5000:
        uid = random.choice(user_ids)
        cid = random.choice(comment_ids)
        itype = random.choices(comment_interaction_types, weights=[70, 30], k=1)[0]
        key = (uid, cid, itype)
        if key not in seen_ci:
            seen_ci.add(key)
            comment_interactions.append(CommentInteraction(user_id=uid, comment_id=cid, interaction_type=itype))

    db.bulk_save_objects(comment_interactions)
    db.commit()
    print(f"Đã tạo xong {len(comment_interactions)} CommentInteractions.")
    print("Hoàn tất bơm dữ liệu!")

if __name__ == "__main__":
    seed_data()