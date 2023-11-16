
from flask import Flask, render_template, request,url_for
import test2
import json

app=Flask(__name__)

#index route starter
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    mid_state=request.form['front_state']
    mid_zip=request.form['front_zip']
    action = request.form.get('action')
    
    json_coords= json.loads(request.form['clickedLocation'])
    lat = json_coords['lat']#json likes to swap order so don't be startled about why they get swapped in the return
    lng = json_coords['lng']
    mid_node=test2.Node((lat,lng),0)
    print(f'Front end data received in flask route:{mid_state},{mid_zip},{mid_node}')

    if action=='bubble':
        sorting_algorithm='bubble'
    elif action=='merge':
        sorting_algorithm='merge'
    elif action=='selection':
        sorting_algorithm='selection'

    back_station=test2.get_stations(mid_node,mid_state,mid_zip,sorting_algorithm)

    #test2.get_stations returns fire station object
    #parameters available for fire station object:(self, name, geometry, zip_code, city, state, address, global_id, distance)
    #use back_station.parameter in the return
    #example return statement: return render_template('index.html',state=mid_state, zip_code=mid_zip, coords=back_station.name)#for testing
    back_lat=(back_station.geometry[0])
    back_lng=(back_station.geometry[1])
    return render_template('index.html',return_start_lng=lat, return_start_lat=lng,return_name=back_station.name, return_lat=back_lat, return_lng=back_lng, 
                           return_zip=back_station.zip_code, return_city=back_station.city, return_state=back_station.state, 
                           return_address=back_station.address, return_global_id=back_station.global_id, 
                           return_distance=back_station.distance)#the return viariables are set in the html, make sure they match here

if __name__=='__main__':
    app.run(debug=True)