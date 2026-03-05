from faker import Faker
from database import SessionLocal
from models import User, Post, Comment, Interaction, CommentInteraction
import random

fake = Faker()
db = SessionLocal()

def seed_data():
    print("Bắt đầu tạo dữ liệu giả...")

    # 1. Tạo 5 Users (có display_name và email)
    users = []
    for _ in range(5):
        users.append(User(
            student_id=str(fake.unique.random_number(digits=9, fix_len=True)),
            display_name=fake.name(),
            email=fake.unique.email()
        ))

    db.bulk_save_objects(users)
    db.commit()
    print("Đã tạo xong 5 Users.")

    # Lấy ID của users vừa tạo
    user_ids = [u.id for u in db.query(User.id).all()]

    # 2. Tạo 15 Posts
    posts = []
    for _ in range(15):
        posts.append(Post(
            author_id=random.choice(user_ids),
            content=fake.text(max_nb_chars=200)
        ))

    db.bulk_save_objects(posts)
    db.commit()
    print("Đã tạo xong 15 Posts.")

    # Lấy ID của posts vừa tạo
    post_ids = [p.id for p in db.query(Post.id).all()]

    # 3. Tạo 30 Interactions (đảm bảo không trùng unique constraint)
    interaction_types = ['like', 'view']
    all_combinations = [
        (uid, pid, itype)
        for uid in user_ids
        for pid in post_ids
        for itype in interaction_types
    ]
    selected = random.sample(all_combinations, min(30, len(all_combinations)))

    interactions = [
        Interaction(user_id=uid, post_id=pid, interaction_type=itype)
        for uid, pid, itype in selected
    ]

    db.bulk_save_objects(interactions)
    db.commit()
    print(f"Đã tạo xong {len(interactions)} Interactions.")

    # 4. Tạo 20 Comments (comment gốc, parent_id = NULL)
    comments = []
    for _ in range(20):
        comments.append(Comment(
            user_id=random.choice(user_ids),
            post_id=random.choice(post_ids),
            content=fake.sentence(nb_words=15)
        ))

    db.bulk_save_objects(comments)
    db.commit()
    print("Đã tạo xong 20 Comments.")

    # Lấy ID của comments vừa tạo
    comment_ids = [c.id for c in db.query(Comment.id).all()]

    # 5. Tạo 10 Replies (comment trả lời, có parent_id)
    replies = []
    for _ in range(10):
        parent = random.choice(comment_ids)
        # Reply phải cùng post với comment cha
        parent_post = db.query(Comment.post_id).filter(Comment.id == parent).scalar()
        replies.append(Comment(
            user_id=random.choice(user_ids),
            post_id=parent_post,
            parent_id=parent,
            content=fake.sentence(nb_words=10)
        ))

    db.bulk_save_objects(replies)
    db.commit()
    print("Đã tạo xong 10 Replies.")

    # Cập nhật lại danh sách comment_ids (bao gồm cả replies)
    comment_ids = [c.id for c in db.query(Comment.id).all()]

    # 6. Tạo 15 CommentInteractions (đảm bảo không trùng unique constraint)
    comment_interaction_types = ['like', 'dislike']
    all_ci_combinations = [
        (uid, cid, itype)
        for uid in user_ids
        for cid in comment_ids
        for itype in comment_interaction_types
    ]
    selected_ci = random.sample(all_ci_combinations, min(15, len(all_ci_combinations)))

    comment_interactions = [
        CommentInteraction(user_id=uid, comment_id=cid, interaction_type=itype)
        for uid, cid, itype in selected_ci
    ]

    db.bulk_save_objects(comment_interactions)
    db.commit()
    print(f"Đã tạo xong {len(comment_interactions)} CommentInteractions.")
    print("Hoàn tất bơm dữ liệu!")

if __name__ == "__main__":
    seed_data()