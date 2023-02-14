import { navbar } from "./header.js";

async function render_featured_content() {

    const URL = "http://localhost:3000/home/"
    let response = await fetch(URL, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });
    var result = await response.json();
    var keys = Object.keys(result);
    if (keys.includes("products")) {
        var products = result['products'];
        if (products.length != 0) {
            var products_grid = document.getElementById("product-grid");
            for (let product in products) {
                var product_wrapper = document.createElement("a");
                product_wrapper.href = `./product-details.html?product_id=${products[product][0]}`;
                product_wrapper.classList.add("product-link");
                products_grid.appendChild(product_wrapper);

                var product_div = document.createElement("div");
                product_div.classList.add("product");
                product_wrapper.appendChild(product_div);

                var product_img = document.createElement("img");
                product_img.src = products[product][4];
                product_div.appendChild(product_img);

                var product_h4 = document.createElement("h4");
                product_h4.classList.add("product-title");
                product_h4.innerHTML = products[product][1];
                product_div.appendChild(product_h4);

                var product_p = document.createElement("p");
                product_p.innerHTML = "$" + products[product][2];
                product_div.appendChild(product_p);
            }
        }
        else {
            var products_container_title = document.getElementById("title");
            products_container_title.innerHTML = "No Featured Products";
        }
    }
    else {
        var products_container_title = document.getElementById("title");
        products_container_title.innerHTML = "No Featured Products";
    }
}

window.onload = function () {
    navbar();
    render_featured_content();
}