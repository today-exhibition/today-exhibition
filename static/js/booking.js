import secrets from '/static/js/secrets.js';

$("#booking-date").on("change", function() {
  const selectedDate = $("#booking-date").val();
  $("#selected-date").text(selectedDate);
});

$("#ticket-type").on("change", function() {
  const selectedPrice = $("#ticket-type").val();
  if (selectedPrice) {
    $("#selected-price").text(selectedPrice);
  }
  else {
    $("#selected-price").text("");
  }
});

$('#booking').on("click", function() {
  if (!$("#ticket-type").val() || !$("#booking-date").val()) {
    $('.modal-body').text('옵션을 모두 선택해주세요');
    $('#alertmodal').modal('show');
  }
  else {
    $('.payments').removeAttr('hidden');

    const clientKey = secrets.toss_api_key;
    const customerKey = data.user.id;

    const paymentWidget = PaymentWidget(clientKey, customerKey);

    const paymentMethods = paymentWidget.renderPaymentMethods('#payment-method',
    {
      value: $("#ticket-type").val(),
      currency: 'KRW',
      country: 'KR',
    },
    { variantKey: 'widgetA' }
    );

    paymentWidget.renderAgreement('#agreement')

    $("#payment-button").on("click", function() {
      paymentMethods.updateAmount($("#ticket-type").val());

      paymentWidget.requestPayment({
        orderId: self.crypto.randomUUID(),
        orderName: data.exhibition.title,
        successUrl: 'http://127.0.0.1:8000/booking/success',
        failUrl: 'http://127.0.0.1:8000/fail',
        customerEmail: data.user.email, 
        customerName: data.user.nickname
      }).catch(function (error) {
        if (error.code === 'USER_CANCEL') {
        // 결제 고객이 결제창을 닫았을 때 에러 처리
        } if (error.code === 'INVALID_CARD_COMPANY') {
            // 유효하지 않은 카드 코드에 대한 에러 처리
          }
      })
    })
  }
});