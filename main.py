from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from users import users
from offers import offers
from orders import orders
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))



class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(50), unique=True)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))



class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))



def main():
    db.create_all()
    insert_data()

    app.run(debug=True)



def insert_data():
    new_users = []
    for user in users:
        new_users.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            )
        )
        with db.session.begin():
            db.session.add_all(new_users)

    new_orders = []
    for order in orders:
        new_orders.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
        )
        with db.session.begin():
            db.session.add_all(new_orders)

    new_offers = []
    for offer in offers:
        new_offers.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
        )
        with db.session.begin():
            db.session.add_all(new_offers)



@app.route('/users', methods=['GET', 'POST'])
def users_index():
    if request.method == 'GET':
        data = []
        for user in User.query.all():
            data.append(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'age': user.age,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone
                }
            )
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone']
        )
        db.session.add(new_user)
        db.session.commit()

        return '', 201



@app.route('/users/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def user_by_oid(oid):
    if request.method == 'GET':
        user = User.query.get(oid)
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        }

        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        user = User.query.get(oid)
        user.first_name = data['first_name'],
        user.last_name = data['last_name'],
        user.age = data['age'],
        user.email = data['email'],
        user.role = data['role'],
        user.phone = data['phone']

        db.session.add(user)
        db.session.commit()

        return '', 203

    elif request.method == 'DELETE':
        user = User.query.get(oid)
        db.session.delete(user)
        db.session.commit()



@app.route('/orders', methods=['GET', 'POST'])
def orders_index():
    if request.method == 'GET':
        data = []
        for order in Order.query.all():
            customer = User.query.get(order.customer_id).first_name if User.query.get(order.customer_id) else order.customer_id
            executor = User.query.get(order.executor_id).first_name if User.query.get(order.executor_id) else order.executor_id
            data.append(
                {
                    "id": order.id,
                    "name": order.name,
                    "description": order.description,
                    "start_date": order.start_date,
                    "end_date": order.end_date,
                    "address": order.address,
                    "price": order.price,
                    "customer_id": customer,
                    "executor_id": executor
                }
            )
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        new_order = Order(
            name=data['name'],
            description=data['description'],
            start_date=datetime.strptime(data['start_date'], '%m/%d/%Y'),
            end_date=datetime.strptime(data['end_date'], '%m/%d/%Y'),
            address=data['address'],
            price=data['price'],
            customer_id=data['customer_id'],
            executor_id=data['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()

        return '', 201



@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def order_by_oid(oid):
    if request.method == 'GET':
        order = Order.query.get(oid)
        data = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id
        }
        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        order = Order.query.get(oid)
        order.name = data['name'],
        order.description = data['description'],
        order.start_date = datetime.strptime(data['start_date'], '%m/%d/%Y'),
        order.end_date = datetime.strptime(data['end_date'], '%m/%d/%Y'),
        order.address = data['address'],
        order.price = data['price'],
        order.executor_id = data['executor_id']

        db.session.add(order)
        db.session.commit()

        return '', 203

    elif request.method == 'DELETE':
        order = Order.query.get(oid)
        db.session.delete(order)
        db.session.commit()



@app.route('/offers', methods=['GET', 'POST'])
def offers_index():
    if request.method == 'GET':
        data = []
        for offer in Offer.query.all():
            order = Order.query.get(offer.order_id).name if User.query.get(offer.order_id) else offer.order_id
            executor = User.query.get(offer.executor_id).first_name if User.query.get(offer.executor_id) else offer.executor_id
            data.append(
                {
                    'id': offer.id,
                    'order_id': order,
                    'executor_id': executor
                }
            )
        return jsonify(data)

    elif request.method == 'POST':
        data = request.get_json()
        new_offer = Offer(
            order_id=data['order_id'],
            executor_id=data['executor_id']
        )
        db.session.add(new_offer)
        db.session.commit()

        return '', 201



@app.route('/offers/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def offer_by_oid(oid):
    if request.method == 'GET':
        offer = Offer.query.get(oid)
        order = Order.query.get(offer.order_id).name if User.query.get(offer.order_id) else offer.order_id
        executor = User.query.get(offer.executor_id).first_name if User.query.get(offer.executor_id) else offer.executor_id
        data = {
            "id": offer.id,
            "order_id": order,
            "executor_id": executor
        }

        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        offer = Offer.query.get(oid)
        offer.order_id = data['order_id'],
        offer.executor_id = data['executor_id']

        db.session.add(offer)
        db.session.commit()

        return '', 203

    elif request.method == 'DELETE':
        offer = Offer.query.get(oid)
        db.session.delete(offer)
        db.session.commit()



if __name__ == '__main__':
    main()

