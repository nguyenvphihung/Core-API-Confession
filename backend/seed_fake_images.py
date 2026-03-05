import random
from database import SessionLocal
from models import Post, PostMedia

def seed_fake_images():
    db = SessionLocal()
    try:
        posts = db.query(Post).all()
        print(f"Found {len(posts)} posts. Seeding images...")
        added_count = 0
        
        for post in posts:
            # Check if post already has media
            existing = db.query(PostMedia).filter(PostMedia.post_id == post.id).first()
            if existing:
                continue
                
            # Randomly decide to add an image (70% chance)
            if random.random() < 0.7:
                # Add 1 or 2 images
                num_images = random.randint(1, 2)
                for i in range(num_images):
                    seed = random.randint(1, 100000)
                    # Width 800, height between 400 and 800 for variety
                    height = random.randint(400, 800)
                    image_url = f"https://picsum.photos/seed/{seed}/800/{height}"
                    
                    new_media = PostMedia(
                        post_id=post.id,
                        file_url=image_url,
                        file_name=f"fake_image_{seed}.jpg",
                        file_size=random.randint(50000, 300000),
                        media_type="image",
                        mime_type="image/jpeg"
                    )
                    db.add(new_media)
                    added_count += 1
                    
        db.commit()
        print(f"Success! Added {added_count} fake images directly into DB.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding images: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_fake_images()
