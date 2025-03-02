import logging
from sqlalchemy.orm import Session
from app import models, schemas
from app.core import security

logger = logging.getLogger(__name__)


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    logger.info(f"Hashing password for user: {user.username}")
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User {user.username} created with ID: {db_user.id}")
    return db_user


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Article).offset(skip).limit(limit).all()


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    db_article = models.Article(**article.model_dump(), owner_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article: schemas.ArticleCreate, article_id: int):
    db_article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if db_article:
        db_article.title = article.title
        db_article.description = article.description
        db.commit()
        db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(
        models.Article.id == article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article
