from flask import Flask
from newsapi import NewsApiClient
import xmlrpc.client
import datetime
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from flask import request
import socket
import hprose

app = Flask(__name__)

# HPRose application
def ping():
    return socket.gethostbyname(socket.gethostname())

# Student queries
# http://localhost:5000/students?name=alice
@app.route('/students')
def user_queries():

    id = request.args.get('id')
    name = request.args.get('name')
    dob = request.args.get('dob')

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="http://localhost:4000/graphql")
    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    if id != None:
        # Provide a GraphQL query
        query = gql(
            """
            query name($id: String)
            { queryById(studentId: $id) {
            studentId
            studentName
            studentDOB
            }

            }
            """
        )
        variable = {"id":id}
    elif name != None:
       # Provide a GraphQL query
        query = gql(
            """
            query name($name: String)
            { queryByName(studentName: $name) {
            studentId
            studentName
            studentDOB
            }

            }
            """
        )
        variable = {"name":name}
    elif dob != None:
        # Provide a GraphQL query
        query = gql(
            """
            query name($dob: String)
            { queryByDOB(studentDOB: $dob) {
            studentId
            studentName
            studentDOB
            }

            }
            """
        )
        variable = {"dob":dob}

    result = client.execute(query, variable)
    print(result)

    return result

# Save users in the users.log file
# http://localhost:5000/insertStudent?number=B00102810&first=farihah&last=hamizan
@app.route('/insertStudent')
def insertstudent():
    number = request.args.get('number')
    first = request.args.get('first')
    last = request.args.get('last')

    # append users to the end of the file
    get_file = open('users.log','a')

    curr = datetime.datetime.now()

    # write the current datetime and the name of the functions that is called
    get_file.write(curr.strftime("%c") + ": " + str(number) + " " + str(first) + " " + str(last) +"\n")

    get_file.close()

    return 'The file has been updated with: ' + str(number)  + " " + str(first) + " " + str(last)
    # return 'Insert student'

# Ping Pong task
@app.route('/ping')
def ping_pong():

    curr = datetime.datetime.now()

    return 'pong         ' + curr.strftime("%c")
    
# Call the rpc server in the python xmlserver.py
# http://localhost:5000/callClient?arg=8
@app.route('/callClient')
def rpc_client():

    temp = request.args.get('temp')

    result = ''

    with xmlrpc.client.ServerProxy("http://localhost:8001/",allow_none=True) as proxy:
        result = str(proxy.is_warm_cold(int(temp)))
        update_calls()
    
    if result == 'Warm':
        result = 'The value given is ' + temp + ' therefore it is <b>' + result + '</b>'
    elif result == 'Cold':
        result = 'The value given is ' + temp + ' therefore it is <b>' + result + '</b>'

    return str(result)

# Update the calls in the calls.log file each time the xml server is called by the client
def update_calls():
    # it will append the value to the end of the file
    get_file = open('calls.log','a')

    curr = datetime.datetime.now()

    # write the current datetime and the name of the functions that is called
    get_file.write(curr.strftime("%c") + ", the function name is is_warm_cold \n")

    get_file.close()

# Default hello world page
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 2 Defined URLs
# To see the retun values (http://newsapi.org/v2/top-headlines?q=forecast&country=ie&apiKey=966611677d694731833118dddf7bd7fc)
@app.route('/justweather')
def get_weather():
    newsapi = NewsApiClient(api_key='966611677d694731833118dddf7bd7fc')

    # weather article
    # weather = newsapi.get_top_headlines(q='forecast',country='ie')
    weather = newsapi.get_everything(q='forecast',
                                          from_param='2021-02-20',
                                          to='2021-04-30',
                                          language='en',
                                          sort_by='relevancy',
                                          page=1)

    result = ''

    for k, v in weather.items():
        result = result + str(v)

    return result

# Another page (url to test: http://127.0.0.1:5000/updates) - Return a list of all the time that the service has been updated.
@app.route('/updates')
def read_update():
    get_file = open('updates.txt','r')
    read_content = get_file.readlines()

    output = '{'

    # Return content in json format
    for i in read_content:
        output = output + '"line": "' + i + '",'
    get_file.close()

    # Get rid of the comma at the end
    output = output[:-1]

    output = output + '}'

    return output