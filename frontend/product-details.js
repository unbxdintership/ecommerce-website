import { navbar } from "./header.js";

async function render_product() {
    var content_container = document.getElementById("content-container");

    var content_style = document.createElement("style");
    content_style.innerHTML = `
    .small-container {
        max-width: 90%;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 70px;
        padding-left: 25px;
        padding-right: 25px;
        box-shadow: 0 0 20px 0px rgba(0, 0, 0, 0.1);
    }

    .small-container .row {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        justify-content: space-around;
    }

    .col-2 {
        flex-basis: 50%;
        min-width: 300px;
        padding-left: 50px;
    }

    .col-2 h1 {
        padding-top: 20px;
        padding-bottom: 20px;
        text-transform: capitalize;
    }

    .col-2 img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 70%;
        height: 70%;
        padding: 50px 0;
    }

    .single-product .col-2 {
        padding: 20px;
    }

    .single-product .col-2 img {
        padding: 0;
    }

    .single-product h4 {
        margin: 20px 0;
        font-size: 22px;
        font-weight: bold;
    }
    `;
    content_container.appendChild(content_style);

    const queryString = window.location.search;
    // console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    // console.log(urlParams);
    const product_id = urlParams.get('product_id');
    // console.log(product_id);

    const URL = `http://localhost:3000/products/${product_id}`; // to be changed
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
    // console.log(result);
    var keys = Object.keys(result);
    // console.log(keys.includes("product"));
    // console.log(keys)
    if (keys.includes("product")) {
        var product = result['product'];

        // console.log(product)

        var products_container = document.createElement("div");
        products_container.classList.add("small-container");
        products_container.classList.add("single-product");
        content_container.appendChild(products_container);

        var product_details_container = document.createElement("div");
        product_details_container.classList.add("row");
        products_container.appendChild(product_details_container);

        var product_details_col1 = document.createElement("div");
        product_details_col1.classList.add("col-2");
        product_details_container.appendChild(product_details_col1);

        // console.log(product[4]);

        var product_details_col1_img = document.createElement("img");
        product_details_col1_img.src = product[2];
        product_details_col1.appendChild(product_details_col1_img);

        var product_details_col2 = document.createElement("div");
        product_details_col2.classList.add("col-2");
        product_details_container.appendChild(product_details_col2);

        var product_details_col2_p = document.createElement("p");
        product_details_col2_p.innerHTML = "Home / Product / " + product[0];
        product_details_col2.appendChild(product_details_col2_p);

        var product_details_col2_h1 = document.createElement("h1");
        product_details_col2_h1.innerHTML = product[1];
        product_details_col2.style.textTransform = "capitalize";
        product_details_col2.appendChild(product_details_col2_h1);

        var product_details_col2_h4 = document.createElement("h4");
        product_details_col2_h4.innerHTML = "$" + product[4];
        product_details_col2.appendChild(product_details_col2_h4);

        var product_details_col2_h3 = document.createElement("h3");
        product_details_col2_h3.innerHTML = "Product Details:";
        product_details_col2.appendChild(product_details_col2_h3);

        var product_details_col2_details_p = document.createElement("p");
        product_details_col2_details_p.innerHTML = product[6];
        product_details_col2.appendChild(product_details_col2_details_p);
    }
}

window.onload = function () {
    navbar();
    render_product();
}