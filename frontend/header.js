function showhide(id) {
    var element = document.getElementById(id);
    element.style.display = (element.style.display == 'block') ? 'none' : 'block';
}

function showcat1(catid) {
    window.location.href = `./category.html?catid=${catid}&page=1`;
}

async function navbar() {
    const URL = "http://localhost:3000/"

    var categories_container = document.getElementById("categories-container");

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
        if (categories[category].length != 1) {

            var catlvl1_container = document.createElement("div");
            catlvl1_container.classList.add("category-lvl1");
            catlvl1_container.id = "category-lvl1-" + category;
            catlvl1_container.style.display = "none";
            categories_container.appendChild(catlvl1_container);

            var lvl2_length = categories[category].length;
            var rem = lvl2_length % 4;
            var counter = 1;
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
                        catlvl2_value.href = `./category.html?catid=${categories[category][counter][1]}&page=1`;
                        catlvl2_value.innerHTML = categories[category][counter][0];
                        catlvl2.appendChild(catlvl2_value);
                        counter += 1;
                    }
                }
                catlvl2_container.appendChild(catlvl2);
            }

            var products_li = document.getElementById("cat-products");

            var catlvl1_li = document.createElement('li');
            catlvl1_li.id = `cat-${category}`;
            catlvl1_li.innerHTML = category;
            catlvl1_li.classList.add("cat-" + category);
            catlvl1_li.onclick = function () {
                showhide("category-lvl1-" + category)
            };
            catlvl1_li.ondblclick = function () {
                showcat1(categories[category][0]);
            };
            products_li.before(catlvl1_li);
        }
    }
};


export { navbar };

window.onload = function () {
    navbar();
}