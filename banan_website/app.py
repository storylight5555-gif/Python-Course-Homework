from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-your-own-project"

PRODUCT = {
    "name": "Banan Universal One",
    "price": 699,
    "currency": "AED",
    "description": "A new kind of everyday phone. Thoughtful design, powerful performance, and a clean experience."
}

@app.context_processor
def inject_globals():
    return {"cart_count": session.get("cart_count", 0), "product": PRODUCT}

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/shop")
def shop():
    return render_template("shop.html", page="shop")

@app.route("/support")
def support():
    return render_template("support.html", page="support")

@app.route("/onboarding")
def onboarding():
    return render_template("onboarding.html", page="onboarding")

@app.post("/cart/add")
def add_to_cart():
    session["cart_count"] = session.get("cart_count", 0) + 1
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"count": session["cart_count"], "message": "Added to your demo cart"})
    return redirect(request.referrer or url_for("home"))

@app.route("/cart")
def cart():
    return render_template("cart.html", page="cart", quantity=session.get("cart_count", 0))

@app.post("/cart/clear")
def clear_cart():
    session["cart_count"] = 0
    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)
