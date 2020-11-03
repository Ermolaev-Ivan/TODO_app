from flask import Flask, request, jsonify
from peewee import SqliteDatabase, Model, TextField, DateTimeField, CharField
from flask_restplus import Resource, Api, fields
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard_secret_string"
api = Api(app)
ma = Marshmallow(app)
db = SqliteDatabase("task.db")


class Task(Model):
    class Meta:
        database = db

    title = CharField(max_length=150)
    content = TextField()
    create_at = DateTimeField(default=datetime.strftime(datetime.now(), '%d/%m/%Y  %H:%M:%S'))

# db.create_tables([Task])  # создание бд


class TaskListSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'create_at')


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'create_at')


schema_list = TaskListSchema(many=True)
schema_about = TaskSchema()


model = api.model('model', {'title': fields.String('Enter title'),
                            'content': fields.String('Enter content')})


@api.route('/api/task/')
class getlist_post(Resource):
    def get(self):
        return jsonify(schema_list.dump(Task.select()))

    @api.expect(model)
    def post(self):
        task = Task(title=request.json['title'], content=request.json['content'])
        task.save()
        return {'message': 'task created'}


@api.route('/api/task/<int:id>/')
class getabout_puttask_deletetask(Resource):
    def get(self, id):
        return jsonify(schema_about.dump(Task.get(id)))

    @api.expect(model)
    def put(self, id):
        task = Task.get(id)
        task.title = request.json['title']
        task.content = request.json['content']
        task.save()
        return {'message': 'task updated'}

    def delete(self,id):
        task = Task.get(id)
        task.delete_instance()
        return {'message': 'task deleted'}


if __name__ == '__main__':
    app.run()