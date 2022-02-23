$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    console.log(id)
    var eml = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            if (data.flag==0){
                swal.fire('Quantity Exceeded');
            }
            else{
                eml.innerText = data.quantity
                document.getElementById('amount').innerText = data.amount
                document.getElementById('totalamount').innerText = data.totalamount
                location.reload(true);
        }
        }
    })
})
$('.minus-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var eml = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function (data) {
            console.log('success')
            eml.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            location.reload(true);

        }
    })
})

$('.remove-cart').click(function () {
    var id = $(this).attr('pid').toString();
    var eml = this

    $.ajax({
        type: 'GET',
        url: "/removecart",
        data: {
            prod_id : id
        },
        success: function (data) {
            console.log('Delete')
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.parentNode.remove()
            location.reload(true);
            
        }
    })
})




