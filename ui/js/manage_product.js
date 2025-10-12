const productModal = $('#productModal');

$(function () {
    // Load product list
    $.get(productListApiUrl, function (response) {
        if (response && Array.isArray(response)) {
            let table = '';
            $.each(response, function (index, product) {
                table += `
                    <tr data-id="${product.product_id}" 
                        data-name="${product.name}" 
                        data-unit="${product.uom_name}" 
                        data-price="${product.price_per_unit}">
                        <td>${product.name}</td>
                        <td>${product.uom_name}</td>
                        <td>${product.price_per_unit}</td>
                        <td>
                            <span class="btn btn-xs btn-danger delete-product">Delete</span>
                            <span class="btn btn-xs btn-primary edit-product">Edit</span>
                        </td>
                    </tr>`;
            });
            $("table").find('tbody').empty().html(table);
        }
    });

    // Open modal on edit
    $(document).on("click", ".edit-product", function () {
        const tr = $(this).closest('tr');
        $("#id").val(tr.data('id'));
        $("#name").val(tr.data('name'));
        $("#unit").val(tr.data('unit'));
        $("#price").val(tr.data('price'));
        productModal.find('.modal-title').text('Edit Product');
        productModal.modal('show');
    });

    // Save product
    $("#saveProduct").click(function () {
        const data = $("#productForm").serializeArray();
        const requestPayload = {
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };

        for (let i = 0; i < data.length; i++) {
            let element = data[i];
            switch (element.name) {
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value;
                    break;
            }
        }

        callApi("POST", productSaveApiUrl, {
            data: JSON.stringify(requestPayload)
        });

        productModal.modal('hide');
        alert("Product saved successfully.");
        location.reload(); // or re-fetch the product list
    });

    // Delete product
    $(document).on("click", ".delete-product", function () {
        const tr = $(this).closest('tr');
        const productId = tr.data('id');

        if (confirm("Are you sure you want to delete this product?")) {
            callApi("DELETE", productDeleteApiUrl + "/" + productId, {});
            alert("Product deleted.");
            tr.remove(); // or location.reload();
        }
    });
});