
from flask import Flask, render_template, request,url_for
import test2

app=Flask(__name__)

#index route starter
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    back_state=request.form['front_state']
    back_zip=request.form['front_zip']
    back_coords=request.form['clickedLocation']
    print(back_state,back_zip,back_coords)
    return render_template('index.html',state=back_state, zip_code=back_zip, coords=back_coords)

if __name__=='__main__':
    app.run(debug=True)