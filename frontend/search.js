import { navbar } from "./header.js";

async function render_products() {
    var content_container = document.getElementById("content-container");

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    try {
        var query = urlParams.get("searchbar").replaceAll(" ", "space").replaceAll("&", "amp");
        var order = urlParams.get('sort-select');
    }
    catch(err) {
        console.log(err);
        var query = urlParams.get("q");
        var order = urlParams.get("order");
    }
    var page = urlParams.get('page');
    if (page == null) {
        page = "1";
    }

    const URL = `http://localhost:3000/search?q=${query}&order=${order}&page=${page}`
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
    // console.log(keys)

    var products = result['products'];
    if (keys.includes("products") && products.length!=0) {
        var page = result['page'];
        var pages = result['pages'];
        // console.log(page, pages);

        var products_container = document.createElement("div");
        products_container.classList.add("small-container");
        content_container.appendChild(products_container);

        var products_container_title = document.createElement("h2");
        products_container_title.classList.add("title");
        query = query.replaceAll("space", " ").replaceAll("amp", "&");
        products_container_title.innerHTML = `${query} Products`;
        products_container.appendChild(products_container_title);

        var products_grid = document.createElement("div");
        products_grid.classList.add("product-grid");
        products_container.appendChild(products_grid);

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

        var pagination_div = document.createElement("div");
        pagination_div.classList.add("pagination");
        content_container.appendChild(pagination_div);

        var pagination_buttons = document.createElement("div");
        pagination_buttons.classList.add("text-right");
        pagination_div.appendChild(pagination_buttons);

        if (page != 1) {
            var previous_button = document.createElement("a");
            previous_button.href = `./search.html?q=${query}&order=${order}&page=${page - 1}`;  // to be changed
            previous_button.classList.add("btn-not-active");
            previous_button.innerHTML = "<b>&laquo;</b>";
            pagination_buttons.appendChild(previous_button);
        }
        if (page - 1 != 0) {
            var previous_button_number = document.createElement("a");
            previous_button_number.href = `./search.html?q=${query}&order=${order}&page=${page - 1}`; // to be changed
            previous_button_number.classList.add("btn-not-active");
            previous_button_number.innerHTML = page - 1;
            pagination_buttons.appendChild(previous_button_number);
        }
        var current_button = document.createElement("a");
        current_button.href = `./search.html?q=${query}&order=${order}&page=${page}`; // to be changed
        current_button.classList.add("btn");
        current_button.innerHTML = page;
        pagination_buttons.appendChild(current_button);

        if (page + 1 <= pages) {
            var next_button_number = document.createElement("a");
            next_button_number.href = `./search.html?q=${query}&order=${order}&page=${page + 1}`; // to be changed
            next_button_number.classList.add("btn-not-active");
            next_button_number.innerHTML = page + 1;
            pagination_buttons.appendChild(next_button_number);
        }
        if (page != pages) {
            var next_button = document.createElement("a");
            next_button.href = `./search.html?q=${query}&order=${order}&page=${page + 1}`; // to be changed
            next_button.classList.add("btn-not-active");
            next_button.innerHTML = "<b>&raquo;</b>";
            pagination_buttons.appendChild(next_button);
        }

        var pagination_p = document.createElement("p");
        pagination_p.classList.add("text-right");
        pagination_p.innerHTML = "Showing page " + page + " of " + pages;
        pagination_div.appendChild(pagination_p);
    }
    else {
        var products_container = document.createElement("div");
        products_container.classList.add("small-container");
        content_container.appendChild(products_container);

        var products_container_title = document.createElement("h2");
        products_container_title.classList.add("title");
        products_container_title.innerHTML = "No Products To Be Displayed.";
        products_container.appendChild(products_container_title);
    }
}

window.onload = function () {
    navbar();
    render_products();
}