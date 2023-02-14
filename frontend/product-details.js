import { navbar } from "./header.js";

async function render_product() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const product_id = urlParams.get('product_id');

    var content_container = document.getElementById("content-container");

    const URL = `http://localhost:3000/products/${product_id}`;
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
    if (keys.includes("product")) {
        var product = result['product'];

        if (product.length != 0) {
            var product_details_col1_img = document.getElementById("prod-det-img");
            product_details_col1_img.src = product[2];

            var product_details_col2_p = document.getElementById("prod-det-p");
            product_details_col2_p.innerHTML = "Home / Product / " + product[0];

            var product_details_col2_h1 = document.getElementById("prod-det-h1");
            product_details_col2_h1.innerHTML = product[1];

            var product_details_col2_h4 = document.getElementById("prod-det-h4");
            product_details_col2_h4.innerHTML = "$" + product[4];

            var product_details_col2_h3 = document.getElementById("prod-det-h3");
            product_details_col2_h3.innerHTML = "Product Details:";

            var product_details_col2_details_p = document.getElementById("prod-det-details");
            product_details_col2_details_p.innerHTML = product[6];
        }
        else {
            var product_title = document.createElement("h1");
            product_title.classList.add("title");
            products_title.innerHTML = "Product does not exist.";
            content_container.appendChild(product_title)
        }
    }
}

window.onload = function () {
    navbar();
    render_product();
}