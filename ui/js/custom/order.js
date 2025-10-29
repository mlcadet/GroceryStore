// ✅ Define API endpoints
const productListApiUrl = "/api/products";
const productSaveApiUrl = "/api/products";
const orderSaveApiUrl = "/api/orders";

$(function () {
  const productPrices = {};

  // ✅ Open product modal using Bootstrap's modal API
  $(document).on('click', '#addProductBtn', function () {
    $('#productModal').modal('show');
  });

  function closeModal() {
    $('#productModal').modal('hide');
  }

  // ✅ Fetch product list and populate dropdown
  $.get(productListApiUrl, function (response) {
    if (response) {
      let options = '<option value="">Select Product</option>';
      $.each(response, function (index, product) {
        options += `<option value="${product.product_id}" data-price="${product.price}">${product.name}</option>`;
        productPrices[product.product_id] = product.price;
      });
      $(".product-box").find("select").empty().html(options);
    }
  });

  // ✅ Add new product row
  $("#addMoreButton").click(function () {
    const row = $(".product-box").first().clone();
    row.find(".remove-row").removeClass("hideit");
    row.find(".product-price").val("0.00");
    row.find(".product-qty").val("1");
    row.find(".product-total").val("0.00");
    $(".product-container").append(row);
  });

  // ✅ Remove product row
  $(document).on("click", ".remove-row", function () {
    $(this).closest('.row').remove();
    calculateGrandTotal();
  });

  // ✅ Update price and total on product change
  $(document).on("change", ".cart-product", function () {
    const product_id = $(this).val();
    const price = productPrices[product_id] || 0;

    $(this).closest('.row').find('.product-price').val(price);
    calculateGrandTotal();
  });

  // ✅ Calculate grand total
  function calculateGrandTotal() {
    let grandTotal = 0;
    $(".product-box").each(function () {
      const qty = parseFloat($(this).find(".product-qty").val()) || 0;
      const price = parseFloat($(this).find(".product-price").val()) || 0;
      const total = qty * price;
      $(this).find(".product-total").val(total.toFixed(2));
      grandTotal += total;
    });
    $("input[name='product_grand_total']").val(grandTotal.toFixed(2));
  }

  // ✅ Submit order
  $("#saveOrder").on("click", function () {
    const formData = $("#orderForm").serializeArray();
    const requestPayload = {
      customer_name: null,
      total_cost: null,
      order_details: []
    };
    let currentItem = null;

    formData.forEach(element => {
      switch (element.name) {
        case 'customerName':
          requestPayload.customer_name = element.value;
          break;
        case 'product_grand_total':
          requestPayload.total_cost = element.value;
          break;
        case 'product':
          currentItem = { product_id: element.value };
          requestPayload.order_details.push(currentItem);
          break;
        case 'qty':
          if (currentItem) currentItem.quantity = element.value;
          break;
        case 'item_total':
          if (currentItem) currentItem.total_price = element.value;
          break;
      }
    });

    // ✅ Send order to backend
    callApi('POST', orderSaveApiUrl, requestPayload, function (response) {
      alert('Order saved successfully');
      $("#orderForm")[0].reset();
      $(".product-container").html($(".product-box").first().clone());
    });
  });

  // ✅ Submit new product
  $(document).on('submit', '#productForm', function (e) {
    e.preventDefault();

    const name = $('#name').val().trim();
    const uom = $('#uom').val().trim();
    const price = parseFloat($('#price').val());

    if (!name || !uom || isNaN(price)) {
      alert('Please fill in all fields correctly.');
      return;
    }

    const newProduct = {
      name: name,
      uom_name: uom,
      price: price
    };

    callApi('POST', productSaveApiUrl, newProduct, function (response) {
      alert('Product added successfully!');
      closeModal();
      $('#productForm')[0].reset();
      location.reload(); // ✅ Refresh product list
    });
  });

  // ✅ Helper function to make API calls
  function callApi(method, url, data, callback) {
    $.ajax({
      url: url,
      method: method,
      contentType: "application/json",
      data: JSON.stringify(data),
      success: callback,
      error: function (xhr) {
        alert("API call failed: " + xhr.responseText);
      }
    });
  }
});






// const productListApiUrl = "/api/products";
// const productSaveApiUrl = "/api/products";
// const orderSaveApiUrl = "/api/orders";

// $(function () {
//   const productPrices = {};

//   // Open product modal using Bootstrap's modal API
//   $(document).on('click', '#addProductBtn', function () {
//     $('#productModal').modal('show');
//   });

//   function closeModal() {
//     $('#productModal').modal('hide');
//   }

//   // JSON data by api for order table
//   $.get(productListApiUrl, function (response) {
//     if (response) {
//       let options = '<option value="">Select Product</option>';
//       $.each(response, function (index, product) {
//         options += `<option value="${product.product_id}" data-price="${product.price}">${product.name}</option>`;
//         productPrices[product.product_id] = product.price;
//       });
//       $(".product-box").find("select").empty().html(options);
//     }
//   });

//     // Add new button click
//   $("#addMoreButton").click(function () {
//     const row = $(".product-box").first().clone();
//     row.find(".remove-row").removeClass("hideit");
//     row.find(".product-price").text("0.00");
//     row.find(".product-qty").val("1");
//     row.find(".product-total").text("0.00");
//     $(".product-container").append(row);
//   });

//     // Calculate grand total
//     $(document).on("click", ".remove-row", function () {
//       $(this).closest('.row').remove();
//       calculateGrandTotal();
//     });

//     // On product change
//     $(document).on("change", ".cart-product", function () {
//       const product_id = $(this).val();
//       const price = productPrices[product_id] || 0;
      
//       $(this).closest('.row').find('.product-price').val(price);
//       calculateGrandTotal();
//     });

//     // SAVE ORDER
//     $("#saveOrder").on("click", function () {
//   const formData = $("#orderForm").serializeArray();
//   const requestPayload = {
//     customer_name: null,
//     total_cost: null,
//     order_details: []
//   };
//   let currentItem = null;

//   formData.forEach(element => {
//     switch (element.name) {
//       case 'customerName':
//         requestPayload.customer_name = element.value;
//         break;
//       case 'product_grand_total':
//         requestPayload.total_cost = element.value;
//         break;
//       case 'product':
//         currentItem = { product_id: element.value };
//         requestPayload.order_details.push(currentItem);
//         break;
//       case 'qty':
//         if (currentItem) currentItem.quantity = element.value;
//         break;
//       case 'item_total':
//         if (currentItem) currentItem.total_price = element.value;
//         break;
//     }
//   });

//   // SAVE NEW PRODUCT
//   $(document).on('submit', '#productForm', function (e) {
//     e.preventDefault();

//     const name = $('#name').val().trim();
//     const uom = $('#uom').val().trim();
//     const price = parseFloat($('#price').val());

//     if (!name || !uom || isNaN(price)) {
//       alert('Please fill in all fields correctly.');
//       return;
//     }

//     const newProduct = {
//       name: name,
//       uom_name: uom,
//       price: price
//     };

//     callApi('POST', productSaveApiUrl, newProduct, function (response) {
//       alert('Product added successfully!');
//       closeModal();
//       $('#productForm')[0].reset();
//       // Optionally reload product list
//       location.reload(); // or re-fetch and re-render the table
//     });
//   });


//   // send the request payload directly; callApi will stringify the object
//   callApi('POST', orderSaveApiUrl, requestPayload, function (response) {
//     alert('Order saved successfully');
//   });

// });