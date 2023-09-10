import secrets from '/static/js/secrets.js';

$(document).ready(function () {
  const clientKey = secrets.toss_api_key; // 테스트용 클라이언트 키
  const customerKey = self.crypto.randomUUID(); // 내 상점에서 고객을 구분하기 위해 발급한 고객의 고유 ID -> 이거 숨겨야 하나?

  const paymentWidget = PaymentWidget(clientKey, customerKey); // 회원 결제

  const paymentMethodWidget = paymentWidget.renderPaymentMethods('#payment-method',
  {
    value: 10000,
    currency: 'KRW',
    country: 'KR',
  },
  { variantKey: 'widgetA' }
  );

  paymentWidget.renderAgreement('#agreement')

  document.querySelector("#payment-button").addEventListener("click",()=>{
    paymentWidget.requestPayment({
      orderId: self.crypto.randomUUID(),
      orderName: '토스 티셔츠 외 2건',
      successUrl: 'http://127.0.0.1:8000/booking/success',
      failUrl: 'http://127.0.0.1:8000/fail',
      customerEmail: 'customer123@gmail.com', 
      customerName: '김토스'
    }).catch(function (error) {
      if (error.code === 'USER_CANCEL') {
      // 결제 고객이 결제창을 닫았을 때 에러 처리
      } if (error.code === 'INVALID_CARD_COMPANY') {
          // 유효하지 않은 카드 코드에 대한 에러 처리
        }
    })  
  })
});
