import { navbar } from "./header.js";

function showContent() {
    const contentDiv = document.getElementById("content-container");
    contentDiv.style.display = "block";
}

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
        var recommended_products = result['recommend'];

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

            var recommend_product_row = document.getElementById("recommend-row");

            for (let product in recommended_products) {
                var product_wrapper = document.createElement("a");
                product_wrapper.href = `./product-details.html?product_id=${recommended_products[product][0]}`;
                product_wrapper.classList.add("col-4");
                recommend_product_row.appendChild(product_wrapper);

                var product_div = document.createElement("div");
                product_div.classList.add("product");
                product_wrapper.appendChild(product_div);

                var product_img = document.createElement("img");
                product_img.src = recommended_products[product][2];
                product_div.appendChild(product_img);

                var product_h4 = document.createElement("h4");
                product_h4.classList.add("product-title");
                product_h4.innerHTML = recommended_products[product][1];
                product_div.appendChild(product_h4);

                var product_p = document.createElement("p");
                product_p.innerHTML = "$" + recommended_products[product][4];
                product_div.appendChild(product_p);
            }
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
    showContent();
}