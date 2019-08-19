
# Import Flask related dependencies
from flask import Flask, render_template, jsonify, redirect
# Import pymongo library, to connect Flask app to Mongo database.
from flask_pymongo import PyMongo
# Import scrape_mars
import scrape_mars



# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable and pass connection to the pymongo instance
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Create and set route to query Mongo database and 
# pass the mars data into an HTML template to display the data.

@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars = mars)


# Create a route called `/scrape` that imports `scrape_mars.py` script and call `scrape` function. 
@app.route("/scrape")
def scrape():
    
    mars_data = scrape_mars.scrape()
    
    # Store the return value in Mongo as a Python dictionary
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)