from sql import create_connection, execute_query
import mysql.connector
from flask import jsonify, request, make_response, render_template, session, redirect
from datetime import datetime
from flask import redirect, url_for
from flask import send_from_directory
from mysql.connector import Error
import flask
import random
import uuid





def create_connection(host_name,user_name,user_password,db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
            )
        print('Connect to MySql DB successful')
    except Error as e:
        print(f"The error '{e}' has occured")
    return connection
conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'intersteller')

def execute_query(conn, query, fetch=True):
    cursor = conn.cursor()
    cursor.execute(query)
    if fetch:
        result = cursor.fetchall()
        return result
    else:
        conn.commit()




app = flask.Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def execute_query(connection, query):
    cursor = connection.cursor(dictionary=True)  # Add dictionary=True for MySQL Connector
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        print("Query executed successfully")
        return result
    except Error as e:
        print(f"The error '{e}' has occured")
        return None


@app.route('/cargo', methods=['GET'])
def cargo():
    return render_template('cargo.html')

@app.route('/captain', methods=['GET'])
def captain():
    return render_template('captain.html')

@app.route('/spaceship', methods=['GET'])
def spaceship():
    return render_template('spaceship.html')

@app.route('/api/cargo', methods=['GET'])
def get_all_cargo():
    conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'intersteller')
    cargos = []
    sql_select = "SELECT * FROM cargo"
    cargos_ = execute_query(conn, sql_select)  # Change this line
    for item in cargos_:
        cargos.append({
            'cargotype': item['cargotype'],
            'weight': item['weight'],
            'shipid': item['shipid']  # Add this line to include shipid

        })
    return jsonify(cargos)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Raahima' and password == 'password':
            session['username'] = username
            return redirect('/home')
        else:
            error_message = 'Invalid username or password'
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        cargos = []
        sql_select = "SELECT * FROM cargo"
        cargos_ = execute_query(conn, sql_select)  # Change this line
        for item in cargos_:
            cargos.append({
                'cargotype': item['cargotype'],
                'weight': item['weight'],
                'shipid': item['shipid']  # Add this line to include shipid
            })

        return render_template('home.html', username=session['username'], cargos=cargos)
    else:
        return redirect('/login')




###############CRUD ROUTES#################

@app.route('/api/cargo',methods=['GET'])  #Can be tested by using link like this: http://127.0.0.1:5000/api/cargo?id=[ID of your choosing]
def get_cargo_id():
    cargos = [] #Houses the SQL results
    sql_select = "SELECT * FROM cargo" #SQL command to get all cargo
    cargos_ = execute_query(conn,sql_select) #Executes SQL
    for items in cargos_:
        cargos.append(items) #Adds SQL records to cargo list

#CREATED A NEW JSON WITHIN GET REQUESTS BECAUSE IT WOULD NOT CHANGE WHEN I USED A POST METHOD.

    if 'id' in request.args:  #Checks if and id is given in api parameters
        id = int(request.args['id']) #ID in parameter to be compared later in for loop.
    else:
        return "NO ID GIVEN" #If there is not ID in the parameter this will be returned.
    result = [] #All the results will be placed here
    for item in cargos_: #For loop iterates through cargo list in line 20
        if item['id'] == id: 
            result.append(item) #Adds record in result list if the id matches the parameter.
    return jsonify(result) #Turns the results list into JSON.

##########CAPTAIN TABLE GET ROUTE ##########
@app.route('/api/captain', methods=['GET'])
def get_all_captains():
    conn = create_connection('hw1cis3368.c8aubdep9gnu.us-east-2.rds.amazonaws.com', 'admin', 'Passward1!', 'intersteller')
    captains = []
    sql_select = "SELECT * FROM captain"
    captains_ = execute_query(conn, sql_select)
    for item in captains_:
        captains.append({
            'firstname': item['firstname'],
            'lastname': item['lastname'],
            'captainrank': item['captainrank'],
            'homeplanet': item['homeplanet']
        })
    return jsonify(captains)

@app.route('/captain', methods=['GET'])
def captain1():
    response = request.get('http://127.0.0.1:5000/api/captain')
    captain_data = response.json()

    return render_template('captain.html', captains=captain_data)

@app.route('/api/captain/all',methods=['GET']) #Creates get request for all captains
def get_captains():
    captain = [] #Houses the SQL results
    sql_select = "SELECT * FROM captain" #SQL command to get all captains
    captains = execute_query(conn,sql_select) #Executes SQL
    for c in captains:
        captain.append(c) #Adds SQL records to captain list
    return jsonify(captain) #Turns list into JSON


@app.route('/api/captain',methods=['GET'])  
def get_captain_id():
    captains = [] # Houses the SQL results
    sql_select = "SELECT * FROM captain" # SQL command to get all captains
    captains_ = execute_query(conn, sql_select) # Executes SQL
    for c in captains_:
        captains.append(c) # Adds SQL records to captains list

    # CREATED A NEW JSON WITHIN GET REQUESTS BECAUSE IT WOULD NOT CHANGE WHEN I USED A POST METHOD.
    if 'id' in request.args:  # Checks if an ID is given in api parameters
        id = int(request.args['id']) # ID in parameter to be compared later in for loop.
    else:
        return "NO ID GIVEN" # If there is no ID in the parameter, this will be returned.

    result = [] # All the results will be placed here
    for item in captains: # For loop iterates through captains list 
        if item['id'] == id: 
            result.append(item) # Adds record in result list if the id matches the parameter.

    return jsonify(result) # Turns the results list into JSON.


##############SPACESHIP TABLE GET ROUTE ###################
@app.route('/api/spaceship', methods=['GET'])
def get_spaceship():
    spaceships = []  # Houses the SQL results
    sql_select = "SELECT * FROM spaceship"  # SQL command to get all spaceships
    spaceships_ = execute_query(conn, sql_select)  # Executes SQL
    for s in spaceships_:
        spaceships.append(s)  # Adds SQL records to spaceships list

    return jsonify(spaceships)  # Turns list into JSON

def get_all_spaceships():
    cursor = conn.cursor()
    query = "SELECT * FROM spaceship"
    cursor.execute(query)
    spaceships = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    cursor.close()
    return spaceships


def add_cargo(cargotype, weight, departure, arrival, shipid):
    cursor = conn.cursor()

    query = """
        INSERT INTO cargo (cargotype, weight, departure, arrival, shipid)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (cargotype, weight, departure, arrival, shipid))
    conn.commit()
    cursor.close()
    conn.close()



    #####################POST ROUTES FOR ALL TABLES###################
# def get_ship_ids():
#     query = "SELECT id as shipid FROM spaceship"
#     result = execute_query(conn, query)
#     return [row['shipid'] for row in result]


    ###CARGO TABLE###

from flask import jsonify

@app.route('/api/cargo', methods=['POST'])
def create_cargo():
    cargotype = request.form['cargotype']
    weight = request.form['weight']
    departure = request.form['departure']
    arrival = request.form['arrival']

    # Get all ship_ids from the spaceship table
    ship_ids = get_all_spaceships()
    # Assign a random Ship ID from the list
    ship_id = random.choice(ship_ids)
    # Add the new cargo to the database
    add_cargo(cargotype, weight, departure, arrival, ship_id)
    return redirect(url_for('cargo'))

    ###CAPTAIN TABLE###
@app.route('/api/captain/add_captain', methods=['POST'])
def add_item1():
    request_data = request.form
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    captainrank = request_data['captainrank']
    homeplanet = request_data['homeplanet']
    
    add_sql = f"INSERT INTO captain (firstname, lastname, captainrank, homeplanet) VALUES ('{firstname}', '{lastname}', '{captainrank}', '{homeplanet}')"
    cursor = execute_query(conn, add_sql)
    captain_id = cursor.lastrowid
    return jsonify({"id": captain_id}) # Return the inserted id




###################PUT REQUEST FOR ALL TABLES##################

########CARGO TABLE############

@app.route('/api/cargo',methods=['PUT']) #Can be tested by using link like this: http://127.0.0.1:5000/api/cargo?id=[ID of your choosing]
def change_item2():
    if 'id' in request.args:
        id=int(request.args['id'])
        request_data = request.get_json()
        it_weight = request_data['Weight'] #weight to update
        it_cargotype = request_data['Cargotype'] #cargotype to update
        it_departure = request_data['Departure'] #Departure to update
        it_arrival = request_data['Arrival'] 
        it_shipid = request_data['shipid']
        #arrival to update
        update_item_sql = f"UPDATE cargo SET Weight='{it_weight}', Cargotype'{it_cargotype}',Departure='{it_departure}',Arrival='{it_arrival},Shipid='{it_shipid}'  WHERE id={id}"
        execute_query(conn,update_item_sql)
        
    else:
        return 'NO ID GIVEN TO UPDATE' #If there is no ID in the API url this is returned.
    return 'CARGO UPDATED' #Confirms that cargo is updated.



########captain TABLE########
@app.route('/api/captain/<int:captain_id>', methods=['PUT'])
def change_item1(captain_id):
    request_data = request.get_json()  # Allows data to be added in JSON format
    new_firstname = request_data['firstname']
    new_lastname = request_data['lastname']  # new lastname to be added
    new_captainrank = request_data['captainrank']  # new captainrank to be added
    new_homeplanet = request_data['homeplanet']  # new homeplanet to be added

    add_sql = f"INSERT INTO captain VALUES (id,firstname='{new_firstname}',lastname='{new_lastname}',captainrank='{new_captainrank}',homeplanet='{new_homeplanet}')"  # Turns JSON data to SQL insert
    execute_query(conn, add_sql)

    return 'CAPTAIN UPDATED'  # Confirms that captain is updated.


########SPACESHIP TABLE########
@app.route('/api/spaceship', methods=['POST'])
def add_spaceship():
    try:
        request_data = request.json

        if 'maxweight' not in request.form:
            return jsonify({'error': 'maxweight is missing'}), 400

        new_maxweight = request.form['maxweight']
        new_spaceshipid = uuid.uuid4().hex  # generate new spaceship ID
        new_captainid = uuid.uuid4().hex   # generate new captain ID

        # insert new captain into Captain table
        add_captain_sql = f"INSERT INTO captain (id) VALUES ('{new_captainid}')"
        execute_query(conn, add_captain_sql, fetch=False)  # Set fetch to False

        # insert new spaceship with new captain into Spaceship table
        add_spaceship_sql = f"INSERT INTO spaceship (id, captainid, maxweight) VALUES ('{new_spaceshipid}', '{new_captainid}', {new_maxweight})"
        execute_query(conn, add_spaceship_sql, fetch=False)  # Set fetch to False

        return jsonify({"status": "success", "spaceship": {"id": new_spaceshipid, "captainid": new_captainid, "maxweight": new_maxweight}})

    except Exception as e:
        return jsonify({'error': str(e)}), 400








    #################DELETE ROUTES##################

    ###########CARGO TABLE##############
@app.route('/api/cargo',methods=['DELETE'])
def del_item():
    if 'id' in request.args:
        id=int(request.args['id'])
    else:
        return "NO ID GIVEN TO DELETE" #If no ID parameter is given this is returned
    delete_c_sql = f"DELETE FROM captain WHERE id={id}" #Runs SQL statment using the id param as WHERE constraint. 
    execute_query(conn,delete_c_sql) 
    return f"captain WITH ID:{id} DELETED" 



    ############SPACESHIP TABLE################
@app.route('/api/spaceship',methods=['DELETE']) #Can be tested by using link like this: http://127.0.0.1:5000/api/spaceship?id=[ID of your choosing]
def del_ships():
    if 'id' in request.args:
        id=int(request.args['id']) #Allows user to user ID as parameter.
    else:
        return "NO ID GIVEN TO DELETE" #If no ID parameter is given this is returned
    delete_c_sql = f"DELETE FROM spaceship WHERE id={id}" #Runs SQL statment using the id param as WHERE constraint. 
    execute_query(conn,delete_c_sql) 

    return f"spaceship WITH ID:{id} DELETED" 

@app.route('/api/captain', methods=['DELETE'])
def delete_captain():
    if 'id' in request.args:
        id = int(request.args['id'])  # Allows user to use ID as a parameter.
    else:
        return "NO ID GIVEN TO DELETE"  # If no ID parameter is given this is returned
    delete_captain_sql = f"DELETE FROM captain WHERE id={id}"  # Runs SQL statement using the id param as WHERE constraint.
    execute_query(conn, delete_captain_sql)

    return f"captain WITH ID:{id} DELETED"  # Delete confirmation


if __name__ == '__main__':
    app.run(debug=True, port=3000)

