import { navbar } from "./header.js";

function hideLoader() {
    const loaderDiv = document.getElementById("loader");
    loaderDiv.style.display = "none";
}

function showContent() {
    const contentDiv = document.getElementById("content-container");
    contentDiv.style.display = "block";
}

async function render_products() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    var query;
    var order;
    var page;

    try {
        query = urlParams.get("q").replaceAll('&', "amp").replaceAll(' ', "space");
        order = urlParams.get("diff_sort_select");
        page = urlParams.get("page")
    }
    catch (err) {
        var query = urlParams.get("q").replaceAll('&', "amp").replaceAll(' ', "space");
        var order = urlParams.get("order");
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

    var products = result['products'];
    if (keys.includes("products")) {
        var page = result['page'];
        var pages = result['pages'];

        var products_container_title = document.getElementById("title");
        query = query.replaceAll("space", " ").replaceAll("amp", "&");
        products_container_title.innerHTML = `${query} Products`;

        var diff_hidden_search = document.getElementById("q");
        diff_hidden_search.value = query;

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

        var pagination_buttons = document.getElementById("text-right");

        if (page != 1) {
            var previous_button = document.createElement("a");
            previous_button.href = `./search.html?q=${query}&order=${order}&page=${page - 1}&diff_sort_select=${order}`;
            previous_button.classList.add("btn-not-active");
            previous_button.innerHTML = "<b>&laquo;</b>";
            pagination_buttons.appendChild(previous_button);
        }
        if (page - 1 != 0) {
            var previous_button_number = document.createElement("a");
            previous_button_number.href = `./search.html?q=${query}&order=${order}&page=${page - 1}&diff_sort_select=${order}`;
            previous_button_number.classList.add("btn-not-active");
            previous_button_number.innerHTML = page - 1;
            pagination_buttons.appendChild(previous_button_number);
        }
        var current_button = document.createElement("a");
        current_button.href = `./search.html?q=${query}&order=${order}&page=${page}&diff_sort_select=${order}`;
        current_button.classList.add("btn");
        current_button.innerHTML = page;
        pagination_buttons.appendChild(current_button);

        if (page + 1 <= pages) {
            var next_button_number = document.createElement("a");
            next_button_number.href = `./search.html?q=${query}&order=${order}&page=${page + 1}&diff_sort_select=${order}`;
            next_button_number.classList.add("btn-not-active");
            next_button_number.innerHTML = page + 1;
            pagination_buttons.appendChild(next_button_number);
        }
        if (page != pages) {
            var next_button = document.createElement("a");
            next_button.href = `./search.html?q=${query}&order=${order}&page=${page + 1}&diff_sort_select=${order}`;
            next_button.classList.add("btn-not-active");
            next_button.innerHTML = "<b>&raquo;</b>";
            pagination_buttons.appendChild(next_button);
        }

        var pagination_p = document.getElementById("text-right-p");
        pagination_p.innerHTML = "Showing page " + page + " of " + pages;
    }
    else {
        var products_container_title = document.getElementById("title");
        products_container_title.innerHTML = "No Products To Be Displayed.";
    }
}

window.onload = function () {
    navbar();
    render_products();
    const timeout_loader = setTimeout(hideLoader, 2000);
    const timeout_content = setTimeout(showContent, 2000);
}