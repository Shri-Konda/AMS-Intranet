!(function ($) {
  "use strict";

  // Smooth scroll for the navigation menu and links with .scrollto classes
  var scrolltoOffset = $('#header').outerHeight() - 17;
  $(document).on('click', '.nav-menu a, .mobile-nav a, .scrollto', function (e) {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      if (target.length) {
        e.preventDefault();

        var scrollto = target.offset().top - scrolltoOffset;

        if ($(this).attr("href") == '#header') {
          scrollto = 0;
        }

        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
        return false;
      }
    }
  });

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function () {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top - scrolltoOffset;
        $('html, body').animate({
          scrollTop: scrollto
        }, 1500, 'easeInOutExpo');
      }
    }
  });

  // Mobile Navigation
  if ($('.nav-menu').length) {
    var $mobile_nav = $('.nav-menu').clone().prop({
      class: 'mobile-nav d-lg-none'
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" class="mobile-nav-toggle d-lg-none"><i class="icofont-navigation-menu"></i></button>');
    $('body').append('<div class="mobile-nav-overly"></div>');

    $(document).on('click', '.mobile-nav-toggle', function (e) {
      $('body').toggleClass('mobile-nav-active');
      $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
      $('.mobile-nav-overly').toggle();
    });

    $(document).on('click', '.mobile-nav .drop-down > a', function (e) {
      e.preventDefault();
      $(this).next().slideToggle(300);
      $(this).parent().toggleClass('active');
    });

    $(document).click(function (e) {
      var container = $(".mobile-nav, .mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
          $('.mobile-nav-overly').fadeOut();
        }
      }
    });
  } else if ($(".mobile-nav, .mobile-nav-toggle").length) {
    $(".mobile-nav, .mobile-nav-toggle").hide();
  }

  // Toggle .header-scrolled class to #header when page is scrolled
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });

  if ($(window).scrollTop() > 100) {
    $('#header').addClass('header-scrolled');
  }

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
    } else {
      $('.back-to-top').fadeOut('slow');
    }
  });

  $('.back-to-top').click(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });



  // JS for form submission at 'edit single product' page for product records table | Ajax call
  $(document).on('submit', '#ProdForm', function (e) {
    e.preventDefault();
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var formData = JSON.stringify($(this).serializeArray());
    $.ajax({
      url: '../../formsubmit',
      type: 'post',
      data: {
        csrfmiddlewaretoken: csrf,
        data: formData
      },
      success: function (response) {
        var div_body = document.querySelector('#prodform_container');
        $(this).remove();
        div_body.innerHTML = `<div class="card" style="width: 15em; text-align: center; height: 5em; margin-bottom: 10px !important; margin: auto;">
                                <div style="margin: auto;">
                                  <strong>${response.msg}</strong>
                                </div>
                              </div>`;
      }
    });
  });

  // JS for form submission at 'edit single product' page for technical records table | Ajax call
  $(document).on('submit', '#TechForm', function (e) {
    e.preventDefault();
    var csrf = $("input[name=csrfmiddlewaretoken]").val();
    var formData = JSON.stringify($(this).serializeArray());
    $.ajax({
      url: '../../formsubmit',
      type: 'post',
      data: {
        csrfmiddlewaretoken: csrf,
        data: formData
      },
      success: function (response) {
        var div_body = document.querySelector('#techform_container');
        $(this).remove();
        div_body.innerHTML = `<div class="card" style="width: 15em; text-align: center; height: 5em; margin-bottom: 10px !important; margin: auto;">
                                <div style="margin: auto;">
                                  <strong>${response.msg}</strong>
                                </div>
                              </div>`;
      }
    });
  });

  // JS for form submission at 'add new supplier' page | Ajax call
  $(document).on('submit', '#NewSupplier', function (e) {
    e.preventDefault();
    $.ajax({
      url: 'AddNewSupplier',
      type: 'post',
      data:{
        comp_name: $('#comp_name').val(),
        acc_code: $('#acc_code').val(),
        curr_code: $('#curr_code').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      },
      success: function(json){
        document.getElementById('NewSupplier').reset();
        if (json.c_name == "" && json.c_code == ""){
          alert("Please enter the details!")
        }
        else {
          var card = document.querySelector("#SuccessCard");
          card.innerHTML = `<div class="card" style="margin-right: 20%; width: 20em;">
                              <div style="margin: 5%; margin-bottom: 2%;">    
                                <h4><strong>${json.c_name}</strong></h4>
                                <h6 class="text-muted">${json.c_code}</h6>
                                <h6 class="text-muted">${json.cur}</h6>
                                <br>
                                <p class="text-success" style="text-align:center;">${json.msg}</p>
                              </div>
                            </div>`;
        }
      }
    });
  });

  // JS to hide tracking details modal box on FedEx UK/USA.html and DHL.html
  $('button[id^="closeInfo"]').on('click', function () {
    var v = document.getElementById("showOrHide");
    if (v.style.display === "none") {
      v.style.display = "block";
    } else {
      v.style.display = "none";
    }
  });

  // JS for loading shipment details on index.html | Ajax call
  $(document).ready(function () {
    $('button[id^="viewOrder"]').one('click', function () {
      var OID = $(this).val();
      var shipping_div = document.querySelector("#shipping"+OID);
      var itemname_div = document.querySelector("#item_name"+OID);
      $.ajax({
        url: 'shipment_details',
        type: 'get',
        data:{
          order_id: OID
        },
        success: function(json){
          var form = document.querySelector("#form4" + OID);
          var form_div = document.querySelector("#orderprocessing" + OID);
          if (json.status != "pending"){
            form.remove();
            form_div.style.cssText = 'text-align: center;'
            var div_inside_form_div = document.createElement("div");
            div_inside_form_div.innerHTML = `Order Status: <strong>${json.status}</strong>`;
            form_div.append(div_inside_form_div);
          }
          for (const [key, value] of Object.entries(json.result)) {
            const div = document.createElement("div");
            div.style.cssText = "white-space: pre-wrap;";
            div.innerHTML = `<strong>${key}: </strong>${value}`;
            shipping_div.append(div);
          }
          for (const [ele, dict] of Object.entries(json.item_name)) {
            for (const [key, value] of Object.entries(dict)) {
              const item_div = document.createElement("div");
              item_div.style.cssText = "white-space: pre-wrap;";
              item_div.innerHTML = `<strong>${key}: </strong>${value}`;
              if (key == 'sku'){
                item_div.style.cssText = "white-space: pre-wrap; margin-bottom: 5px;";
              }
              itemname_div.append(item_div);
            }
          }
          const price_div = document.createElement("div");
          price_div.style.cssText = 'margin-top: 20px;';
          price_div.innerHTML = `<strong>Grand Total: </strong>${json.price}`;
          itemname_div.append(price_div);
          
          var spinner1 = document.querySelector("#spinner"+ OID);
          spinner1.remove();
          var spinner2 = document.querySelector("#spinnerItem"+ OID);
          spinner2.remove();
        }
      });
    });

    // Removes message generated by Django_messages from the page
    var message_ele = document.getElementById("shipment_msg");
    if (message_ele) {
      setTimeout(function(){
        message_ele.style.display = "none"; 
      }, 3500);
    }

  });

  // JS for sorting table by,if available, GBP per ug o/w Purchase price GBP
  $(document).ready(function () {  
    var table =document.querySelector("#sim_prod_body");
    if (document.querySelector("#GBPperug")) {
      sortTable(6);
    }
    else if (document.querySelector("#PriceGBPhead")) {
      sortTable(5);
    }
    function sortTable(col_index){
      var rows, switching, i, x, y, shouldSwitch;
      switching = true
      while (switching){
        switching = false;
        rows = table.rows;
        for (i = 0; i < (rows.length - 1) ; i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[col_index];
          y = rows[i + 1].getElementsByTagName("TD")[col_index];
          if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {
            shouldSwitch = true;
            break;
          }
        }
        if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
        }
      }
    }
  });
  
})(jQuery);