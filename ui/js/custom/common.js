// API base configuration (change this to switch environments)
// Use a relative base by default to avoid CORS between 127.0.0.1 and localhost
// If you need to point to a remote server set window.API_BASE before loading this file.
const API_BASE = (typeof window !== 'undefined' && window.API_BASE) ? window.API_BASE : '';

// Api Definitions (use API_BASE)
const orderSaveApiUrl = `${API_BASE}/api/orders`;
const orderListApiUrl = `${API_BASE}/api/orders`;
const productListApiUrl = `${API_BASE}/api/products`;
const productSaveApiUrl = `${API_BASE}/api/products`;
const productDeleteApiUrl = `${API_BASE}/api/products`;
const uomListApiUrl = `${API_BASE}/api/uoms`;
const productsApiUrl = `${API_BASE}/api/products`;

//🔄Common function to call API
function callApi(method, url, data, onSuccess, onError) {
  // If data is an object and not a string, stringify it for JSON POST/PUT/PATCH
  var payload = data;
  if (method !== 'GET' && typeof data === 'object') {
    try {
      payload = JSON.stringify(data);
    } catch (e) {
      payload = data;
    }
  }

  $.ajax({
    url: url,
    method: method,
    contentType: "application/json",
    data: method !== 'GET' ? payload : null,
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