function showhide(id) {
    var element = document.getElementById(id);
    element.style.display = (element.style.display == 'block') ? 'none' : 'block';
}

async function navbar() {
    const URL = "http://localhost:3000/"

    var container = document.getElementById("header-container");

    var categories_container = document.createElement("div");
    categories_container.id = "categories-container";
    container.appendChild(categories_container);

    var navbar_container = document.createElement("div");
    navbar_container.classList.add("navbar-container");
    categories_container.before(navbar_container);

    var navbar = document.createElement("nav");
    var logo_div = document.createElement("div");
    logo_div.classList.add("logo-div")
    navbar_container.appendChild(navbar);
    navbar.before(logo_div);

    var logo_img = document.createElement("img");
    logo_img.classList.add("logo-img");
    logo_img.src = "./shopping-cart.png";
    logo_img.alt = "shopping cart logo";
    logo_div.appendChild(logo_img);

    var nav_list = document.createElement("ul");
    nav_list.id = "nav-list";
    navbar.appendChild(nav_list);

    var products_li = document.createElement("li");
    products_li.id = "cat-products";
    var products_a = document.createElement("a");
    products_a.href = "./products.html?&page=1";
    products_a.innerHTML = "Products";
    products_li.appendChild(products_a);
    nav_list.appendChild(products_li);

    var home_li = document.createElement("li");
    home_li.id = "cat-home";
    var home_a = document.createElement("a");
    home_a.href = "./home.html";
    home_a.innerHTML = "Home";
    home_li.appendChild(home_a);
    nav_list.appendChild(home_li);

    var searchbar_form = document.createElement("form");
    searchbar_form.action = "./search.html";
    searchbar_form.method = "get";
    searchbar_form.classList.add("form-search");
    searchbar_form.autocomplete = "off";
    products_li.before(searchbar_form);

    // var searchbar_select = document.createElement("select");
    // searchbar_select.classList.add("sort-select");
    // searchbar_select.name = "sort-select";
    // searchbar_select.id = "sort-select";
    // searchbar_form.appendChild(searchbar_select);

    // var options_list = ['None', 'Ascending', 'Descending', 'Relevance']
    // for (let option in options_list) {
    //     var opt_option = document.createElement("option");
    //     opt_option.value = options_list[option];
    //     opt_option.innerHTML = options_list[option];
    //     searchbar_select.appendChild(opt_option);
    // }

    var searchbar_input = document.createElement("input");
    searchbar_input.type = "text";
    searchbar_input.placeholder = "Search products";
    searchbar_input.classList.add("searchbar");
    searchbar_input.name = "searchbar";
    searchbar_input.autocomplete = "off";
    searchbar_form.appendChild(searchbar_input);

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
    var categories = result['categories']
    for (let category in categories) {
        if (categories[category].length != 0) {
            var catlvl1_container = document.createElement("div");
            catlvl1_container.classList.add("category-lvl1");
            catlvl1_container.id = "category-lvl1-" + category;
            catlvl1_container.style.display = "none";
            categories_container.appendChild(catlvl1_container);

            var lvl2_length = categories[category].length;
            var rem = lvl2_length % 4;
            var counter = 0;
            var prod_per_col = Math.floor(lvl2_length / 4);
            if (rem != 0) {
                prod_per_col += 1;
            }
            
            var catlvl2_container = document.createElement("div");
            catlvl2_container.classList.add("category-lvl2-container");
            catlvl1_container.appendChild(catlvl2_container);

            var catlvl1_title = document.createElement("h1");
            catlvl1_title.classList.add("category-title");
            catlvl1_title.id = "category-title";
            catlvl1_title.innerHTML = "Category - " + category;
            catlvl2_container.before(catlvl1_title);

            for (let i = 0; i < prod_per_col; i++) {
                var catlvl2 = document.createElement("div");
                catlvl2.classList.add("category-lvl2");
                for (let inner_counter = 0; inner_counter < 4; inner_counter++) {
                    if (categories[category][counter]) {
                        var catlvl2_value = document.createElement("a");
                        catlvl2_value.classList.add("category-lvl2-value");
                        catlvl2_value.href = `./category.html?catlvl1=${category.replaceAll('&', 'amp').replaceAll(" ", "space")}&catlvl2=${categories[category][counter].replaceAll('&', 'amp').replaceAll(" ", "space")}&page=1`;
                        catlvl2_value.innerHTML = categories[category][counter];
                        catlvl2.appendChild(catlvl2_value);
                        counter += 1;
                    }
                }

                catlvl2_container.appendChild(catlvl2);
            }

            var catlvl1_li = document.createElement('li');
            catlvl1_li.id = `cat-${category}`;
            catlvl1_li.classList.add("cat-"+category);
            var catlvl1_div = document.createElement("div");
            catlvl1_div.innerHTML = category;
            catlvl1_div.style.textTransform = "capitalize";
            catlvl1_li.appendChild(catlvl1_div);
            catlvl1_li.onclick = function () {
                showhide("category-lvl1-" + category)
            };

            products_li.before(catlvl1_li);
        }
    }
};


export { navbar };

window.onload = function () {
    navbar();
}