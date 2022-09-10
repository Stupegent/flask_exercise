from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
import enum


app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class CategoryChoices(enum.Enum):
    Chaussures = "Chaussures"
    Vehicule = "Véhicule"
    Telephonie = "Téléphonie"
    Electromenager = "Electroménager"


class ProductModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(225), nullable=False)
	category = db.Column(db.Enum(CategoryChoices,
					        values_callable=lambda x: [str(ctg.value) for ctg in CategoryChoices]),
						 	nullable=False)
	quantity = db.Column(db.Integer,db.CheckConstraint('quantity>0'), nullable=False)

	def __init__(self,name,description,category,quantity):
		self.name = name
		self.description = description
		self.category = category
		self.quantity = quantity

	def __repr__(self):
		return f"Product( name = {self.name}, description = {self.description}, category = {self.category} , quantity = {self.quantity})"



@app.route("/product/<int:prod_id>/",methods = ["GET"])
def read_prod(prod_id):
	print(prod_id)
	if request.method == "GET":
		res = ProductModel.query.get_or_404(prod_id)
		print(res.category)
		ser = {
			"id" : res.id,
			"name":res.name,
			"description":res.description,
			"category":res.category.value,
			"quantity": res.quantity
			}
		return jsonify(ser)
	return "<h1> please send a get method </h1>"


switcher = {
	"Chaussures":1,
    "Véhicule":2,
    "Téléphonie":3,
    "Electroménager":4
}



@app.route("/",methods = ["POST"])
def create_prod():

	if request.method == "POST":
		if switcher.get(request.args["category"],None):
			try:
				prod = ProductModel(name = request.args["name"],description = request.args["description"]
								,category = request.args["category"],quantity = request.args["quantity"])
				db.session.add(prod)
				db.session.commit()
				return f"{prod} have been added succefully."
			except:
				return "QUANTITY_ERROR : please enter a positive quantity number"
		else : return str("please select one of these categories : Chaussures | Véhicule | Téléphonie | Electroménager ")
		
		
		return "",201

	print(request.args)
	return "Please use a Post method"





@app.route("/product/<int:prod_id>/update",methods = ["PUT"])
def update_prod(prod_id):
	print("salem")
	if request.method == "PUT":
		print(prod_id)
		result = ProductModel.query.get_or_404(prod_id)
		print("salem")
		if request.args['name']:
			result.name = request.args['name']
		if request.args['description']:
			result.description = request.args['description']
		if switcher.get(request.args["category"],None):
			result.category = request.args['category']
		else : return str("please select one of these categories : Chaussures | Véhicule | Téléphonie | Electroménager ")
		if request.args['quantity']:
			try:
				result.quantity = request.args['quantity']
				db.session.commit()
				return "updated"
			except:
				return "QUANTITY_ERROR : please enter a positive quantity number"
		db.session.commit()
		return "updated"
		

	print(request.args)
	return "<h1> SALAM 2 </h1>"



@app.route("/product/<int:prod_id>/delete/", methods=["DELETE"])
def delete_prod(prod_id):
	if request.method == "DELETE":
		result = ProductModel.query.get_or_404(prod_id)
		db.session.delete(result)
		db.session.commit()
		return f"Status 204 :product has been deletd succesfully"
	else : 
		return str("please use the delete method")




if __name__ == "__main__":
	app.run(debug=True)