select "shopapp_product"."id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."preview",
        "shopapp_product"."created_at",
        "shopapp_product"."created_by_id",
        "shopapp_product"."archived"
from "shopapp_product"
where not "shopapp_product"."archived"
order by "shopapp_product"."name" asc,
         "shopapp_product"."price" asc;
         args=();
alias=default

select "shopapp_product"."id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."preview",
        "shopapp_product"."created_at",
        "shopapp_product"."created_by_id",
        "shopapp_product"."archived"
from "shopapp_product"
where "shopapp_product"."id" = 2
LIMIT 21; args=(2,); alias=default

select "shopapp_productimage"."id",
        "shopapp_productimage"."product_id",
        "shopapp_productimage"."image",
        "shopapp_productimage"."description"
from "shopapp_productimage"
where "shopapp_productimage"."product_id"
in (2); args=(2,); alias=default

select "django_session"."session_key",
        "django_session"."session_data",
        "django_session"."expire_date"
from "django_session"
where ("django_session"."expire_date" > '2023-09-04 10:30:49.939479'
and "django_session"."session_key" = '08b38ujx98c0vpqw9l76kz4clnsnspqn')
LIMIT 21; args=('2023-09-04 10:30:49.939479', '08b38ujx98c0vpqw9l76kz4clnsnspqn');
alias=default

select "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser", "auth_user"."username",
        "auth_user"."first_name", "auth_user"."last_name",
        "auth_user"."email", "auth_user"."is_staff",
        "auth_user"."is_active", "auth_user"."date_joined"
from "auth_user" where "auth_user"."id" = 1 LIMIT 21; args=(1,); alias=default

select "shopapp_order"."id",
        "shopapp_order"."delivery_address",
        "shopapp_order"."promocode",
        "shopapp_order"."created_at",
        "shopapp_order"."user_id",
        "shopapp_order"."receipt",
        "auth_user"."id",
        "auth_user"."password",
        "auth_user"."last_login",
        "auth_user"."is_superuser",
        "auth_user"."username",
        "auth_user"."first_name",
        "auth_user"."last_name",
        "auth_user"."email",
        "auth_user"."is_staff",
        "auth_user"."is_active",
        "auth_user"."date_joined"
from "shopapp_order"
inner join "auth_user" on ("shopapp_order"."user_id" = "auth_user"."id"); args=(); alias=default

select ("shopapp_order_products"."order_id") as "_prefetch_related_val_order_id",
        "shopapp_product"."id",
        "shopapp_product"."name",
        "shopapp_product"."description",
        "shopapp_product"."price",
        "shopapp_product"."discount",
        "shopapp_product"."preview",
        "shopapp_product"."created_at",
        "shopapp_product"."created_by_id",
        "shopapp_product"."archived"
from "shopapp_product"
inner join "shopapp_order_products" on ("shopapp_product"."id" = "shopapp_order_products"."product_id")
where "shopapp_order_products"."order_id" in (2, 15, 16, 21, 24, 27, 28)
 order by "shopapp_product"."name" asc, "shopapp_product"."price" asc; args=(2, 15, 16, 21, 24, 27, 28); alias=default



