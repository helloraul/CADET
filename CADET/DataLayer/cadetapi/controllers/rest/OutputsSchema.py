""" These classes define the return values from the appropriate API calls.
    Marshmellow is used to serialize/deserialize the data between json and
    other python objects.
    More information can be found below:
    https://marshmallow.readthedocs.io/en/latest/
"""

from marshmellow import Schema, fields


class MetaSchema(Schema):
    doc_id = fields.Integer()
    topics = fields.Integer()
    iterations = fields.Integer()
    words_per_topic = fields.Integer()

class TopicsSchema(Schema):
    topic_id = fields.Integer()
    positive = fields.List(fields.String())
    neutral  = fields.List(fields.String())
    negative = fields.List(fields.String())

class RatingsSchema(Schema):
    course_sect = fields.String()
    instr_first = fields.String()
    instr_last  = fields.String()
    positive = fields.List(fields.String())
    neutral  = fields.List(fields.String())
    negative = fields.List(fields.String())

class ResultsSchema(Schema):
    meta = fields.Nested(MetaSchema)
    topic_stats = fields.Nested(TopicsSchema)
    instructor_stats = fields.Nested(RatingSchema)
