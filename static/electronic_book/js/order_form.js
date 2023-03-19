const form = document.querySelector('form');
const orde_media =
    document.querySelector('#id_order_execution_description');
const order_description = document.querySelector('#id_orde_exec_media');
form.addEventListener('submit', function (evt) {
    evt.preventDefault();
    if (order_description.value || orde_media.value) {
        this.submit();
    } else {
        alert('Заполните хотя бы одно поле!');
    }
});
