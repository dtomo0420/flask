from flask import Flask, render_template, request, url_for, redirect
import sqlite3


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def database_length():
    connection = sqlite3.connect('beer.db')
    data = connection.execute("SELECT * FROM BEERS;").fetchall()
    return (len(data) // 100) + 1


'''
in the case of the POST method: list the elements with the appropriate name and style
in the case of the GET method: list all elements

@param  number  it points out that it should be listed from which row

@return after   recording it will return to index.html
'''
@app.route("/select/<int:number>", methods=['GET', 'POST'])
def select(number):
    connection = sqlite3.connect('beer.db')
    length = database_length()
    try:
        if request.method == "POST":
            name = "'%" + request.form.get("name") + "%'"
            style = "'%" + request.form.get("style") + "%'"
            data = connection.execute(
                "SELECT * FROM BEERS WHERE NAME LIKE {} AND STYLE LIKE {} ORDER BY ID;"
                .format(name, style)).fetchall()
            length = 1
        else:
            off = number * 100
            data = connection.execute("SELECT * FROM BEERS ORDER BY ID LIMIT 100 OFFSET {};".format(off)).fetchall()

        connection.commit()
        connection.close()

        json_data = []
        for i in data:
            json_element = {
                "ABV": i[0],
                "IBU": i[1],
                "ID": i[2],
                "NAME": i[3],
                "STYLE": i[4],
                "BREWERY_ID": i[5],
                "OUNCES": i[6]
            }

            json_data.append(json_element)

        return render_template('list.html', data=json_data, len=length)
    except sqlite3.Error as error:
        print("Failed to select from table", error)
    finally:
        if connection:
            connection.close()


'''
insert  new elements to the database

@return after recording it will return to index.html
'''
@app.route("/insert_item", methods=['POST', 'GET'])
def insert_item():
    if request.method == 'POST':
        try:
            connection = sqlite3.connect('beer.db')

            id = request.form.get("id")
            name = request.form.get("name")
            style = request.form.get("style")
            abv = request.form.get("abv")
            ibu = request.form.get("ibu")
            brewery_id = request.form.get("brewery_id")
            ounces = request.form.get("ounces")

            connection.execute("INSERT INTO BEERS "
                               "(ABV, IBU, ID, NAME, STYLE, BREWERY_ID, OUNCES) VALUES"
                               "({}, {}, {}, {}, {}, {}, {});"
                               .format(abv, ibu, id, name, style, brewery_id, ounces))
            connection.commit()
            connection.close()
        except sqlite3.Error as error:
            print("Failed to insert to table", error)
        finally:
            if connection:
                connection.close()
            return render_template("index.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/insert")
def insert():
    return render_template("insert.html")


'''
updates the elements of the database where the id and name are the same as those given in the parameter.

@param  id      id of the beer to be modified
@param name    name of the beer to be modified

@return returns to the search page
'''
@app.route("/modify_item/<string:id>/<string:name>", methods=['POST', 'GET'])
def modify_item(id, name):
    if request.method == 'POST':
        try:
            connection = sqlite3.connect('beer.db')

            n_style = request.form.get("style")
            n_abv = request.form.get("abv")
            n_ibu = request.form.get("ibu")
            n_brewery_id = request.form.get("brewery_id")
            n_ounces = request.form.get("ounces")

            connection.execute(
                "UPDATE BEERS SET STYLE = {}, IBU = {}, BREWERY_ID = {}, OUNCES = {}, ABV = {} WHERE ID = {} AND NAME = {};"
                .format(n_style, n_ibu, n_brewery_id, n_ounces, n_abv, id, name))
            connection.commit()
            connection.close()
        except sqlite3.Error as error:
            print("Failed to insert to table", error)
        finally:
            if connection:
                connection.close()
            return render_template("search.html")


'''
passes parameters

@param  id     the id of the beer to be modified
@param name    the name of the beer to be modified
@param style   the current style of the beer to be modified
@param abv     the current abv value of the beer to be modified
@param ibu     the current ibu value of the beer to be modified
@param brewery_id   the current brewery_id value of the beer to be modified
@param ounces   the current ounces value of the beer to be modified

@return returns to edit page
'''
@app.route("/modify_page/<string:id>/<string:name>/<string:style>/<string:abv>/<string:ibu>/<string:brewery_id>/<string:ounces>", methods=['POST', 'GET'])
def modify_page(id, name, style, abv, ibu, brewery_id, ounces):
    return render_template("edit.html", id=id, name=name, style=style, abv=abv, ibu=ibu, brewery_id=brewery_id, ounces=ounces)


if __name__ == '__main__':
    app.run(port=4041)
