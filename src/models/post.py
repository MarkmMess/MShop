# from sqlalchemy import String, Text, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# # from .mixins import UserRelationMixin
#
# from .base import Base
#
#
# # class Post(UserRelationMixin, Base):
# class Post(Base):
#     _user_back_populates = "posts"
#     title: Mapped[str] = mapped_column(String(100))
#     body: Mapped[str] = mapped_column(
#         Text,
#         default="",
#         server_default="",
#     )
#
#
#
#     def __str__(self):
#         return f"{self.__class__.__name__}(id:{self.id}, title:{self.title!r}, user_id:{self.user_id!r})"
#
#     def __repr__(self):
#         return str(self)
