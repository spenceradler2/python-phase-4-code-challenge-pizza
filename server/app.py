#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class RestaurantsResource(Resource):
    def get(self):
        restaurants = [restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in Restaurant.query.all()]
        return make_response(restaurants, 200)
    
api.add_resource(RestaurantsResource, "/restaurants", endpoint="restaurants")
  
class RestaurantResource(Resource):
    def get(self,id):
        restaurant_id = Restaurant.query.filter_by(id=id).first()
        if restaurant_id:
            response = restaurant_id.to_dict()
            return make_response(response, 200)
        else:
            response = {"error": "Restaurant not found"}
            return make_response(response, 404)
        
    def delete(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({}, 204)
        else:
            response = {"error": "Restaurant not found"}
            return make_response(response, 404)

api.add_resource(RestaurantResource, "/restaurants/<int:id>", endpoint="restaurant")  
       
class PizzasResource(Resource):
    def get(self):
        pizzas = [pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in Pizza.query.all()]
        return make_response(pizzas, 200)
    
api.add_resource(PizzasResource, "/pizzas", endpoint="pizzas")

class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")
        try:
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()
            return make_response(restaurant_pizza.to_dict(), 201)
        except:
            response = {"errors": ['validation errors']}
            return make_response(response, 400)




        # new_restaurant_pizza = RestaurantPizza(
        #     price=request.form['price'],
        #     pizza_id=request.form['pizza_id'],
        #     restaurant_id=request.form['restaurant_id'],
        # )

        # if new_restaurant_pizza:
            
        #     db.session.add(new_restaurant_pizza)
        #     db.session.commit()

        #     response_dict = new_restaurant_pizza.to_dict()
        #     response = make_response(
        #         response_dict,
        #         201,
        #     )
        #     return response
        # else:
        #     response = {"error": "Restaurant not found"}
        #     return make_response(response, 400)
        
        # 
    
api.add_resource(RestaurantPizzaResource, "/restaurant_pizzas", endpoint="restaurants_pizza")  #review path and endpoint

if __name__ == "__main__":
    app.run(port=5555, debug=True)
