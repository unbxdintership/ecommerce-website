
create table productinfo(product_id text,product_title text,product_image text,product_price text,product_availability,product_name text,product_description text);
create table category(id serial,category text,parent_id int,productid text,level int);