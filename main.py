from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select


# User 
class UserBase(SQLModel):
    username: str = Field(index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password: str


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    password: str | None = None
    password: str | None = None


# Post
class PostBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    text: str

    user_id: int | None = Field(default=None, foreign_key="user.id")


class Post(PostBase, table=True):
    pass


class PostPublic(PostBase):
    pass


class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    title: str | None = None
    text: str | None = None
    user_id: int | None = None


# Comment
class CommentBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    text: str

    user_id: int | None = Field(default=None, foreign_key="user.id")
    post_id: int | None = Field(default=None, foreign_key="post.id")


class Comment(CommentBase, table=True):
    pass


class CommentPublic(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    title: str | None = None
    text: str | None = None
    user_id: int | None = None
    post_id: int | None = None


# setup DB
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# User API

@app.post("/login", response_model=UserPublic)
def login(user: User):
    if user.username == "test" and user.password == "1234":
        return {"login": "ok"}
    return JSONResponse(status_code=401, content={"status": "error"})


@app.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserPublic])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: SessionDep):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="user not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

# Post API

@app.post("/posts/", response_model=PostPublic)
def create_post(post: PostCreate, session: SessionDep):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.get("/posts/", response_model=list[PostPublic])
def read_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    posts = session.exec(select(Post).offset(offset).limit(limit)).all()
    return posts


@app.get("/posts/{post_id}", response_model=PostPublic)
def read_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@app.patch("/posts/{post_id}", response_model=PostPublic)
def update_post(post_id: int, post: PostUpdate, session: SessionDep):
    post_db = session.get(Post, post_id)
    if not post_db:
        raise HTTPException(status_code=404, detail="post not found")
    post_data = post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_data)
    session.add(post_db)
    session.commit()
    session.refresh(post_db)
    return post_db


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, session: SessionDep):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    session.delete(post)
    session.commit()
    return {"ok": True}


# Comment API

@app.post("/comments/", response_model=CommentPublic)
def create_comment(comment: CommentCreate, session: SessionDep):
    db_comment = Comment.model_validate(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


@app.get("/comments/", response_model=list[CommentPublic])
def read_comments(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
    return comments


@app.get("/comments/{comment_id}", response_model=CommentPublic)
def read_comment(comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


@app.patch("/comments/{comment_id}", response_model=CommentPublic)
def update_comment(comment_id: int, comment: CommentUpdate, session: SessionDep):
    comment_db = session.get(Comment, comment_id)
    if not comment_db:
        raise HTTPException(status_code=404, detail="comment not found")
    comment_data = comment.model_dump(exclude_unset=True)
    comment_db.sqlmodel_update(comment_data)
    session.add(comment_db)
    session.commit()
    session.refresh(comment_db)
    return comment_db


@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    session.delete(comment)
    session.commit()
    return {"ok": True}