#!/usr/bin/env python3
import sqlite3
from sqlite3.dbapi2 import connect
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field should be filled"
        )

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # return {'item': item}, 200 if item else 404
        #------#
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return {'item': row[0], 'price': row[1]}
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': row[0], 'price': row[1]}

    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # data = Item.parser.parse_args()
        # item = {'name': name , 'price': data['price']}
        # items.append(item)
        # return item, 201
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = {
            'name': name,
            'price': data['price']
        }
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (item['name'], item['price']))

        # connection.commit()
        # connection.close()
        try:
            self.insert(item)
        except:
            return {"message": "An error occured"}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted succesfully'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted succesfully'}

    def put(self, name):
        # data = Item.parser.parse_args()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item
        data =Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_items = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_items)
            except:
                return {'message': 'Error occured while insertion'}, 500
        else:
            try:
                self.update(updated_items)
            except:
                return {'message': 'Error occured while updating'}, 500
        
        return updated_items

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    # def get(self):
    #     return {'items': items}
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
