import { navbar } from "./header.js";

async function render_products() {

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    var catlvl1 = urlParams.get('catlvl1').replaceAll('&', "amp").replaceAll(' ', "space");
    var catlvl2 = urlParams.get('catlvl2').replaceAll('&', "amp").replaceAll(' ', "space");
    var page = urlParams.get('page');
    var order = urlParams.get('diff_sort_select')
    var content_container = document.getElementById("content-container");

    console.log(catlvl1, catlvl2, page, order);
    const URL = `http://localhost:3000/category?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page}&order=${order}`
    console.log(URL);
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
        catlvl1 = catlvl1.replaceAll('amp', "&").replaceAll('space', " ");
        catlvl2 = catlvl2.replaceAll('amp', "&").replaceAll('space', " ");
        var products = result['products'];
        var page = result['page'];
        var pages = result['pages'];

        var products_container = document.createElement("div");
        products_container.classList.add("small-container");
        content_container.appendChild(products_container);

        var products_container_title = document.createElement("h2");
        products_container_title.classList.add("title");
        products_container_title.innerHTML = `${catlvl1}-${catlvl2} Products`;
        products_container.appendChild(products_container_title);

        //extra starts here
        var diff_searchbar_form = document.createElement("form");
        diff_searchbar_form.action = `./sortcategory.html`;
        diff_searchbar_form.method = "get";
        diff_searchbar_form.classList.add("diff_form_search");
        diff_searchbar_form.autocomplete = "off";
        products_container.appendChild(diff_searchbar_form);

        var diff_searchbar_select = document.createElement("select");
        diff_searchbar_select.classList.add("diff_sort_select");
        diff_searchbar_select.name = "diff_sort_select";
        diff_searchbar_select.id = "diff_sort_select";
        diff_searchbar_form.appendChild(diff_searchbar_select);

        var diff_options_list = ['None', 'Ascending', 'Descending']//, 'Relevance']
        for (let option in diff_options_list) {
            var diff_opt_option = document.createElement("option");
            diff_opt_option.value = diff_options_list[option];
            diff_opt_option.innerHTML = diff_options_list[option];
            diff_searchbar_select.appendChild(diff_opt_option);
        }

        var diff_hidden_catlvl1 = document.createElement("input")
        diff_hidden_catlvl1.type = "hidden";
        diff_hidden_catlvl1.name = "catlvl1";
        diff_hidden_catlvl1.value = catlvl1
        diff_searchbar_form.appendChild(diff_hidden_catlvl1)

        var diff_hidden_catlvl2 = document.createElement("input")
        diff_hidden_catlvl2.type = "hidden";
        diff_hidden_catlvl2.name = "catlvl2";
        diff_hidden_catlvl2.value = catlvl2
        diff_searchbar_form.appendChild(diff_hidden_catlvl2)

        var diff_hidden_page = document.createElement("input")
        diff_hidden_page.type = "hidden"
        diff_hidden_page.name = "page"
        diff_hidden_page.value = 1
        diff_searchbar_form.appendChild(diff_hidden_page)

        var diff_btn_submit = document.createElement("button")
        diff_btn_submit.type = "submit"
        diff_btn_submit.classList.add("btn")
        diff_btn_submit.innerHTML = "submit"
        diff_searchbar_form.appendChild(diff_btn_submit)
        // extra ends here

        var products_grid = document.createElement("div");
        products_grid.classList.add("product-grid");
        products_container.appendChild(products_grid);

        for (let product in products) {
            console.log(products[product])
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

        catlvl1 = catlvl1.replaceAll('&', "amp").replaceAll(' ', "space");
        catlvl2 = catlvl2.replaceAll('&', "amp").replaceAll(' ', "space");

        if (page != 1) {
            var previous_button = document.createElement("a");
            previous_button.href = `./sortcategory.html?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page - 1}&diff_sort_select=${order}`;  // to be changed
            previous_button.classList.add("btn-not-active");
            previous_button.innerHTML = "<b>&laquo;</b>";
            pagination_buttons.appendChild(previous_button);
        }
        if (page - 1 != 0) {
            var previous_button_number = document.createElement("a");
            previous_button_number.href = `./sortcategory.html?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page - 1}&diff_sort_select=${order}`; // to be changed
            previous_button_number.classList.add("btn-not-active");
            previous_button_number.innerHTML = page - 1;
            pagination_buttons.appendChild(previous_button_number);
        }
        var current_button = document.createElement("a");
        current_button.href = `./sortcategory.html?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page}&diff_sort_select=${order}`; // to be changed
        current_button.classList.add("btn");
        current_button.innerHTML = page;
        pagination_buttons.appendChild(current_button);

        if (page + 1 <= pages) {
            var next_button_number = document.createElement("a");
            next_button_number.href = `./sortcategory.html?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page + 1}&diff_sort_select=${order}`; // to be changed
            next_button_number.classList.add("btn-not-active");
            next_button_number.innerHTML = page + 1;
            pagination_buttons.appendChild(next_button_number);
        }
        if (page != pages) {
            var next_button = document.createElement("a");
            next_button.href = `./sortcategory.html?catlvl1=${catlvl1}&catlvl2=${catlvl2}&page=${page + 1}&diff_sort_select=${order}`; // to be changed
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