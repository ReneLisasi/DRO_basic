
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
    
    json_coords= json.loads(request.form['clickedLocation'])
    lat = json_coords['lat']
    lng = json_coords['lng']
    mid_coords=(lat,lng)
    mid_node=test2.Node((lat,lng),0)
    print(f'Front end data received in flask route:{mid_state},{mid_zip},{mid_node}')
    back_station=test2.get_stations(mid_node,mid_state,mid_zip)
    #test2.get_stations returns fire station object with 
    #parameters:(self, name, geometry, zip_code, city, state, address, global_id, distance)
    #use back_station.parameter in the return
    #return render_template('index.html',state=mid_state, zip_code=mid_zip, coords=back_station.name)#for testing
    return render_template('index.html',return_start=mid_coords,return_name=back_station.name, return_geometry=back_station.geometry, 
                           return_zip=back_station.zip_code, return_city=back_station.city, return_state=back_station.state, 
                           return_address=back_station.address, return_global_id=back_station.global_id, 
                           return_distance=back_station.distance)#the return viariables are set in the html, make sure they match here

if __name__=='__main__':
    app.run(debug=True)