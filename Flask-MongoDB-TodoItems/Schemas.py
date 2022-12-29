from marshmallow import Schema, fields, validate

class ToDoItemSchemaPost(Schema):
    title = fields.String(required=True, validate=validate.Length(min=5))
    description = fields.String(required=True, validate=validate.Length(min=5))

class ToDoItemSchemaPut(ToDoItemSchemaPost):
    complete = fields.Bool(required=True)

class ToDoItemsSchemaPatch(Schema):
    title = fields.String(required=False, validate=validate.Length(min=5))
    description = fields.String(required=False, validate=validate.Length(min=5))
    complete = fields.Bool(required=False)

