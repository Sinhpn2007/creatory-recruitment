from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import (
    Integer, String, DateTime, Text,
    ForeignKey, text, func, and_
)
import os

from datetime import timedelta, datetime
from flask import jsonify
from marshmallow import Schema, fields, pprint
backend_path = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(backend_path, "db.sqlite3")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_path}"
db = SQLAlchemy(app)

class ChannelSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class MeasurementSchema(Schema):
    id = fields.Int(dump_only=True)
    dayname = fields.Str()
    measurement_date = fields.DateTime()

class VideoSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    # about fields
    # https://marshmallow.readthedocs.io/en/latest/api_reference.html#marshmallow.fields.List
    create_date = fields.DateTime()
    channel = fields.Nested(ChannelSchema)
    measurements = fields.Nested(MeasurementSchema, many=True)

class VideoMeasurement(db.Model):
    __tablename__ = 'video_measurement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('video.id', ondelete="CASCADE"))
    video = relationship("Video", back_populates="measurements")
    measurement_date = Column(DateTime())
    sub_count = Column(Integer, server_default=text("0"))
    comments = Column(Integer, server_default=text("0"))
    subscribersgained = Column(Integer, server_default=text("0"))
    subscriberslost = Column(Integer, server_default=text("0"))
    unsub_views = Column(Integer, server_default=text("0"))
    unsub_likes = Column(Integer, server_default=text("0"))
    unsub_dislikes = Column(Integer, server_default=text("0"))
    unsub_shares = Column(Integer, server_default=text("0"))


class Video(db.Model):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, autoincrement=True)
    youtube_id = Column(String(128))
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship("Channel", back_populates="videos")
    create_date = Column(DateTime())
    title = Column(String(128))
    description = Column(Text())
    duration = Column(Integer)
    measurements = relationship(
        "VideoMeasurement", cascade="all,delete",
        back_populates="video", passive_deletes=True)


class Channel(db.Model):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    videos = relationship("Video")


@app.route('/results', methods=['GET'])
def results():
    list_video = db.session.query(Video).join(VideoMeasurement).filter(VideoMeasurement.measurement_date >= Video.create_date + timedelta(days=2)).all()
    print(list_video)

    full_schema = VideoSchema(many=True)
    result = full_schema.dump(list_video)
    print(result)
    return jsonify({"list_video": result})

if __name__ == '__main__':
    app.run()