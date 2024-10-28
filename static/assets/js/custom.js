$('#commentForm').submit(function (e) {
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr('method'),

        url: $(this).attr('action'),

        dataType: "json",

        success: function (resp) {
            if (resp.bool == true) {
                $('#review-success-alert').html("Review Added Successfully")
                $('.hide-review-text').hide()
                $('.hide-commentform').hide()

                let _html = '<div class="single-comment justify-content-between d-flex">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src=""alt="" />'
                _html += '<a href="#"class="font-heading text-brand">' + resp.context.user + '</a>'
                _html += '</div>'
                _html += '<div class="desc">'
                _html += '<div class="d-flex justify-content-between mb-10">'
                _html += '<div class="d-flex align-items-center">'
                _html += '<span class="font-xs text-muted">' + resp.context.review_date + '</span>'
                _html += '</div>'
                _html += '<div class="product-rate d-inline-block">'
                _html += '<div class="product-rating" style="width: ' + resp.context.star_rating + '%">'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'
                _html += '<p class="mb-10">' + resp.context.review + '</p>'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'

                $('.comment-list').prepend(_html)
            }
        }
    })
})




$(document).ready(function () {
    $(".filter-checkbox").on("click", function () {

        let filter_object = {}

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data('filter')

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
        })

        $.ajax({
            url: "/product-filter",
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("trying to filter product .....")
            },
            success: function (response) {
                console.log("data filtered successfully")
                $("#filtered-product").html(response.data)
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("AJAX Error: " + textStatus + ": " + errorThrown);
            }
        })
    })


    $(".add-to-cart-btn").on('click', function () {
        const thisVal = $(this);
        const productPid = $(this).attr("data-index");

        $.ajax({
            url: '/add-to-cart',
            data: {
                'pid': productPid,
            },
            dataType: 'json',
            beforeSend: function () {
                console.log("Adding Product to Cart .......");
            },
            success: function (response) {
                alert('Item Added to cart');

                // Check the response and update the cart item count
                if (response.total_cart_items !== undefined) {
                    $(".cart-item-count").text(response.total_cart_items);
                } else {
                    console.error("total_cart_items not found in response");
                }
            },
            error: function (xhr, status, error) {
                console.error("Error adding product to cart: ", error);
            }
        });
    });



})


// add to cart from product detail page

// $("#add-to-cart-btn").on('click', function () {
//     let quantity = $('#product-quantity').val()
//     let product_title = $('#product-title').val()
//     let product_id = $('#product-id').val()
//     let product_price = $('#current-product-price').text()
//     let this_val = $(this)


//     console.log(quantity)
//     console.log(product_id)
//     console.log(product_price)
//     console.log(product_title)
//     console.log(this_val)

//     $.ajax({
//         url: '/add-to-cart',
//         data: {
//             'pid': product_id,
//             'qty': quantity,
//             'title': product_title,
//             'price': product_price
//         },
//         dataType: 'json',
//         beforeSend: function () {
//             console.log("Adding Product to Cart .......")
//         },
//         success: function (response) {
//             this_val.html("Added to Cart.")
//             console.log("Product Added to Cart")
//             $(".cart-item-count").text(response.total_count_items)
//         }
//     })
// })

// add to cart from all pages








// delete from cart

$(document).on('click', '.delete-from-cart', function () {
    let productPid = $(this).attr("data-productpid")
    console.log("this is the product pid", productPid)

    $.ajax({
        url: '/delete-from-cart',
        data: { 'productPid': productPid },
        dataType: 'json',
        success: function (response) {
            alert('Item removed from cart');
            $(".cart-item-count").text(response.cart_count)
            $("#cart-list").html(response.data)


        }
    })
})

$(document).on('click', '.update-cart', function () {
    let productPid = $(this).attr("data-productpid")
    const quantity = $('.item-quantity-' + productPid).val()
    console.log("this is the product pid", productPid)
    console.log("this is the current quantity, ", quantity)

    $.ajax({
        url: '/update-cart',
        data: { 'productPid': productPid, 'quantity': quantity },
        dataType: 'json',
        success: function (response) {
            alert('Item updated');
            $("#cart-list").html(response.data)

        }
    })
})

// add to wishlist

$(document).on('click', '.add-to-wishlist', function () {
    let productPid = $(this).attr("data-productpid")
    console.log("this is the product pid", productPid)

    $.ajax({
        url: '/add-to-wishlist',
        data: { 'productPid': productPid },
        dataType: 'json',
        success: function (response) {
            alert('Added to wishlist');
            $(".total-wishitems").text(response.wishitems)

        }
    })
})

// delete from wishlist
$(document).on('click', '.delete-from-wishlist', function () {
    let productPid = $(this).attr("data-productpid")
    console.log("this is the product pid", productPid)

    $.ajax({
        url: '/delete-from-wishlist',
        data: { 'productPid': productPid },
        dataType: 'json',
        success: function (response) {
            alert('Removed from wishlist');
            $(".total-wishitems").text(response.wishitems)
            $("#wish-list").html(response.data)

        }
    })
})

$(document).on('click', '.set-default-address', function () {
    let address_id = $(this).attr("data-addressid")
    console.log("this is the address id: ", address_id)

    $.ajax({
        url: "/set-default-address",
        data: { 'address_id': address_id },
        dataType: 'json',
        success: function (response) {
            console.log("the default address has been changed.")
            $("#default-address").html(response.data)

        }
    })
})

$(document).on('submit', '#contact-form-ajax', function (e) {
    e.preventDefault()
    let full_name = $("#full_name").val()
    let email = $("#email").val()
    let mobile = $("#mobile").val()
    let subject = $("#subject").val()
    let message = $("#message").val()

    $.ajax({
        url: "/user/ajax-contact",
        data: {
            'full_name': full_name,
            'email': email,
            'mobile': mobile,
            'subject': subject,
            'message': message
        },
        dataType: 'json',
        beforeSend: function () {
            console.log("Sending to server")
        },
        success: function () {
            console.log('back from server')
            $("#contact-form-ajax").html('<h5>Message sent successfully.</h5>')
        }
    })
})

$(document).on('submit', '.account-detail-update', function (e) {
    e.preventDefault()
    let user_id = $(this).attr("data-userid")
    let first_name = $("#user_firstname").val()
    let last_name = $("#user_lastname").val()
    let email = $("#user_email").val()
    let bio = $("#user_bio").val()
    let username = $("#user_username").val()

    console.log("this user has an id of: ", user_id)

    $.ajax({
        url: "/user/account-update",
        data: {
            'first_name': first_name,
            'email': email,
            'last_name': last_name,
            'username': username,
            'bio': bio,
            'user_id': user_id
        },
        dataType: 'json',
        beforeSend: function () {
            console.log("Sending to server")
        },
        success: function (response) {
            console.log('back from server')
            $("#account-update").html(response.data)
        }
    })
})