from flask import Flask, render_template

app = Flask(__name__)

categories = {
    "Men": [
        'Pant',
        'Shirt',
        'Caps'
    ],
    "Women": [
        'Tops',
        'Dresses',
        'Earrings'
    ]
}

products = [
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg'],
    ['Top', '$25', 'https://www.w3schools.com/images/lamp.jpg']
]


@app.route("/products/")
def home():
    return render_template("home.html", title="HomePage", categories=categories, products=products)


@app.route("/products/<product_id>")
def render_product(product_id):
    product_name, product_price, product_url, product_description = products[0][0], products[0][1], products[0][2], "This is a very nice top which looks like a lightbulb."
    return render_template("product.html", categories=categories, product_id=product_id, product_name=product_name, product_price=product_price, product_url=product_url, product_description=product_description)

if __name__ == "__main__":
    app.run(debug=True)