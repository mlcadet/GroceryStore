$(function () {
  // JSON data by API call for order table
  $.get(orderListApiUrl, function (response) {
    let table = '';
    let grandTotal = 0;

    if (response && response.length > 0) {
      $.each(response, function (index, order) {
        const total = parseFloat(order.total) || 0;
        grandTotal += total;

        table += `
          <tr>
            <td>${order.datetime}</td>
            <td>${order.customer_name}</td>
            <td>$${total.toFixed(2)}</td>
          </tr>`;
      });

      $('#orderTable tbody').html(table);
      $('#grandTotal').text(`$${grandTotal.toFixed(2)}`);
    } else {
      $('#orderTable tbody').html('<tr><td colspan="3">No orders found</td></tr>');
      $('#grandTotal').text('$0.00');
    }
  });
});
