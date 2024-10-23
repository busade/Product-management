from flask_restx import Namespace, Resource,fields, abort
from ..model import Products
from flask import request, jsonify
from http import HTTPStatus
from ..utils import db
from werkzeug.exceptions import NotFound



crud_namespace= Namespace("prod", description="namespace for crud operation")

crud_model = crud_namespace.model(
    "Prod",{
        "id": fields.Integer(description="Product Id"),
        "name": fields.String(decription = "Name of Product"),
        "info": fields.String(description="Products information"),
        "date_added":fields.DateTime(description="Date product was added"),
        "quantity":fields.Integer(description="Products quantity"),



    }
)
crud_expected_model= crud_namespace.model(
    "Prod",{
        "name":fields.String(description= "Name of Product"),
        "info":fields.String(description= "Poducts information"),
        "quantity": fields.Integer(description="Quantity of products" )

    }
)

@crud_namespace.route('/product')
class Create(Resource):
    @crud_namespace.expect(crud_expected_model)
    @crud_namespace.marshal_with(crud_model)
    @crud_namespace.doc(description="This route is for adding a new product")
    def post(self):

        """create a new product"""
        data= request.get_json()
        existence_check = Products.query.filter_by(name=data.get('name')).first()
        if existence_check:
            abort(HTTPStatus.CONFLICT, f"Product with name '{data.get('name')}' already exists.")

        new_product = Products(
            name=data.get("name"),
            info = data.get("info"),
            quantity= data.get("quantity")
        )
        new_product.save()
        return new_product,HTTPStatus.CREATED
    


    @crud_namespace.marshal_with(crud_model)  
    @crud_namespace.doc(description="This is for adding a retrieving all products")
    def get (self):
        """Get all products"""
        products= Products.query.all()
        return products, HTTPStatus.OK

   
@crud_namespace.route("/products/<int:id>")
class GetUpdateDelete(Resource):

    @crud_namespace.marshal_with(crud_model)
    @crud_namespace.doc(description="This retrieves a particular product by id")
    def get(self, id):
        """retrieve a product by id"""
        product = Products.get_by_id(id)
        if product:
            return product, HTTPStatus.OK
        return (HTTPStatus.NOT_FOUND, f"Product with {id}' does not exists.")

    @crud_namespace.expect(crud_expected_model)
    @crud_namespace.marshal_with(crud_model)
    @crud_namespace.doc(description="This updates a particular product by id ")
    def put (self, id):
        """update a product by id """
        product_to_update = Products.get_by_id(id)
        if not product_to_update:
            return {"message":f"product with the id {id} not found"}, HTTPStatus.NOT_FOUND
        data= request.get_json()
        if 'name' in data:
            product_to_update.name= data['name']
        if 'quantity' in data:
            product_to_update.quantity= data['quantity']
        if 'info' in data:
            product_to_update.info = data['info']

        db.session.commit()
        return product_to_update, HTTPStatus.ACCEPTED

    @crud_namespace.doc(description="This deletes a particular product by id")
    def delete(self, id):
        """Delete a product by ID."""
        product_to_delete = Products.get_by_id(id)
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
            return {"message": f"Product with ID {id} has been deleted."}, HTTPStatus.ACCEPTED
        
        abort(HTTPStatus.NOT_FOUND, f"Product with ID {id} does not exist.")
    # @crud_namespace.errorhandler(NotFound)
    # def handle_not_found(e):
    #     response = jsonify({"message": str(e)})
    #     response.status_code = 404
    #     return response