const productModal = $('#productModal');

// Reusable API caller using fetch
async function callApi(method, url, payload = null, onSuccess = null, onError = null) {
  try {
    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: method !== 'GET' ? JSON.stringify(payload) : null
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (onSuccess) onSuccess(data);
  } catch (error) {
    console.error('API error:', error);
    if (onError) onError(error);
    else alert('Something went wrong. Please try again.');
  }
}

// Render product table
function renderProductTable(products) {
  let table = '';
  products.forEach(product => {
    table += `
      <tr data-id="${product.product_id || ''}" 
          data-name="${product.name || ''}" 
          data-unit="${product.uom_name || ''}" 
          data-price="${product.price_per_unit || 0}">
        <td>${product.name || ''}</td>
        <td>${product.uom_name || ''}</td>
        <td>${parseFloat(product.price_per_unit || 0).toFixed(2)}</td>
        <td>
          <span class="btn btn-xs btn-danger delete-product">Delete</span>
          <span class="btn btn-xs btn-primary edit-product">Edit</span>
        </td>
      </tr>`;
  });
  $("table").find('tbody').html(table);
}

// Clear modal form
function clearProductForm() {
  $("#productForm")[0].reset();
  $("#id").val('');
}

// DOM Ready
$(function () {
  // Load product list
  callApi("GET", productListApiUrl, null, renderProductTable);
  // Load UOM Dropdown
  callApi("GET", uomListApiUrl, null, function (response) {
  if (response) {
    let options = '<option value="">Select UOM</option>';
    response.forEach(uom => {
      options += `<option value="${uom.uom_name}">${uom.uom_name}</option>`;
    });
    $("#uom").html(options);
  }
});

  // Open modal for new product
  $("#addProductBtn").click(function () {
    clearProductForm();
    productModal.find('.modal-title').text('Add Product');
    productModal.modal('show');
  });

  // Open modal for edit
  $(document).on("click", ".edit-product", function () {
    const tr = $(this).closest('tr');
    $("#id").val(tr.data('id'));
    $("#name").val(tr.data('name'));
    $("#uom").val(tr.data('unit'));
    $("#price").val(tr.data('price'));
    productModal.find('.modal-title').text('Edit Product');
    productModal.modal('show');
  });

  // Save product
  $("#productForm").submit(function(e) {
    e.preventDefault(); // Prevent default form submission
    
    const name = $("#name").val().trim();
    const unit = $("#uom").val().trim();
    const price = $("#price").val().trim();
    
    // Validation block
    if (!name || !unit || !price || isNaN(price)) {
      alert("Please fill out all fields correctly.");
      return;
    }

    // Get UOM ID for the selected UOM name
    callApi("GET", uomListApiUrl, null, function(uoms) {
      const uom = uoms.find(u => u.uom_name === unit);
      if (!uom) {
        alert("Invalid UOM selected");
        return;
      }

      const requestPayload = {
        product_name: name,
        uom_id: uom.uom_id,
        price_per_unit: parseFloat(price)
      };

      callApi(
        "POST",
        productSaveApiUrl,
        requestPayload,
        (response) => {
          productModal.modal('hide');
          alert("Product saved successfully.");
          location.reload();
        },
        (error) => {
          alert("Failed to save product. Please check all fields and try again.");
          console.error("Save error:", error);
        }
      );
    });
  });

  // Delete product
  $(document).on("click", ".delete-product", function () {
    const tr = $(this).closest('tr');
    const productId = tr.data('id');

    if (confirm("Are you sure you want to delete this product?")) {
      callApi(
        "DELETE",
        `${productDeleteApiUrl}/${productId}`,
        null,
        () => {
          alert("Product deleted.");
          tr.remove();
        },
        () => {
          alert("Failed to delete product.");
        }
      );
    }
  });
});



