import pytest
from src import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    posts_map = map(lambda post: schemas.Post(**post), res.json())
    posts_list = list(posts_map)
    
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)
    assert posts_list[0].id == test_posts[0].id
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    
    assert res.status_code == 200
    
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 200
    
def test_get_unexistent_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888888")
    
    assert res.status_code == 404
    
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.Post(**res.json())
    
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title
    assert post.category == test_posts[0].category
    assert post.tags == test_posts[0].tags
    
@pytest.mark.parametrize("title, content, category, tags", [
    ("awesome new title", "awesome new content", "Technology", ["Tech", "Programming"]),
    ("favourite pizza", "I love pepperoni", "Food", ["Pizza", "Cooking"]),
    ("tallest skyscrapers", "wahoo", "Travel", ["City", "Architecture"]),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, category, tags):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "category": category, "tags": tags})
    
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.category == category
    assert created_post.tags == tags
    assert created_post.owner_id == test_user['id']
    
def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title": "title", "content": "content", "category": "category", "tags": ["tag1", "tag2"]})
    
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204
    
def test_delete_non_existent_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/8888888888888")
    
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    
    assert res.status_code == 403
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "category": "updated category",
        "tags": ["tag3", "tag4"],
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.category == data['category']
    assert updated_post.tags == data['tags']
    
def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "category": "updated category",
        "tags": ["tag3", "tag4"],
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    
    assert res.status_code == 403
    
def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401
    
def test_update_non_existent_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "category": "updated category",
        "tags": ["tag3", "tag4"],
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/8888888888888", json=data)
    
    assert res.status_code == 404
    
def test_get_posts_with_search(authorized_client, test_posts):
    res = authorized_client.get("/posts/?term=Technology")
    
    assert res.status_code == 200
    assert len(res.json()) == 3  # 3 posts have Technology category

def test_get_posts_with_limit(authorized_client, test_posts):
    res = authorized_client.get("/posts/?limit=2")
    
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_get_posts_with_skip(authorized_client, test_posts):
    res = authorized_client.get("/posts/?skip=3")
    
    assert res.status_code == 200
    assert len(res.json()) == 1  # 4 posts total, skip 3