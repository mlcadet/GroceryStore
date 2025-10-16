const productPrices = {};
const formData = $("#orderForm").serializeArray();

  // API call function
  document.getElementById("addProductBtn").addEventListener("click", function () {
  document.getElementById("productModal").style.display = "flex";
});

function closeModal() {
  document.getElementById("productModal").style.display = "none";
}

    // JSON data by api for order table
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

    // Add new button click
  $("#addMoreButton").click(function () {
    const row = $(".product-box").first().clone();
    row.find(".remove-row").removeClass("hideit");
    row.find(".product-price").text("0.00");
    row.find(".product-qty").val("1");
    row.find(".product-total").text("0.00");
    $(".product-container").append(row);
  });

    // Calculate grand total
    $(document).on("click", ".remove-row", function () {
      $(this).closest('.row').remove();
      calculateGrandTotal();
    });

    // On product change
    $(document).on("change", ".cart-product", function () {
      const product_id = $(this).val();
      const price = productPrices[product_id] || 0;
      
      $(this).closest('.row').find('.product-price').val(price);
      calculateGrandTotal();
    });

    // SAVE ORDER
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

  // SAVE NEW PRODUCT
document.getElementById("productForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const uom = document.getElementById("uom").value.trim();
  const price = parseFloat(document.getElementById("price").value);

  if (!name || !uom || isNaN(price)) {
    alert("Please fill in all fields correctly.");
    return;
  }

  const newProduct = {
    name: name,
    uom_name: uom,
    price: price
  };

  callApi("POST", productSaveApiUrl, JSON.stringify(newProduct), function (response) {
    alert("Product added successfully!");
    closeModal();
    document.getElementById("productForm").reset();
    // Optionally reload product list
    location.reload(); // or re-fetch and re-render the table
  });
});


  callApi("POST", orderSaveApiUrl, {
    data: JSON.stringify(requestPayload)
  }, function(response) {
    alert('Order saved successfully');
  });
});