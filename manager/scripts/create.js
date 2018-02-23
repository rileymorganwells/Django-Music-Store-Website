$(function() {
  $('#form > p').show()
  $('#form > p').find('input').show()
  $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date').hide()
  $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date').closest('p').hide()
  $('#id_type').on('change', function() {
    var tp = $("#id_type").val()

    if (tp == 1) {
      $('#form > p').show()
      $('#form > p').find('input').show()
      $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date').hide()
      $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date').closest('p').hide()
    } else if (tp == 2) {
      $('#form > p').show()
      $('#form > p').find('input').show()
      $('#id_pid, #id_max_rental_days, #id_retire_date').hide()
      $('#id_pid, #id_max_rental_days, #id_retire_date').closest('p').hide()
    } else {
      $('#form > p').show()
      $('#form > p').find('input').show()
      $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity').hide()
      $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity').closest('p').hide()
    }

  })
})
