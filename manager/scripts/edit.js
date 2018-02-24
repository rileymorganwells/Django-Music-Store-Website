$(function() {

  var tp = $("#id_type").val()
  console.log(tp)
  console.log($("#id_id").val())

  if (tp == 1) {
    console.log('indiv')
    $('#form > p').show()
    $('#form > p').find('input').show()
    $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date, #id_type, #id_id').hide()
    $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_max_rental_days, #id_retire_date, #id_type, #id_id').closest('p').hide()
  } else if (tp == 2) {
    $('#form > p').show()
    console.log('bulk')
    $('#form > p').find('input').show()
    $('#id_pid, #id_max_rental_days, #id_retire_date, #id_type, #id_id').hide()
    $('#id_pid, #id_max_rental_days, #id_retire_date, #id_type, #id_id').closest('p').hide()
  } else {
    $('#form > p').show()
    console.log('rental')
    $('#form > p').find('input').show()
    $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_type, #id_id').hide()
    $('#id_quantity, #id_reorder_trigger, #id_reorder_quantity, #id_type, #id_id').closest('p').hide()
  }
})
