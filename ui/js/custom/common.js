// Api Definitions
const orderSaveApiUrl = "http://localhost:5000/api/orders";
const productListApiUrl = "http://localhost:5000/api/products";
const uomListApiUrl = "http://localhost:5000/api/uoms";
const orderListApiUrl = "http://localhost:5000/api/orders";
const productSaveApiUrl = "http://localhost:5000/api/products";
const productDeleteApiUrl = "http://localhost:5000/api/products";
const productsApiUrl = "http://localhost:5000/api/products";

//🔄Common function to call API
function callApi(method, url, data, onSuccess, onError) {
  $.ajax({
    url: url,
    method: method,
    contentType: "application/json",
    data: method !== 'GET' ? data : null,
    success: function (response) {
      if (onSuccess) onSuccess(response);
    },
    error: function (xhr, status, error) {
      console.error("API error:", error); 
      if (onError) onError(error);
      else alert("Something went wrong. Please try again.");
    }
  });
}

//💰Placeholder for grand total calculation
function calculateGrandTotal() {
  let total = 0;
  $(".product-item").each(function (index) {
    let qty = parseFloat($(this).find(".product-qty").val()) || 0;
    let price = parseFloat($(this).find(".product-price").text()) || 0;
    let itemTotal = qty * price;
    $(this).find("#item_total").val(price.toFixed(2));
    total += itemTotal;
  });
  $("#product_grand_total").text(total.toFixed(2));
}

//🔄 Parser for order object
function orderParser(order) {
  return {
    id: order.id,
    date: order.date,
    orderNo: order.order_number,
    customerName: order.customer_name,
    cost: parseFloat(order.total)
  };
}

//🛒 Parser for product object
function productParser(product) {
  return {
    id: product.id,
    name: product.name,
    unit: product.uom_name,
    price: product.price
  };
}

//🛒 Parser for product dropdown
function productDropParser(product) {
return {
    id: product.id,
    name: product.name,
    unit: product.uom_name,
    price: product.price
  };
}

//🧪 Parser for UOM dropdown
function uomDropParser(uom) {
  return {
    id: uom.id,
    name: uom.name
  };
}