from flask import Flask , request , jsonify , make_response # , render_template as rt
from flask_sqlalchemy import SQLAlchemy
import uuid 
from werkzeug.security import generate_password_hash , check_password_hash
import jwt 
import datetime
from functools import wraps

app = Flask (__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model) : 
    id = db.Column(db.Integer , primary_key = True)
    public_id = db.Column(db.String(50) , unique =True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


def token_required(f) : 
    @wraps(f)
    def decorated(*args , **kwargs) : 
        token = None

        if ('x-access-token') in request.headers : 
            token = request.headers['x-access-token']
        
        if not token : 
            return jsonify ({"message" : "Token is missing"}) , 401
        
        try : 
            data = jwt.decode(token , app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id = data ["public_id"]).first()
        except : 
            return jsonify ({"message" : "Token is missing"}) , 401

        return f(current_user , *args , **kwargs)
    return decorated


@app.route('/user' , methods =['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin : 
        return jsonify({'message' : 'Cannot perform that function' })

    users = User.query.all()
    output = []
    for user in users : 
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>' , methods = ['GET'])
@token_required
def get_one_user(current_user , public_id) : 
    if not current_user.admin : 
        return jsonify({'message' : 'Cannot perform that function' })
    
    user = User.query.filter_by(public_id = public_id).first()
    
    if not user : 
        return jsonify({'message' : 'No user found !'  , 'user_name' :  data['name']})
    
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user' , methods = ['POST'])
@token_required
def creat_user(current_user) :
    if not current_user.admin : 
        return jsonify({'message' : 'Cannot perform that function' })

    data = request.get_json()
    
    

    hashed_password = generate_password_hash(data['password'] , method = 'sha256')

    new_user = User(public_id = str(uuid.uuid4()) , name = data['name'] , password = hashed_password , admin = False )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!' , 'user_name' :  data['name']  })

@app.route('/user/<public_id>' , methods = ['PUT'])
@token_required
def promote_user(current_user , public_id) : 

    if not current_user.admin : 
        return jsonify({'message' : 'Cannot perform that function' })

    user = User.query.filter_by(public_id = public_id).first()

    if not user : 
        return jsonify ({'message' : 'No user found!'})
    
    user.admin = True 
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'  , 'user_name' :  data['name'] })

@app.route('/user/<public_id>' , methods = ['DELETE'])
@token_required
def delete_user(current_user , public_id):
    
    if not current_user.admin : 
        return jsonify({'message' : 'Cannot perform that function' })
    
    user = User.query.filter_by(public_id = public_id).first()

    if not user : 
        return jsonify({'message' : 'No user found!'  , 'user_name' :  data['name']})
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'  , 'user_name' :  data['name']})

@app.route('/login')
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password : 
        return make_response('Could not verify' , 401 , {'WWW-Authenticate' : 'Basic realm ="Login required"'})
    
    user = User.query.filter_by (name = auth.username).first()

    if not user : 
        return make_response('Could not verify' , 401 , {'WWW-Authenticate' : 'Basic realm ="Login required"'})

    if check_password_hash (user.password , auth.password) : 
        token = jwt.encode({'public_id' : user.public_id , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)} , app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify' , 401 , {'WWW-Authenticate' : 'Basic realm ="Login required"'})



if __name__ == "__main__" :
    app.run(debug = True)  #runs on local host
    #app.run(host='0.0.0.0') #runs on local network
