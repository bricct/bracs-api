from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative.api import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import Column, DECIMAL, Date, DateTime, Float, ForeignKey, Index, JSON, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TINYINT
from app.utils import load_app_config


#from app.utils.api_imports import *
Base = declarative_base()


class User(Base):
  __tablename__ = "user"
  id = Column(INTEGER, primary_key=True)
  username = Column(VARCHAR(64), unique=True, nullable=False)
  email = Column(VARCHAR(256), unique=True, nullable=False)
  phone = Column(VARCHAR(64), unique=True, nullable=True)
  password = Column(VARCHAR(1024), nullable=False)
  isAdmin = Column(TINYINT, nullable=False, server_default=text('0'))
  createdAt = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
  updatedAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Token(Base):
  __tablename__ = "token"
  id = Column(INTEGER, primary_key=True)
  userID = Column(INTEGER, ForeignKey("user.id"), nullable=False)
  token = Column(VARCHAR(256), nullable=False)
  createdAt = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
  updatedAt = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

