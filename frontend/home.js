import { navbar } from "./header.js";

function render_explore_content() {
    var content_container = document.getElementById("content-container");

    var explore_div = document.createElement("div");
    explore_div.id = "row";
    explore_div.classList.add("row");
    content_container.appendChild(explore_div);

    var explore_inside_div1 = document.createElement("div");
    explore_inside_div1.id = "col-2";
    explore_inside_div1.classList.add("col-2");
    explore_div.appendChild(explore_inside_div1);

    var explore_col1_h1 = document.createElement("h1");
    explore_col1_h1.innerHTML = `Give Your Wardrobe <br> A Makeover!`;
    explore_inside_div1.appendChild(explore_col1_h1);

    var explore_col1_p = document.createElement("p");
    explore_col1_p.innerHTML = "Style is a way to say who you are without having to speak.";
    explore_inside_div1.appendChild(explore_col1_p);

    var explore_col1_a = document.createElement("a");
    explore_col1_a.href = "./products.html?page=1"; // to be changed
    explore_col1_a.classList.add("btn");
    explore_col1_a.innerHTML = `Explore Now &#8594;`;
    explore_inside_div1.appendChild(explore_col1_a);

    var explore_inside_div2 = document.createElement("div");
    explore_inside_div2.classList.add("col-2");
    explore_div.appendChild(explore_inside_div2);

    var explore_col2_img = document.createElement("img");
    explore_col2_img.src = "./fashion-background.png";
    explore_inside_div2.appendChild(explore_col2_img);
}

async function render_featured_content() {
    var content_container = document.getElementById("content-container");

    var products_container = document.createElement("div");
    products_container.classList.add("small-container");
    content_container.appendChild(products_container);

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
    // console.log(keys.includes("products"));
    if (keys.includes("products")) {
        var products = result['products']
        // console.log(products);
        var products_container_title = document.createElement("h2");
        products_container_title.classList.add("title");
        products_container_title.innerHTML = "Featured Products";
        products_container.appendChild(products_container_title);

        var products_grid = document.createElement("div");
        products_grid.classList.add("product-grid")
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
            product_p.innerHTML = "$"+products[product][2];
            product_div.appendChild(product_p);
        }
        products_container.appendChild(products_grid);
    }
    else {
        var products_container_title = document.createElement("h2");
        products_container_title.classList.add("title");
        products_container_title.innerHTML = "No Featured Products";
        products_container.appendChild(products_container_title);
    }
}

window.onload = function () {
    navbar();
    render_explore_content();
    render_featured_content();
}